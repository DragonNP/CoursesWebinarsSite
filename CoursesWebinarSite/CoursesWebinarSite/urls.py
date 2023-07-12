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
from django.urls import path
from home import views as home
from webinars import views as webinars
from user import views as user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.index),
    path('profile', user.profile),
    path('login', user.login_page),
    path('signup', user.signup),
    path('logout', user.logout_user),
    path('webinars', webinars.my),
    path('webinar/add', webinars.add),
    path('webinar/<str:id>', webinars.show),
    path('webinar/remove/<str:id>', webinars.remove)
]
