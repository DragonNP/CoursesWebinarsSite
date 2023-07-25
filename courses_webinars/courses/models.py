from django.db import models


class Module(models.Model):
    name = models.CharField(max_length=150,
                            blank=False)

    parent = models.ForeignKey(to='self',
                               related_name='%(class)s_parent',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)

    root_module = models.ForeignKey(to='self',
                                    related_name='%(class)s_root_module',
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True)

    is_root = models.BooleanField(blank=False)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=150,
                            blank=False)

    module = models.ForeignKey(to=Module,
                               related_name='%(class)s_parent',
                               on_delete=models.CASCADE)

    description = models.CharField(max_length=300,
                                   blank=True)

    text = models.BinaryField(blank=False)

    root_module = models.ForeignKey(to=Module,
                                    related_name='%(class)s_root_module',
                                    on_delete=models.CASCADE,
                                    blank=False)

    def __str__(self):
        return self.name
