import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .services import get_context_for_user_courses, get_context_for_module, get_context_for_lesson, \
    get_list_courses_from_get_course, save_courses


@login_required
def send_user_courses_view(request):
    user = request.user

    context = get_context_for_user_courses(user)

    return render(request, 'courses/my.html', context=context)


@login_required
def send_module_view(request, module_pk):
    user = request.user

    context = get_context_for_module(user, module_pk)

    return render(request, 'courses/module.html', context=context)


@login_required
def send_lesson_view(request, lesson_pk):
    user = request.user

    context = get_context_for_lesson(user, lesson_pk)

    return render(request, 'courses/lesson.html', context=context)


@login_required
def add(request):
    return render(request, 'courses/add.html')


class GetCourseView(View):
    def get(self, request):
        response = get_list_courses_from_get_course(request.GET)
        return HttpResponse(json.dumps(response))

    def post(self, request):
        response = save_courses(request.user, request.body)
        return HttpResponse(json.dumps(response))
