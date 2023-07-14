from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=150, blank=False, unique=True)


class Webinar(models.Model):
    name = models.CharField(max_length=150, blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, blank=True)
    date = models.DateField(blank=False)
    url = models.URLField(max_length=150, blank=False)

    def __str__(self):
        return self.name

    def format_date(self, is_month_name=True):
        year, m, day = str(self.date).split('-')
        if is_month_name:
            month = {'01': 'января',
                     '02': 'февраля',
                     '03': 'марта',
                     '04': 'апреля',
                     '05': 'мая',
                     '06': 'июня',
                     '07': 'июля',
                     '08': 'августа',
                     '09': 'сентября',
                     '10': 'октября',
                     '11': 'ноября',
                     '12': 'декабря'}

            return f'{day} {month[m]} {year}'
        return f'{day}.{m}.{year}'


class Photo(models.Model):
    url = models.URLField(max_length=300, blank=False)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)


class File(models.Model):
    name = models.CharField(max_length=150, blank=False)
    url = models.URLField(max_length=300, blank=False)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)


class Music(models.Model):
    url = models.URLField(max_length=300, blank=False)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)
