from celery.decorators import task

from .ml_modules.core import *
from .models import Submissions_Demo

@task
def add(x, y):
    return x + y

@task
def new_ml_task(task_id, task_type, train_data, test_data, label, feat_sel, estimator, cv_type):
    Submissions_Demo.objects.filter(task_id=id).update(task_status='Running')
    try:
        test_task(task_id, task_type, train_data, test_data, label, feat_sel, estimator, cv_type)
        Submissions_Demo.objects.filter(task_id=id).update(task_status='Finished')
    except:
        Submissions_Demo.objects.filter(task_id=id).update(task_status='Failed')
    return