import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from getCourse import GetCourse
from users.models import UserModuleLink, UserLessonLink, UserTaskLink
from .models import Module, Lesson
import materials.tasks
from materials.models import VideoType


@login_required
def my(request):
    user = request.user
    context = {}

    mass = []
    for user_module_link in UserModuleLink.objects.filter(user=user):
        if not user_module_link.module.is_root:
            continue
        module = user_module_link.module

        cur = {
            'id': str(module.id),
            'name': module.name,
            'is_watched': user_module_link.is_watched
        }
        mass.append(cur)

    context['courses'] = mass
    return render(request, 'courses/my.html', context=context)


def show_module(request, id):
    user = request.user
    context = {}

    mass = []
    for module in Module.objects.filter(module=id):
        cur = {
            'id': str(module.id),
            'name': module.name
        }
        mass.append(cur)
    context['modules'] = mass

    mass = []
    for lesson in Lesson.objects.filter(module=id):
        user_lesson_link = UserLessonLink.objects.filter(user=user, lesson=lesson).first()
        if user_lesson_link is None:
            is_watched = False
        else:
            is_watched = user_lesson_link.is_watched

        cur = {
            'id': str(lesson.pk),
            'name': lesson.name,
            'description': lesson.description,
            'is_watched': is_watched
        }
        mass.append(cur)
    context['lessons'] = mass

    return render(request, 'courses/module.html', context=context)


def show_lesson(request, id):
    user = request.user
    context = {'lesson': {}}

    lesson = Lesson.objects.get(pk=id)
    user_lesson_link = UserLessonLink.objects.get(user=user, lesson=lesson)

    context['lesson']['watched'] = user_lesson_link.is_watched
    context['lesson']['name'] = lesson.name
    context['lesson']['text'] = lesson.text.decode('utf-8')

    return render(request, 'courses/lesson.html', context=context)


@login_required
def add(request):
    return render(request, 'courses/add.html')


@login_required
def list(request):
    if request.method == 'GET':
        return HttpResponse(json.dumps(_get_list(request)))
    elif request.method == 'POST':
        return _post_list(request)
    else:
        js = {'success': True, 'data': {}, 'errorMessage': 'Данный метод не поддерживается'}
        return HttpResponse(json.dumps(js))


@login_required
def _post_list(request):
    js = {'success': True, 'data': {}, 'errorMessage': ''}

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    account_data = body['account']
    courses = body['data']

    if 'http://' in account_data['url']:
        url = account_data['url'].replace('http://', '')
    elif 'https://' in account_data['url']:
        url = account_data['url'].replace('https://', '')
    else:
        url = account_data['url']
    host = url.split('/')[0]

    get_course = GetCourse(host)
    res = get_course.login(account_data['email'], account_data['password'])

    if res[0]:
        for name in courses.keys():
            if courses[name][1] == 'module':
                module = Module.objects.create(name=name, is_root=True)
                UserModuleLink.objects.create(user=request.user, module=module)
                parse_list(request.user, get_course, module, courses[name][0])
            else:
                print('Так не допустимо', courses)
                js['success'] = False
                js['errorMessage'] = 'Так не допустимо'
                return HttpResponse(json.dumps(js))
        return HttpResponse(json.dumps(js))
    else:
        js['success'] = False
        js['errorMessage'] = res[1]
        return HttpResponse(json.dumps(js))


def parse_list(user, get_course, parent, js):
    for name in js.keys():
        if js[name][1] == 'module':
            module = Module.objects.create(name=name, parent=parent, is_root=False)
            UserModuleLink.objects.create(user=user, module=module)
            parse_list(user, get_course, module, js[name][0])
        else:
            result = get_course.get_info_from_lesson(js[name][0])
            if not result[0]:
                continue
            information = result[1]
            lesson = Lesson.objects.create(name=name,
                                           module=parent,
                                           description=information['description'],
                                           text=information['text'])

            UserLessonLink.objects.create(user=user, lesson=lesson)

            for image in information['images']:
                image = image.replace('https:////', 'https://')

                task_id = materials.tasks.add_image_to_lesson.delay(lesson.pk, image).id
                UserTaskLink.objects.create(user=user, task_id=task_id)

            for video in information['videos']:
                if video['type'] == 'youtube':
                    task_id = materials.tasks.add_video_to_lesson.delay(lesson.pk, video['url'], VideoType.YOUTUBE)
                    UserTaskLink.objects.create(user=user, task_id=task_id)
                elif video['type'] == 'm3u8':
                    task_id = materials.tasks.add_video_to_lesson.delay(lesson.pk, video['url'], VideoType.M3U8)
                    UserTaskLink.objects.create(user=user, task_id=task_id)
                else:
                    print('Неизвестный тип', video)

            for audio in information['audio']:
                audio = audio.replace('https:////', 'https://')

                task_id = materials.tasks.add_audio_to_lesson.delay(lesson.pk, audio)
                UserTaskLink.objects.create(user=user, task_id=task_id)


def _get_list(request):
    js = {'success': True, 'data': {}, 'errorMessage': ''}
    response = request.GET

    if 'url' not in response or 'email' not in response or 'password' not in response:
        js['success'] = False
        js['errorMessage'] = 'url, email, password не указаны'
        return HttpResponse(json.dumps(js))

    url: str = response['url']
    email: str = response['email']
    password: str = response['password']

    if 'http://' in url:
        url = url.replace('http://', '')
    elif 'https://' in url:
        url = url.replace('https://', '')
    host = url.split('/')[0]

    get_course = GetCourse(host)
    res = get_course.login(email, password)
    if not res[0]:
        js['success'] = False
        js['errorMessage'] = res[1]
        return HttpResponse(json.dumps(js))

    ls = get_course.get_all_trenings()
    js['data'] = ls
    return js
