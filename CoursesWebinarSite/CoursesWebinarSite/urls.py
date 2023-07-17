"""
URL configuration for CoursesWebinarSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from courses import views as courses
from home import views as home
from webinars import views as webinars
from users import views as user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.index),
]

# URL для курсов
urlpatterns += [
    path('courses/my/', courses.my, name='my_courses'),
    path('courses/add/', courses.add, name='add_course'),
    path('courses/prepeare_add', courses.prepeare_add, name='123')
]

# URL для вебинаров
urlpatterns += [
    path('webinars/', webinars.all_webinars, name='webinars'),
    path('webinars/my/', webinars.my, name='my_webinars'),
    path('webinars/add/', webinars.add, name='add_webinar'),
    path('webinars/<str:id>/', webinars.show, name='show_webinar'),
    path('webinars/<str:id>/remove/', webinars.remove, name='remove_webinar'),
    path('webinars/<str:id>/make/watched/', webinars.make_watched, name='make_watched_webinar'),
    path('webinars/<str:id>/make/no_watched/', webinars.make_no_watched, name='make_no_watched_webinar')
]

# URL для аккаунта
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', user.profile, name='my_profile'),
    path('accounts/registration/', user.registration, name='registration')
]
"""
accounts/ login/ [name='login']
accounts/ logout/ [name='logout']
accounts/ password_change/ [name='password_change']
accounts/ password_change/done/ [name='password_change_done']
accounts/ password_reset/ [name='password_reset']
accounts/ password_reset/done/ [name='password_reset_done']
accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/ reset/done/ [name='password_reset_complete']
"""
