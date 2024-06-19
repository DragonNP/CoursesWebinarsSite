import uuid

from django.db import models
from django.contrib.auth.models import User
from webinars.models import Webinar
from courses.models import Module, Lesson


class UserTaskLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=50)


class UserWebinarLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)
    is_my = models.BooleanField(default=False)
    is_watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'webinar')


class UserRootModuleLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)
    is_watched = models.BooleanField(default=False)
    is_my = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'module')


class UserLessonLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'lesson')
