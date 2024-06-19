import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "courses_webinars.settings")

app = Celery("courses_webinars")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
