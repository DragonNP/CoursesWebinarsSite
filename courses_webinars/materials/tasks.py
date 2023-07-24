from celery import shared_task, states
from celery.utils.log import get_task_logger

from courses_webinars.settings import YANDEX_DISK_TOKEN, BASE_DIR
from users.models import UserTaskLink
from .yandex_disk import YandexDiskResources as YaDisk
from .downloader import Downloader
from .models import MaterialLesson, MaterialType, VideoType

ya_disk = YaDisk(YANDEX_DISK_TOKEN)
# ya_disk.create_root_dir('courses_webinars')
# ya_disk.create_folder('materials')
# ya_disk.create_folder('materials/lesson')

downloader = Downloader(BASE_DIR)

logger = get_task_logger(__name__)


@shared_task(bind=True)
def add_video_to_lesson(self, lesson_pk: int, url: str, video_type: VideoType):
    logger.info('Запуск таска по добавлению видео')
    self.update_state(state='PROGRESS', meta={'process_percent': 0})
    if video_type == VideoType.YOUTUBE:
        result = downloader.save_youtube_video(self, url)
    else:
        result = downloader.save_m3u8_video(self, url)
    logger.info(f'Видео скачалось: {result}')

    _base_task(self, lesson_pk, result, MaterialType.VIDEO)


@shared_task(bind=True)
def add_audio_to_lesson(self, lesson_pk: int, url: str):
    self.update_state(state='PROGRESS', meta={'process_percent': 0})
    result = downloader.save_file(url)

    _base_task(self, lesson_pk, result, MaterialType.AUDIO)


@shared_task(bind=True)
def add_image_to_lesson(self, lesson_pk: int, url: str):
    self.update_state(state='PROGRESS', meta={'process_percent': 0})
    result = downloader.save_file(url)

    _base_task(self, lesson_pk, result, MaterialType.IMAGE)


def _base_task(current_task, lesson_pk, result_download, material_type: MaterialType):
    if not result_download[0]:
        current_task.update_state(state=states.FAILURE, meta={'result': result_download[1]})
        return result_download[1]
    current_task.update_state(state='PROGRESS', meta={'process_percent': 20})

    filename = result_download[1]
    path = f'{BASE_DIR}/temp/{filename}'

    file_name = '.'.join(filename.split('.')[:-1])
    file_format = filename.split('.')[-1]
    try:
        logger.info(
            f'Пробуем добавить материал в бд: name={file_name}, lesson_id={lesson_pk}, type={MaterialType.VIDEO}, extension={file_format}, is_saved=False')
        material = MaterialLesson.objects.create(name=file_name,
                                                 lesson_id=lesson_pk,
                                                 type=material_type,
                                                 extension=file_format,
                                                 is_saved=False)
    except Exception as e:
        current_task.update_state(state=states.FAILURE, meta=e)
        raise e

    logger.info('Материал добавлен в бд')
    current_task.update_state(state='PROGRESS', meta={'process_percent': 40})

    logger.info('Загружаем материал на я.диск')
    filename_for_disk = str(material.pk) + '.' + file_format
    result = ya_disk.upload_file(f'materials/lesson/{filename_for_disk}', path)
    if not result[0]:
        current_task.update_state(state=states.FAILURE, meta={'result': result[1]})
        return result[1]
    current_task.update_state(state='PROGRESS', meta={'process_percent': 60})
    logger.info('материал загружен')

    logger.info('Обновляем бд')
    material.is_saved = True
    material.save()
    current_task.update_state(state='PROGRESS', meta={'process_percent': 80})

    logger.info('Удаляем файл')
    downloader.remove(filename)
    current_task.update_state(state='PROGRESS', meta={'process_percent': 100})

    UserTaskLink.objects.get(task_id=current_task.request.id).delete()