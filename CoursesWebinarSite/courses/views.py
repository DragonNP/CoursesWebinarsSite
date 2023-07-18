import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from getCourse import GetCourse


@login_required
def my(request):
    user = request.user
    context = {}

    # mass = []
    # for user_webinar_link in UserWebinarLink.objects.filter(user=user, is_my=True):
    #     webinar = user_webinar_link.webinar
    #
    #     web = [webinar.id, webinar.name]
    #
    #     if webinar.description != '':
    #         web.append(webinar.description)
    #     else:
    #         web.append('')
    #
    #     web.append(webinar.format_date(is_month_name=False))
    #     web.append(user_webinar_link.is_watched)
    #
    #     mass.append(web)
    #
    # context['webinars'] = mass
    return render(request, 'courses/my.html', context=context)


@login_required
def add(request):
    return render(request, 'courses/add.html')


@login_required
def get_list(request):
    js = {'success': True, 'data': {}, 'errorMessage': ''}

    if request.method != 'GET':
        js['success'] = False
        js['errorMessage'] = 'Данный метод не поддерживается'
        return HttpResponse(json.dumps(js))

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
    return HttpResponse(json.dumps(js))
