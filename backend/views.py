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

from .models import Book
from .models import Submissions_Demo
from .models import Data_Demo

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
        task = Submissions_Demo(
            task_name=postBody.get('task_name'),
            task_type=postBody.get('task_type'),
            train_data=postBody.get('train_data'),
            test_data=postBody.get('test_data'),
            label=postBody.get('label'),
            feat_sel=postBody.get('feat_sel'),
            estimator=postBody.get('estimator'),
            cv_type=postBody.get('cv_type'),
            note=postBody.get('note'),
            verbose=postBody.get('verbose'),
            task_status='Submitted',
            task_result=''
        )
        task.save()
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

# class DataForm(forms.Form):
#     data_name = forms.CharField()
#     data_path = forms.FileField()

@require_http_methods(['POST'])
def upload_data(request):
    response = {}
    try:
        # uf = DataForm(request.POST, request.FILES)
        
        # data_name = uf.get('data_name')
        # data_path = uf.get('data_path')
        obj = request.FILES.get('test')
        data = Data_Demo()
        data.data_name = 'test'
        data.data_path = obj.name
        data.save()
        handle_uploaded_file(obj)
        
        response['msg'] = 'success'
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
        else:
            file_name = str(path + f.name)
            destination = open(file_name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    except Exception as e:
        print(e)
    return f.name, path