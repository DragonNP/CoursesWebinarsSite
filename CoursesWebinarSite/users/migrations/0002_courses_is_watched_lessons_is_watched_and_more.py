# Generated by Django 4.2.3 on 2023-07-12 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='is_watched',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lessons',
            name='is_watched',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='webinars',
            name='is_watched',
            field=models.BooleanField(default=False),
        ),
    ]
