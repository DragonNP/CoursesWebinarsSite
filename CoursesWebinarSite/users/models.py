from django.db import models
from django.contrib.auth.models import User
from webinars.models import Webinar
from courses.models import Course, Lesson


class Webinars(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)
    is_watched = models.BooleanField(default=False)


class Courses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_watched = models.BooleanField(default=False)


class Lessons(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_watched = models.BooleanField(default=False)
