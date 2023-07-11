from django.db import models
from django.contrib.auth.models import User


class Webinar(models.Model):
    name = models.CharField(max_length=150, blank=False)
    author = models.CharField(max_length=25, blank=False)
    description = models.CharField(max_length=250, blank=True)
    date = models.DateField(blank=False)
    url = models.URLField(max_length=150, blank=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Photo(models.Model):
    url = models.URLField(max_length=150, blank=False)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)


class File(models.Model):
    name = models.CharField(max_length=150, blank=False)
    url = models.URLField(max_length=150, blank=False)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)


class Music(models.Model):
    url = models.URLField(max_length=150, blank=False)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)
