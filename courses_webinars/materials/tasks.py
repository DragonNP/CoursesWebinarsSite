import traceback

from celery import shared_task, states
from celery.exceptions import Ignore
from celery.utils.log import get_task_logger

from courses.getCourse import GetCourse
from courses_webinars.settings import YANDEX_DISK_TOKEN, BASE_DIR
from users.models import UserTaskLink
from .yandex_disk import YandexDiskResources as YaDisk
from .downloader import Downloader
from .models import MaterialLesson, MaterialType, VideoType

ya_disk = YaDisk(YANDEX_DISK_TOKEN)
downloader = Downloader(BASE_DIR)

logger = get_task_logger(__name__)

YA_DISK_BASE_PATH = 'courses_webinars/materials'


def get_link(filename):
    path = YA_DISK_BASE_PATH + '/lesson/' + filename
    result = ya_disk.get_link_for_download(path)
    return result


@shared_task(bind=True, acks_late=True, reject_on_worker_lost=True)
def add_video_to_lesson(self, lesson_pk: int, url: str, video_type: VideoType):
    def callback_video(percent):
        callback_update_percent(self, percent, 0, 30)

    self.update_state(state='PROGRESS', meta={'process_percent': 0})
    if video_type == VideoType.YOUTUBE:
        result = downloader.save_youtube_video(url, callback_video)
    else:
        result = downloader.save_m3u8_video(url, callback_video)

    _base_task_for_lesson(self, lesson_pk, result, MaterialType.VIDEO)


@shared_task(bind=True, acks_late=True, reject_on_worker_lost=True)
def add_audio_to_lesson(self, lesson_pk: int, url: str):
    self.update_state(state='PROGRESS', meta={'process_percent': 0})
    result = downloader.save_audio_image(url)

    _base_task_for_lesson(self, lesson_pk, result, MaterialType.AUDIO)


@shared_task(bind=True, acks_late=True, reject_on_worker_lost=True)
def add_image_to_lesson(self, lesson_pk: int, url: str):
    self.update_state(state='PROGRESS', meta={'process_percent': 0})
    result = downloader.save_audio_image(url)

    _base_task_for_lesson(self, lesson_pk, result, MaterialType.IMAGE)


@shared_task(bind=True, acks_late=True, reject_on_worker_lost=True)
def add_file_to_lesson(self, lesson_pk: int, data: dict, get_course_data: dict):
    self.update_state(state='PROGRESS', meta={'process_percent': 0})

    get_course = GetCourse(get_course_data['host'])
    get_course.login(get_course_data['email'], get_course_data['password'])
    cookies = {
        'PHPSESSID5': get_course.phpsessid5
    }

    result = downloader.save_file(data, cookies=cookies)

    _base_task_for_lesson(self, lesson_pk, result, MaterialType.FILE)


def _base_task_for_lesson(current_task, lesson_pk, result_download, material_type: MaterialType):
    if not result_download[0]:
        logger.error(result_download[1])
        current_task.update_state(state=states.FAILURE,
                                  meta={
                                      'exc_type': 'ERROR',
                                      'exc_message': result_download[1]
                                  })
        raise Ignore()
    current_task.update_state(state='PROGRESS', meta={'process_percent': 30})

    filename = result_download[1]
    path = f'{BASE_DIR}/temp/{filename}'

    file_name = '.'.join(filename.split('.')[:-1])
    file_format = filename.split('.')[-1]
    try:
        logger.info('Добавляем материал в таблицу')
        material = MaterialLesson.objects.create(name=file_name,
                                                 lesson_id=lesson_pk,
                                                 type=material_type,
                                                 extension=file_format,
                                                 is_saved=False)
    except Exception as ex:
        current_task.update_state(state=states.FAILURE,
                                  meta={
                                      'exc_type': type(ex).__name__,
                                      'exc_message': traceback.format_exc().split('\n')
                                  })
        _delete_file(filename)
        raise Ignore()
    current_task.update_state(state='PROGRESS', meta={'process_percent': 40})

    logger.info('Загружаем материал на я.диск')
    filename_for_disk = str(material.pk) + '.' + file_format
    path_for_ya_disk = YA_DISK_BASE_PATH + '/lesson/' + filename_for_disk

    def callback_ya_disk(percent):
        callback_update_percent(current_task, percent, 40, 70)

    result = ya_disk.upload_file(path_for_ya_disk, path, callback_ya_disk)
    if not result[0]:
        current_task.update_state(state=states.FAILURE, meta={'result': result[1]})
        return result[1]
    current_task.update_state(state='PROGRESS', meta={'process_percent': 70})

    logger.info('Обновляем бд')
    material.is_saved = True
    material.save()
    current_task.update_state(state='PROGRESS', meta={'process_percent': 80})

    _delete_file(filename)
    current_task.update_state(state='PROGRESS', meta={'process_percent': 90})

    UserTaskLink.objects.get(task_id=current_task.request.id).delete()
    current_task.update_state(state='PROGRESS', meta={'process_percent': 100})


def _delete_file(filename):
    logger.info('Удаляем файл')
    return downloader.remove(filename)


def callback_update_percent(current_task, percent, start=0, stop=100):
    coefficient = 100 / (stop - start)
    current_task.update_state(state='PROGRESS', meta={'process_percent': start + percent / coefficient})
