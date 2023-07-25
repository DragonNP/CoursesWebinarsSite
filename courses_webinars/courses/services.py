import json

from django.contrib.auth.models import User

import materials.tasks
from courses.getCourse import GetCourse
from courses.models import Module, Lesson
from materials.models import MaterialLesson, MaterialType, VideoType
from users.models import UserLessonLink, UserTaskLink, UserRootModuleLink


def get_context_for_user_courses(user: User) -> dict:
    """Обрабатывает корневые модули и возвращает обработанные модули пользователя в формате контекст для дальнейшего
    рендеринга страницы"""
    context = {}

    user_courses = []
    for user_module_link in UserRootModuleLink.objects.filter(user=user):
        module = user_module_link.module

        course = {
            'id': str(module.pk),
            'name': module.name,
            'is_watched': user_module_link.is_watched
        }
        user_courses.append(course)

    context['courses'] = user_courses

    return context


def get_context_for_module(user: User, module_pk: str) -> dict:
    """Обрабатывает данные модуля и возвращает контекст для дальнейшего рендеринга страницы"""
    context = {}

    modules = []
    for module in Module.objects.filter(parent_id=module_pk):
        modules.append({
            'id': str(module.pk),
            'name': module.name
        })
    context['modules'] = modules

    lessons = []
    for lesson in Lesson.objects.filter(module_id=module_pk):
        user_lesson_link = UserLessonLink.objects.filter(user=user, lesson=lesson).first()
        if user_lesson_link is None:
            is_watched = False
        else:
            is_watched = user_lesson_link.is_watched

        lessons.append({
            'id': str(lesson.pk),
            'name': lesson.name,
            'description': lesson.description,
            'is_watched': is_watched
        })
    context['lessons'] = lessons

    return context


def get_context_for_lesson(user: User, lesson_pk: str) -> dict:
    """Обрабатывает данные урока и возвращает контекст для дальнейшего рендеринга страницы"""
    context = {'lesson': {}}

    lesson = Lesson.objects.get(pk=lesson_pk)
    user_lesson_link = UserLessonLink.objects.get(user=user, lesson=lesson)

    videos = []
    photos = []
    audios = []
    files = []
    for material in MaterialLesson.objects.filter(lesson=lesson, is_saved=True):
        filename = str(material.pk) + '.' + material.extension
        res = materials.tasks.get_link(filename)
        if not res[0]:
            print(res[1])
            continue

        if material.type == MaterialType.VIDEO:
            videos += [{'url': res[1], 'extension': material.extension}]
        elif material.type == MaterialType.IMAGE:
            photos += [res[1]]
        elif material.type == MaterialType.AUDIO:
            audios += [{'url': res[1], 'extension': material.extension}]
        elif material.type == MaterialType.FILE:
            files += [{'url': res[1], 'name': material.name}]

    context['lesson']['videos'] = videos
    context['lesson']['photos'] = photos
    context['lesson']['audios'] = audios
    context['lesson']['files'] = files
    context['lesson']['watched'] = user_lesson_link.is_watched
    context['lesson']['name'] = lesson.name
    context['lesson']['text'] = lesson.text.decode('utf-8')

    return context


def get_list_courses_from_get_course(parameters) -> dict:
    """Возвращает все курсы, модули в курсах, уроки (ссылка и название) в хронологической последовательности,
    как они есть на производном сайте GetCourse"""

    js = {'success': True, 'data': {}, 'errorMessage': ''}

    # Проверяем, все ли параметры заданы
    if not _check_variables_on_parameters(parameters, ['url', 'email', 'password']):
        js['success'] = False
        js['errorMessage'] = 'Необходимые параметры не указаны'
        return js

    url: str = parameters['url']
    email: str = parameters['email']
    password: str = parameters['password']
    host = _get_host_from_url(url)

    # Авторизуемся на производном сайте GetCourse
    get_course = GetCourse(host)
    response = get_course.login(email, password)
    if not response['success']:
        js['success'] = False
        js['errorMessage'] = response['message']
        return js

    # Скачиваем названия всех курсов и уроков
    js['data'] = get_course.get_all_trenings()

    return js


def save_courses(user: User, request_body):
    """Сохраняет курсы (модули, уроки, материалы) из request_body"""
    response = {'success': True, 'data': {}, 'errorMessage': ''}

    body = json.loads(request_body.decode('utf-8'))
    account_data = body['account']
    courses = body['data']
    host = _get_host_from_url(account_data['url'])

    # Авторизуемся на производном сайте GetCourse
    get_course = GetCourse(host)
    result = get_course.login(account_data['email'], account_data['password'])
    if not result['success']:
        response['success'] = False
        response['errorMessage'] = result['message']
        return response

    # Проходимся по всем модулям, урокам, материалам и создаём их
    for name in courses.keys():
        if courses[name][1] == 'module':
            root_module = _create_or_get_root_module(user=user, name=name)
            _parsing_dict(user, get_course, root_module, courses[name][0], root_module)
        else:
            print('Так не допустимо', courses)
            response['success'] = False
            response['errorMessage'] = 'Так не допустимо'
            return response
    return response


