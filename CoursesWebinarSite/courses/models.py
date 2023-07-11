from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=150, blank=False)
    author = models.CharField(max_length=25, blank=False)
    description = models.CharField(max_length=250, blank=True)
    date = models.DateField(blank=False)


class Lesson(models.Model):
    name = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=250, blank=True)
    url = models.URLField(max_length=150, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Material(models.Model):
    name = models.CharField(max_length=150, blank=False)
    url = models.URLField(max_length=150, blank=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
