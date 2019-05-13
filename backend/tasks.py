from celery.decorators import task

from .ml_modules.core import *
from .models import Submissions_Demo

@task
def add(x, y):
    return x + y

@task
def new_ml_task(id):
    Submissions_Demo.objects.filter(task_id=id).update(task_status='Running')
    test_task()
    Submissions_Demo.objects.filter(task_id=id).update(task_status='Finished')
    return