def _parsing_dict(user, get_course, parent, js, root_module):
    """Рекурсивно создаёт модули и уроки в соответствии с иерархией"""
    for name in js.keys():
        # Если текущий тип это модуль, то создаем его
        if js[name][1] == 'module':
            module = _create_or_get_module(name=name, parent=parent, root_module=root_module)
            # Обращаемся к этой же функции, но на одну ступень ниже, пока не дойдем до конца иерархии
            _parsing_dict(user, get_course, module, js[name][0], root_module)
        # Если текущий тип это урок, то создаем урок
        else:
            message = _create_lesson(get_course,
                                     url=js[name][0],
                                     name=name,
                                     parent_module=parent,
                                     root_module=root_module,
                                     user=user)

            if message != '':
                # TODO: Если загрузить урок не удалось
                print(message)
                pass


def _create_lesson(get_course, url, name, parent_module, root_module, user) -> str:
    """Получает информацию об уроке из ссылки url,
     добавляет этот урок в таблицу,
     запускает параллельные задачи tasks на сохранение фото, видео, аудио и файлов"""

    # Получаем информацию из урока
    result = get_course.get_info_from_lesson(url)
    if not result['success']:
        return result['message']

    information = result['data']  # Сохраняем информацию в переменную
    # Добавляем урок в таблицу Lesson
    lesson = Lesson.objects.create(name=name,
                                   module=parent_module,
                                   description=information['description'],
                                   text=information['text'],
                                   root_module=root_module)
    # Запускаем параллельные задачи tasks
    # Для фотографий
    for image in information['images']:
        task_id = materials.tasks.add_image_to_lesson.delay(lesson.pk, image).id
        UserTaskLink.objects.create(user=user, task_id=task_id)

    # Для видео
    for video in information['videos']:
        if video['type'] == 'youtube':
            task_id = materials.tasks.add_video_to_lesson.delay(lesson.pk, video['url'], VideoType.YOUTUBE)
            UserTaskLink.objects.create(user=user, task_id=task_id)
        elif video['type'] == 'm3u8':
            task_id = materials.tasks.add_video_to_lesson.delay(lesson.pk, video['url'], VideoType.M3U8)
            UserTaskLink.objects.create(user=user, task_id=task_id)

    # Для аудио
    for audio in information['audios']:
        task_id = materials.tasks.add_audio_to_lesson.delay(lesson.pk, audio)
        UserTaskLink.objects.create(user=user, task_id=task_id)

    # Для файлов
    for file in information['files']:
        task_id = materials.tasks.add_file_to_lesson.delay(lesson.pk, file)
        UserTaskLink.objects.create(user=user, task_id=task_id)

    return ''


def _check_variables_on_parameters(parameters, variables_name: list) -> bool:
    """Проверяет названия переменных на наличие в параметрах parameters"""
    for name in variables_name:
        if name not in parameters:
            return False
    return True


def _get_host_from_url(url) -> str:
    """Возвращает хост из ссылки url"""
    if 'http://' in url:
        url = url.replace('http://', '')
    elif 'https://' in url:
        url = url.replace('https://', '')
    return url.split('/')[0]


def _create_or_get_module(name, parent, root_module) -> Module:
    # Получаем уже созданный модуль с таким же названием
    module = Module.objects.filter(name=name, parent=parent, root_module=root_module, is_root=False).first()

    # Если такого модуля нет, то создаём его
    if not module:
        module = Module.objects.create(name=name, parent=parent, root_module=root_module, is_root=False)

    return module


def _create_or_get_root_module(user, name) -> Module:
    """Создает новый корневой модуль, если с таким названием нет у пользователя, а если уже есть,
     то возвращаем старый модуль"""

    module = Module.objects.filter(name=name, is_root=True).first()  # Получаем уже созданный модуль с таким названием
    if not module:
        # Если такого модуля нет, то создаем его и добавляем связь между пользователем и корневым модулем
        module = Module.objects.create(name=name, is_root=True)
        UserRootModuleLink.objects.create(user=user, module=module, is_favorite=False, is_watched=False, is_my=True)
    else:
        # Если корневой модуль с таким-же названием есть, то проверяем этот модуль пользователя
        if not UserRootModuleLink.objects.filter(user=user, module=module, is_my=True).first():
            # Если корневой модуль не пользователя, тогда создаем новый модуль и отмечаем,
            # что этот модуль создал пользователь
            module = Module.objects.create(name=name, is_root=True)
            UserRootModuleLink.objects.create(user=user, module=module, is_favorite=False, is_watched=False, is_my=True)

    return module
