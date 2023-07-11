from django.db import models


class Webinar(models.Model):
    name = models.CharField(max_length=150, blank=False)
    author = models.CharField(max_length=25, blank=False)
    date = models.DateField(blank=False)
    url = models.URLField(max_length=150, blank=False)

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=150, blank=False)
    url = models.URLField(max_length=150, blank=False)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)


class Music(models.Model):
    url = models.URLField(max_length=150, blank=False)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)
