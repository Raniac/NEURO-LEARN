# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Book(models.Model):
    book_name = models.CharField(max_length=64)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.book_name

class Submissions_Demo(models.Model):
    task_id = models.CharField(max_length=64, unique=True)
    task_name = models.CharField(max_length=64)
    task_type = models.CharField(max_length=64)
    project_name = models.CharField(max_length=64)
    train_data = models.CharField(max_length=1024)
    enable_test = models.BooleanField()
    test_data = models.CharField(max_length=1024)
    label = models.CharField(max_length=64)
    feat_sel = models.CharField(max_length=64)
    estimator = models.CharField(max_length=64)
    cv_type = models.CharField(max_length=64)
    note = models.CharField(max_length=64)
    verbose = models.BooleanField()
    task_status = models.CharField(max_length=64)
    task_result = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.task_id

class Submissions_SA_Demo(models.Model):
    task_id = models.CharField(max_length=64, unique=True)
    task_name = models.CharField(max_length=64)
    task_type = models.CharField(max_length=64)
    project_name = models.CharField(max_length=64)
    test_var_data_x = models.CharField(max_length=1024)
    group_var_data_y = models.CharField(max_length=1024)
    note = models.CharField(max_length=64)
    verbose = models.BooleanField()
    task_status = models.CharField(max_length=64)
    task_result = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.task_id

class Projects_Demo(models.Model):
    project_id = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=128, unique=True)
    introduction = models.TextField(max_length=4096)
    methods = models.TextField(max_length=4096)
    flowchart_url = models.CharField(max_length=128)
    workflow_templates_url = models.CharField(max_length=128)
    data_templates_url = models.CharField(max_length=128)

    def __unicode__(self):
        return self.project_id

class Data_Demo(models.Model):
    data_id = models.CharField(max_length=64, unique=True)
    data_name = models.CharField(max_length=64, unique=True)
    data_path = models.CharField(max_length=128)

    def __unicode__(self):
        return self.task_id

class User_Demo(models.Model):
    user_id = models.CharField(max_length=64, unique=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)

    def __unicode__(self):
        return self.user_id