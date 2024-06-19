from django.db import models
from courses.models import Lesson


class VideoType:
    YOUTUBE = "YOUTUBE"
    M3U8 = "M3U8"


class MaterialType:
    VIDEO = "VIDEO"
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"
    FILE = "FILE"

    CHOICES = (
        (VIDEO, "video"),
        (IMAGE, "image"),
        (AUDIO, "audio"),
        (FILE, "file")
    )


class MaterialLesson(models.Model):
    name = models.CharField(max_length=150, blank=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    type = models.CharField(max_length=5, choices=MaterialType.CHOICES)
    extension = models.CharField(max_length=5)
    is_saved = models.BooleanField(default=False)

    def __str__(self):
        if self.name != '':
            return self.name
        return self.pk
