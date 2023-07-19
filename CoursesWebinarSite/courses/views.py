import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from getCourse import GetCourse
from users.models import UserModuleLink, UserLessonLink
from .models import Module, Material, Lesson, MaterialType
import manage_files


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

    context['courses'] = mass
    return render(request, 'courses/my.html', context=context)

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
            information = get_course.get_info_from_lesson(js[name][0])
            lesson = Lesson.objects.create(name=information['title'],
                                           module=parent,
                                           description=information['description'],
                                           text=information['text'])

            UserLessonLink.objects.create(user=user, lesson=lesson)

            for image in information['images']:
                image = image.replace('https:////', 'https://')
                print('Скачивается фото', image)

                materal = Material.objects.order_by('-id').first()
                if materal:
                    next_id = materal.id + 1
                else:
                    next_id = 0

                url = manage_files.save_file('courses', next_id, image)
                Material.objects.create(name='', url=url, lesson=lesson, type=MaterialType.IMAGE)

            for video in information['videos']:
                print('Сохраняется видео', video)

                materal = Material.objects.order_by('-id').first()
                if materal:
                    next_id = materal.id + 1
                else:
                    next_id = 0

                if video['type'] == 'youtube':
                    url = manage_files.save_youtube_video('courses', next_id, video['url'])
                elif video['type'] == 'm3u8':
                    url = manage_files.save_m3u8_video('courses', next_id, video['url'])
                else:
                    url = video['url']
                    print('Неизвестный тип', video)

                Material.objects.create(name='', url=url, lesson=lesson, type=MaterialType.VIDEO)

            for audio in information['audio']:
                print('Скачивается аудио', audio)

                audio = audio.replace('https:////', 'https://')

                materal = Material.objects.order_by('-id').first()
                if materal:
                    next_id = materal.id + 1
                else:
                    next_id = 0

                url = manage_files.save_file('courses', next_id, audio)
                Material.objects.create(name='', url=url, lesson=lesson, type=MaterialType.AUDIO)


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
