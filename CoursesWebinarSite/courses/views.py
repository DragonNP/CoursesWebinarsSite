import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from getCourse import GetCourse


def empty(request):
    return redirect('/')


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


def add(request):
    if request.method == 'GET':
        return render(request, 'courses/add.html', context={'alert': ''})
    elif request.method == 'POST':
        response = request.POST
        url: str = response['url']
        email: str = response['email']
        password: str = response['password']

        if 'http://' in url:
            url = url.replace('http://', '')
        elif 'https://' in url:
            url = url.replace('https://', '')
        host = url.split('/')[0]

        return render(request, 'courses/add_show.html',
                      context={'url': f'/courses/prepeare_add?h={host}&e={email}&p={password}'})


def prepeare_add(request):
    response = request.GET
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
        return render(request, 'courses/add.html', context={'alert': res[1]})
    trenings = get_course.get_all_trenings()
    return HttpResponse(json.dumps(trenings))
