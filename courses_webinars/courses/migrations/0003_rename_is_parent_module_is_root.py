# Generated by Django 4.2.3 on 2023-07-17 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_module_parent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='module',
            old_name='is_parent',
            new_name='is_root',
        ),
    ]
