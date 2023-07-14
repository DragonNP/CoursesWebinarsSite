# Generated by Django 4.2.3 on 2023-07-14 17:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
        ('users', '0005_alter_userwebinarlink_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usercourselink',
            unique_together={('user', 'course')},
        ),
        migrations.AlterUniqueTogether(
            name='userlessonlink',
            unique_together={('user', 'lesson')},
        ),
    ]
