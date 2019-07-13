from celery.decorators import task

from .ml_modules.core import *
from .models import Submissions_Demo

from .sa_modules.core import *
from .models import Submissions_SA_Demo

import traceback

@task
def add(x, y):
    return x + y

@task
def new_ml_celery_task(taskid, tasktype, traindata, testdata, label, featsel, estimator, cv):
    Submissions_Demo.objects.filter(task_id=taskid).update(task_status='Running')
    try:
        test_task(taskid, tasktype, traindata, testdata, label, featsel, estimator, cv)
        Submissions_Demo.objects.filter(task_id=taskid).update(task_status='Finished')
    except:
        Submissions_Demo.objects.filter(task_id=taskid).update(task_status='Failed')
        Submissions_Demo.objects.filter(task_id=taskid).update(task_result=traceback.format_exc()[-min(1000, len(traceback.format_exc())):])
    return

@task
def new_sa_celery_task(taskid, tasktype, testvardatax, groupvardatay):
    Submissions_SA_Demo.objects.filter(task_id=taskid).update(task_status='Running')
    try:
        test_sa_task(taskid, tasktype, testvardatax, groupvardatay)
        Submissions_SA_Demo.objects.filter(task_id=taskid).update(task_status='Finished')
    except:
        Submissions_SA_Demo.objects.filter(task_id=taskid).update(task_status='Failed')
        Submissions_SA_Demo.objects.filter(task_id=taskid).update(task_result=traceback.format_exc()[-min(1000, len(traceback.format_exc())):])
    return