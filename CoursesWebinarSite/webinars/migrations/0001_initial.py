# Generated by Django 4.2.3 on 2023-07-10 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Webinar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('author', models.CharField(max_length=25)),
                ('date', models.DateField()),
                ('files', models.JSONField(blank=True)),
                ('music', models.JSONField(blank=True)),
            ],
        ),
    ]