import json

from django.http import HttpResponse
from celery.result import AsyncResult


def get(request, task_id):
    task = AsyncResult(task_id)
    response = {'state': task.state, 'result': task.result}
    return HttpResponse(json.loads(response))

