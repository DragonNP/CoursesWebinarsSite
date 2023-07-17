from django.db import models


class Module(models.Model):
    name = models.CharField(max_length=150, blank=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True)
    is_parent = models.BooleanField()


class Lesson(models.Model):
    name = models.CharField(max_length=150, blank=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=False)
    text = models.CharField(max_length=2500, blank=False)


class Material(models.Model):
    name = models.CharField(max_length=150, blank=False)
    url = models.URLField(max_length=150, blank=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
