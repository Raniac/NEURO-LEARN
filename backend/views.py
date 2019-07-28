from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django import forms
from django.middleware.csrf import get_token, rotate_token

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import permissions

import uuid

from PIL import Image
import pandas as pd
import requests
import json
import os
import io
import time

from .models import Book, Projects_Demo, Submissions_Demo, Submissions_SA_Demo, Data_Demo, User_Demo

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

@require_http_methods(["GET", "POST"])
def user_register(request):
    response_content = {}
    response = HttpResponse()
    try:
        postBody = json.loads(request.body)
        user_id = 'USER' + time.strftime('%Y%m%d%H%M%S')
        username=postBody.get('username')
        password=postBody.get('password')

        user = User_Demo(
            user_id=user_id,
            username=username,
            password=password
        )
        user.save()
        
        response_content['post_body'] = postBody
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1
    
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET,POST"
    response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def user_login(request):
    response_content = {}
    response = HttpResponse()
    try:
        username = request.GET.get('username')
        password = request.GET.get('password')
        userobj = User_Demo.objects.filter(username=username, password=password).first()

        if userobj:
            response_content['msg'] = 'Correct password!'
            response_content['username'] = username

            sessionid = str(uuid.uuid3(uuid.NAMESPACE_URL, username))
            response.set_cookie('sessionid', sessionid, expires=60000, path='/', httponly=False)
            response.set_cookie('username', username, expires=60000, path='/', httponly=False)
            response.set_cookie('user_id', userobj.user_id, expires=60000, path='/', httponly=False)
            response_content['sessionid'] = sessionid

            print(sessionid)
            
            response_content['error_num'] = 0
        else:
            response_content['msg'] = 'Wrong password!'
            response_content['error_num'] = 1
    except  Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET,POST"
    response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def show_project_overview(request):
    response_content = {}
    response = HttpResponse()
    try:
        projects = Projects_Demo.objects.filter()
        print(projects)
        response_content['list']  = json.loads(serializers.serialize("json", projects))
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except  Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET,POST"
    response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def overview_submissions(request):
    response_content = {}
    response = HttpResponse()
    try:
        print(request.COOKIES.get('sessionid'))
        print(request.COOKIES.get('username'))
        print(request.COOKIES.get('user_id'))

        analysis_type = request.GET.get('analysis_type')
        if analysis_type == 'Machine Learning':
            submissions = Submissions_Demo.objects.filter().order_by('-id')[:4]
            response_content['list']  = json.loads(serializers.serialize("json", submissions))
        elif analysis_type == 'Statistical Analysis':
            submissions = Submissions_SA_Demo.objects.filter().order_by('-id')[:4]
            response_content['list']  = json.loads(serializers.serialize("json", submissions))

        total_ml = Submissions_Demo.objects.filter() 
        total_sa = Submissions_SA_Demo.objects.filter()
        response_content['total_num'] = len(total_ml) + len(total_sa)
        submitted_ml = Submissions_Demo.objects.filter(task_status='Submitted')
        submitted_sa = Submissions_SA_Demo.objects.filter(task_status='Submitted')
        response_content['submitted_num'] = len(submitted_ml) + len(submitted_sa)
        running_ml = Submissions_Demo.objects.filter(task_status='Running') 
        running_sa = Submissions_SA_Demo.objects.filter(task_status='Running')
        response_content['running_num'] = len(running_ml) + len(running_sa)
        finished_ml = Submissions_Demo.objects.filter(task_status='Finished') 
        finished_sa = Submissions_SA_Demo.objects.filter(task_status='Finished')
        response_content['finished_num'] = len(finished_ml) + len(finished_sa)
        failed_ml = Submissions_Demo.objects.filter(task_status='Failed') 
        failed_sa = Submissions_SA_Demo.objects.filter(task_status='Failed')
        response_content['failed_num'] = len(failed_ml) + len(failed_sa)

        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except  Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET,POST"
    response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET", "POST"])
def new_task(request):
    response = HttpResponse()
    response_content = {}
    try:
        if request.method == 'GET':
            get_token(request)
        if request.method == 'POST':
            postBody = json.loads(request.body)
            task_id = 'TASK' + time.strftime('%Y%m%d%H%M%S')
            task_name=postBody.get('task_name')
            task_type=postBody.get('task_type')
            project_name=postBody.get('project_name')
            train_data=postBody.get('train_data')
            enable_test=postBody.get('enable_test')
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
                enable_test=enable_test,
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

            # create new celery task
            new_ml_celery_task.delay(
                taskid=task_id,
                tasktype=task_type,
                traindata=train_data,
                enabletest=enable_test,
                testdata=test_data,
                label=label,
                featsel=feat_sel,
                estimator=estimator,
                cv=cv_type
            )

            response_content['post_body'] = postBody
            response_content['msg'] = 'success'
            response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET,POST"
    response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET", "POST"])
