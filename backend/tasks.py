from celery.decorators import task

from .ml_modules.core import *
from .sa_modules.core import *

from .models import Submissions, Datasets

import pandas as pd
import traceback
import json

@task
def add(x, y):
    return x + y

@task
def new_ml_celery_task(taskid, tasktype, traindata, enabletest, testdata, label, featsel, estimator, cv):
    # Submissions.objects.filter(task_id=taskid).update(task_status='Running')
    try:
        train_data_queryset = list(Datasets.objects.filter(data_name__in = traindata).values('data_cont'))
        train_data_list = []
        for itm in list(train_data_queryset):
            train_data_list.append(pd.read_json(itm['data_cont']))

        if enabletest:
            test_data_queryset = list(Datasets.objects.filter(data_name__in = testdata).values('data_cont'))
            test_data_list = []
            for jtm in list(test_data_queryset):
                test_data_list.append(pd.read_json(jtm['data_cont']))

        results = ml_task(taskid, tasktype, train_data_list, enabletest, test_data_list, label, featsel, estimator, cv)
        print(type(results))
        results_json = json.dumps(results)
        print(results_json)
        # Submissions.objects.filter(task_id=taskid).update(task_status='Finished')
        # Submissions.objects.filter(task_id=taskid).update(task_result=results_json)
    except Exception as e:
        traceback.print_exc()
        # Submissions.objects.filter(task_id=taskid).update(task_status='Failed')
        # Submissions.objects.filter(task_id=taskid).update(task_result=traceback.format_exc()[-min(1000, len(traceback.format_exc())):])
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