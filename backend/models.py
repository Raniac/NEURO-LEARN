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
    project_name = models.CharField(max_length=64)
    train_data = models.CharField(max_length=1024)
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

class Data_Demo(models.Model):
    data_id = models.CharField(max_length=64)
    data_name = models.CharField(max_length=64)
    data_path = models.CharField(max_length=128)

    def __unicode__(self):
        return self.task_id

# class UserInfo(models.Model):
#     user_type_choices = (
#         (1, 'Admin'),
#         (2, 'User')
#     )
#     user_type = models.IntegerField(choices=user_type_choices)
#     username = models.CharField(max_length=32, unique=True)
#     password = models.CharField(max_length=64)

# class UserToken(models.Model):
#     user = models.OneToOneField(UserInfo, null=True)
#     token = models.CharField(max_length=64)