def new_sa_task(request):
    response = HttpResponse()
    response_content = {}
    try:
        if request.method == 'GET':
            get_token(request)
        if request.method == 'POST':
            postBody = json.loads(request.body)
            task_id = 'TASK' + time.strftime('%Y%m%d%H%M%S')
            task_name=postBody.get('task_name')
            task_type=postBody.get('task_type')
            project_name=postBody.get('project_name')
            test_var_data_x=postBody.get('test_var_data_x')
            group_var_data_y=postBody.get('group_var_data_y')
            note=postBody.get('note')
            verbose=postBody.get('verbose')

            task = Submissions_SA_Demo(
                task_id=task_id,
                task_name=task_name,
                task_type=task_type,
                project_name=project_name,
                test_var_data_x=test_var_data_x,
                group_var_data_y=group_var_data_y,
                note=note,
                verbose=verbose,
                task_status='Submitted',
                task_result=''
            )
            task.save()

            # create new celery task
            new_sa_celery_task.delay(
                taskid=task_id,
                tasktype=task_type,
                testvardatax=test_var_data_x,
                groupvardatay=group_var_data_y
            )

            response_content['post_body'] = postBody
            response_content['msg'] = 'success'
            response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET,POST"
    response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def show_submissions(request):
    response_content = {}
    response = HttpResponse()
    try:
        analysis_type = request.GET.get('analysis_type')
        if analysis_type == 'Machine Learning':
            submissions = Submissions_Demo.objects.filter().order_by('-id')
            print(submissions)
            response_content['list']  = json.loads(serializers.serialize("json", submissions))
        elif analysis_type == "Statistical Analysis":
            submissions = Submissions_SA_Demo.objects.filter().order_by('-id')
            response_content['list']  = json.loads(serializers.serialize("json", submissions))
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except  Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET,POST"
    response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
    response.write(json.dumps(response_content))

    return response

@require_http_methods(['POST'])
def upload_data(request):
    response_content = {}
    response = HttpResponse()
    try:
        data_file = request.FILES.get('datafile')
        if data_file.name not in os.listdir('data/'):
            data = Data_Demo()
            data_id = 'DATA' + time.strftime('%Y%m%d%H%M%S')
            data.data_id = data_id
            data.data_name = data_file.name[:-4]
            data.data_path = handle_uploaded_file(data_file)
            data.save()
            response_content['msg'] = 'success'
            response_content['dataid'] = data_id
        else:
            response_content['msg'] = 'existed'
        
        response_content['error_num'] = 0
    
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "PUT,POST,GET,DELETE,OPTIONS"
    response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token,X-Requested-With"
    response.write(json.dumps(response_content))

    return response

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
    response_content = {}
    response = HttpResponse()
    try:
        project_id = request.GET.get('project_id')
        print(project_id)
        data = Data_Demo.objects.filter().order_by('-id')
        response_content['list']  = json.loads(serializers.serialize("json", data))
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except  Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET,POST"
    response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def show_results(request):
    response_content = {}
    response = HttpResponse()
    try:
        task_id = request.GET.get('task_id')
        analysis_type = request.GET.get('analysis_type')
        
        if analysis_type == 'Machine Learning':
            result_table = pd.read_csv('results/' + task_id + '/results.csv', encoding='gbk')
            result_json = result_table.to_json(orient='records')
            response_content['list']  = json.loads(result_json)

            task_info = Submissions_Demo.objects.filter(task_id=task_id)
            response_content['info']  = json.loads(serializers.serialize("json", task_info))

            img_list = []
            response_content['got_weights'] = 0
            for filename in os.listdir('results/' + task_id):
                if filename[-4:] == '.png':
                    img_list.append(filename[:-4])
                if filename == 'feature_weights.csv':
                    response_content['got_weights'] = 1
            response_content['img_list'] = img_list

        elif analysis_type == 'Statistical Analysis':
            task_info = Submissions_SA_Demo.objects.filter(task_id=task_id)
            response_content['info']  = json.loads(serializers.serialize("json", task_info))

        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except  Exception as e:
        response_content['msg'] = json.dumps(Submissions_Demo.objects.get(task_id=task_id).task_result)
        response_content['error_num'] = 1

    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET,POST"
    response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def show_img(request):
    response = {}
    task_id = request.GET.get('task_id')
    img_name = request.GET.get('img_name')

    buf = io.BytesIO()
    img = Image.open('results/' + task_id + '/' + img_name + '.png')
    img.save(buf, 'png')

    return HttpResponse(buf.getvalue(), 'image/png')

@require_http_methods(["GET"])
def download_templates(request):
    project_id = request.GET.get('project_id')

    templates_file = open('projects/' + project_id + '/dataset_templates.zip', 'rb')
    response = FileResponse(templates_file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename=\"dataset_templates.zip\"'
    return response

@require_http_methods(["GET"])
def download_workflows(request):
    project_id = request.GET.get('project_id')

    workflows_file = open('projects/' + project_id + '/local_workflows.zip', 'rb')
    response = FileResponse(workflows_file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename=\"local_workflows.zip\"'
    return response

@require_http_methods(["GET"])
def download_feature_weights(request):
    task_id = request.GET.get('task_id')
    feature_weights_file = open('results/' + task_id + '/' + 'feature_weights.csv', 'rb')
    
    response = FileResponse(feature_weights_file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename=\"' + task_id + '/' + 'feature_weights.csv\"'
    return response

@require_http_methods(["GET"])
def download_significance_values(request):
    task_id = request.GET.get('task_id')
    significance_file = open('results/' + task_id + '/' + 'significance.csv', 'rb')
    
    response = FileResponse(significance_file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename=\"' + task_id + '/' + 'significance.csv\"'
    return response
