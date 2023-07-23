from MySQLdb import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect

from .models import UserTaskLink


def registration(request):
    if request.method == "GET":
        return render(request, 'registration/registration.html', context={'alert': ''})
    elif request.method == "POST":
        response = request.POST
        username = response['username']
        firstname = response['firstname']
        lastname = response['lastname']
        email = response['email']
        password = response['password']

        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname,
                                            last_name=lastname)
            if user is not None:
                login(request, user)
            return redirect('/')
        except IntegrityError as e:
            return render(request, 'registration/registration.html',
                          context={'alert': 'Данное имя пользователя уже занято!'})
    else:
        raise Http404(f'Ошибка! Неверный запрос: {request.method}')


@login_required
def profile(request):
    user = request.user

    if user.first_name != '':
        name = user.first_name
    else:
        name = user.username

    full_name = f'{user.first_name} {user.last_name}'
    email = user.email
    return render(request, 'user_profile.html',
                  context={'username': user.username, 'full_name': full_name, 'email': email, 'name': name})


@login_required
def get_tasks(request):
    user = request.user

    response = []
    user_tasks = UserTaskLink.objects.filter(user=user)
    for user_task in user_tasks:
        response.append(user_task.task_id)
    return HttpResponse(response)

