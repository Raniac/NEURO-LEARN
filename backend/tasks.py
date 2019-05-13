from celery.decorators import task

from .ml_modules.core import *

@task
def add(x, y):
    return x + y

@task
def new_ml_task():
    test_task()
    return