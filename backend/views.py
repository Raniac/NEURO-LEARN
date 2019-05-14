from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django import forms
import requests
import json
import os
import time

from .models import Book
from .models import Submissions_Demo
from .models import Data_Demo

from .tasks import *

# Create your views here.
@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def show_books(request):
    response = {}
    try:
        books = Book.objects.filter()
        response['list']  = json.loads(serializers.serialize("json", books))
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["POST"])
def new_task(request):
    response = {}
    postBody = json.loads(request.body)
    try:
        task_id = time.strftime('%Y%m%d%H%M%S')
        task_name=postBody.get('task_name')
        task_type=postBody.get('task_type')
        project_name=postBody.get('project_name')
        train_data=postBody.get('train_data')
        test_data=postBody.get('test_data')
        label=postBody.get('label')
        feat_sel=postBody.get('feat_sel')
        estimator=postBody.get('estimator')
        cv_type=postBody.get('cv_type')
        note=postBody.get('note')
        verbose=postBody.get('verbose')

        task = Submissions_Demo(
            task_id=task_id,
            task_name=task_name,
            task_type=task_type,
            project_name=project_name,
            train_data=train_data,
            test_data=test_data,
            label=label,
            feat_sel=feat_sel,
            estimator=estimator,
            cv_type=cv_type,
            note=note,
            verbose=verbose,
            task_status='Submitted',
            task_result=''
        )
        task.save()

        # # create new celery task
        new_ml_task.delay(
            task_id,
            task_type,
            train_data,
            test_data,
            label,
            feat_sel,
            estimator,
            cv_type
        )

        response['post_body'] = postBody
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['post_body'] = postBody
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def show_submissions(request):
    response = {}
    try:
        submissions = Submissions_Demo.objects.filter()
        response['list']  = json.loads(serializers.serialize("json", submissions))
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(['POST'])
def upload_data(request):
    response = {}
    try:
        data_file = request.FILES.get('datafile')
        if data_file.name not in os.listdir('data/'):
            data = Data_Demo()
            data_id = time.strftime('%Y%m%d%H%M%S')
            data.data_id = data_id
            data.data_name = data_file.name[:-4]
            data.data_path = handle_uploaded_file(data_file)
            data.save()
            response['msg'] = 'success'
        else:
            response['msg'] = 'existed'
        
        response['error_num'] = 0
    
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

def handle_uploaded_file(f):
    try:
        path = 'data/'
        if not os.path.exists(path):
            os.makedirs(path)
        
        file_name = str(path + f.name)
        destination = open(file_name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
    
    except Exception as e:
        print(e)
    return file_name

@require_http_methods(["GET"])
def show_data(request):
    response = {}
    try:
        data = Data_Demo.objects.filter()
        response['list']  = json.loads(serializers.serialize("json", data))
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)