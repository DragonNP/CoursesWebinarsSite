from django.db import models


class MaterialType:
    VIDEO = "VIDEO"
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"

    CHOICES = (
        (VIDEO, "video"),
        (IMAGE, "image"),
        (AUDIO, "audio")
    )


class Module(models.Model):
    name = models.CharField(max_length=150, blank=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    is_root = models.BooleanField(blank=False)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=150, blank=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=True)
    text = models.BinaryField(blank=False)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=150, blank=False)
    url = models.URLField(max_length=150, blank=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    type = models.CharField(max_length=5, choices=MaterialType.CHOICES)

    def __str__(self):
        if self.name != '':
            return self.name
        return self.url
