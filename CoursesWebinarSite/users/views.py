from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from webinars.models import Webinar
from django.db.utils import IntegrityError


def login_page(request):
    if request.method == "GET":
        return render(request, 'authorization/login.html', context={'alert': ''})
    elif request.method == "POST":
        response = request.POST
        username = response['username']
        password = response['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        return render(request, 'authorization/login.html', context={'alert': 'Неверное имя пользователя или пароль!'})


def signup(request):
    if request.method == "GET":
        return render(request, 'authorization/registration.html', context={'alert': ''})
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
            return render(request, 'authorization/registration.html',
                          context={'alert': 'Данное имя пользователя уже занято!'})
    else:
        raise Http404(f'Ошибка! Неверный запрос: {request.method}')


@login_required(login_url="/login")
def logout_user(request):
    logout(request)
    return redirect('/')


@login_required(login_url="/login")
def profile(request):
    user = request.user

    if user.first_name != '':
        name = user.first_name
    else:
        name = user.username

    full_name = f'{user.first_name} {user.last_name}'
    email = user.email
    return render(request, 'profile.html',
                  context={'username': user.username, 'full_name': full_name, 'email': email, 'name': name})
