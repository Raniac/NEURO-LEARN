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
    task_id = models.CharField(max_length=64)
    task_name = models.CharField(max_length=64)
    task_type = models.CharField(max_length=64)
    train_data = models.CharField(max_length=64)
    test_data = models.CharField(max_length=64)
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

class Data_Demo(models.Model):
    data_id = models.CharField(max_length=64)
    data_name = models.CharField(max_length=64)
    data_path = models.CharField(max_length=128)

    def __unicode__(self):
        return self.task_id