# Generated by Django 4.2.3 on 2023-07-19 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_rename_is_parent_module_is_root'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.module'),
        ),
    ]