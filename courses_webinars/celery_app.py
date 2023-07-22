import os
import time

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "courses_webinars.settings")

app = Celery("courses_webinars")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=False)
def debug_task(self):
    time.sleep(10)
    print(f'Request: {self.request!r}')
    return 1
