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
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import os
import io
import time
import zipfile
import traceback

# from .models import Book, Projects_Demo, Submissions_Demo, Submissions_SA_Demo, Data_Demo, User_Demo

from .models import Users, Projects, User_Proj_Auth, Datasets, Submissions

from .tasks import *

# Create your views here.
# ==================================================
# Universal APIs
# ==================================================
@require_http_methods(["GET", "POST"])
def user_register(request):
    response_content = {}
    response = HttpResponse()
    try:
        postBody = json.loads(request.body.decode('utf-8'))
        user_id = 'USER' + time.strftime('%Y%m%d%H%M%S')
        username=postBody.get('username')
        password=postBody.get('password')

        user = Users(
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
    
    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def user_login(request):
    response_content = {}
    response = HttpResponse()
    try:
        username = request.GET.get('username')
        password = request.GET.get('password')
        userobj = Users.objects.filter(username=username, password=password).first()

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
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

# ==================================================
# Data Management APIs
# ==================================================
@require_http_methods(["GET"])
def show_project_overview(request):
    response_content = {}
    response = HttpResponse()
    try:
        user_id = request.COOKIES.get('user_id')
        proj_ids = User_Proj_Auth.objects.filter(user_id=user_id).values('proj_id')
        proj_id_list = []
        for itm in proj_ids:
            proj_id_list.append(itm['proj_id'])
        projects = Projects.objects.filter(proj_id__in = proj_id_list)
        response_content['list']  = json.loads(serializers.serialize("json", projects))
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def show_all_projects(request):
    response_content = {}
    response = HttpResponse()
    try:
        projects = Projects.objects.filter()
        response_content['list']  = json.loads(serializers.serialize("json", projects))
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def join_project(request):
    response_content = {}
    response = HttpResponse()
    try:
        proj_id = request.GET.get('proj_id')
        user_id = request.COOKIES.get('user_id')
        if len(User_Proj_Auth.objects.filter(proj_id=proj_id, user_id=user_id)) == 0:
            auth_rec = User_Proj_Auth(
                user_id=user_id,
                proj_id=proj_id
            )
            auth_rec.save()
        else:
            raise Exception('Already joined!')
        
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def quit_project(request):
    response_content = {}
    response = HttpResponse()
    try:
        proj_id = request.GET.get('proj_id')
        user_id = request.COOKIES.get('user_id')
        if len(User_Proj_Auth.objects.filter(proj_id=proj_id, user_id=user_id)) == 1:
            User_Proj_Auth.objects.filter(proj_id=proj_id, user_id=user_id).delete()
        else:
            raise Exception('Something went wrong!')
        
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(['POST'])
def upload_data(request):
    response_content = {}
    response = HttpResponse()
    try:
        proj_id = request.GET.get('proj_id')
        data_file = request.FILES.get('datafile')
        data_id = 'DATA' + time.strftime('%Y%m%d%H%M%S')
        data_name = data_file.name[:-4]
        data_cont = handle_uploaded_file(data_file)

        dataset = Datasets(
            data_id=data_id,
            proj_id=proj_id,
            data_name=data_name,
            data_cont=data_cont
        )
        dataset.save()
        
        response_content['msg'] = 'success'
        response_content['dataid'] = data_id
    
    except Exception as e:
        traceback.print_exc()
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

def handle_uploaded_file(f):
    try:
        file_name = str(f.name)
        destination = open(file_name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        data_content = pd.read_csv(file_name, encoding='utf-8')
        data_json = data_content.to_json()
    
    except Exception as e:
        print(e)
    return data_json

@require_http_methods(["GET"])
def show_data(request):
    response_content = {}
    response = HttpResponse()
    try:
        proj_id = request.GET.get('proj_id')
        data = Datasets.objects.filter(proj_id=proj_id).order_by('-id')
        response_content['list']  = json.loads(serializers.serialize("json", data))
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def delete_data(request):
    response_content = {}
    response = HttpResponse()
    try:
        proj_id = request.GET.get('proj_id')
        data_id = request.GET.get('data_id')
        user_id = request.COOKIES.get('user_id')
        if len(Datasets.objects.filter(proj_id=proj_id, data_id=data_id, user_id=user_id)) == 0:
            raise Exception('Oops! No access!')
        Datasets.objects.filter(proj_id=proj_id, data_id=data_id, user_id=user_id).delete()

        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def download_data(request):
    try:
        data_id = request.GET.get('data_id')
        user_id = request.COOKIES.get('user_id')
        data_path = data_id + '.csv'
        data_cont_query = Datasets.objects.filter(data_id=data_id, user_id=user_id).values('data_cont')
        if len(data_cont_query) == 0:
            raise Exception('Oops! No access!')
        data_cont = list(data_cont_query)[0]['data_cont']
        pd.read_json(data_cont).to_csv(data_path)
        data_file = open(data_path, 'rb')
        
        response = FileResponse(data_file)
        response['Content-Type']='application/octet-stream'
        response['Content-Disposition']='attachment;filename=\"' + data_id + '.csv\"'
    except Exception as e:
        response_content = {}
        response = HttpResponse()
        response_content['msg'] = str(e)
        response_content['error_num'] = 1
        response.write(json.dumps(response_content))

    return response

# ==================================================
# Workflow Management APIs
# ==================================================
@require_http_methods(["GET", "POST"])
def new_task(request):
    response = HttpResponse()
    response_content = {}
    try:
        if request.method == 'GET':
            get_token(request)
        if request.method == 'POST':
            postBody = json.loads(request.body.decode("utf-8"))
            task_id = 'TASK' + time.strftime('%Y%m%d%H%M%S')
            proj_id = postBody.get('proj_id')
            task_name = postBody.get('task_name')
            task_type = postBody.get('task_type')
            if task_type[:2] == 'ml':
                task_config = {}
                task_config['proj_name'] = postBody.get('proj_name')
                task_config['train_data'] = postBody.get('train_data')
                task_config['enable_test'] = postBody.get('enable_test')
                task_config['test_data'] = postBody.get('test_data')
                task_config['label'] = postBody.get('label')
                task_config['feat_sel'] = postBody.get('feat_sel')
                task_config['estimator'] = postBody.get('estimator')
                task_config['cv_type'] = postBody.get('cv_type')

                task = Submissions(
                    task_id=task_id,
                    proj_id=proj_id,
                    task_name=task_name,
                    task_type=task_type,
                    task_config=json.dumps(task_config),
                    task_status='Submitted',
                    task_result=''
                )
                task.save()

                # create new celery task
                new_ml_celery_task.delay(
                    taskid=task_id,
                    tasktype=task_type,
                    traindata=task_config['train_data'],
                    enabletest=task_config['enable_test'],
                    testdata=task_config['test_data'],
                    label=task_config['label'],
                    featsel=task_config['feat_sel'],
                    estimator=task_config['estimator'],
                    cv=task_config['cv_type']
                )

            elif task_type[:2] == 'sa':
                task_config = {}
                task_config['proj_name'] = postBody.get('proj_name')
                task_config['test_var_data_x'] = postBody.get('test_var_data_x')
                task_config['group_var_data_y'] = postBody.get('group_var_data_y')

                task = Submissions(
                    task_id=task_id,
                    proj_id=proj_id,
                    task_name=task_name,
                    task_type=task_type,
                    task_config=json.dumps(task_config),
                    task_status='Submitted',
                    task_result=''
                )
                task.save()

                # # create new celery task
                # new_sa_celery_task.delay(
                #     taskid=task_id,
                #     tasktype=task_type,
                #     testvardatax=task_config['test_var_data_x'],
                #     groupvardatay=task_config['group_var_data_y']
                # )

            response_content['post_body'] = postBody
            response_content['msg'] = 'success'
            response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

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
        user_id = request.COOKIES.get('user_id')
        proj_ids = User_Proj_Auth.objects.filter(user_id=user_id).values('proj_id')
        proj_id_list = []
        for itm in proj_ids:
            proj_id_list.append(itm['proj_id'])
        if analysis_type == 'Machine Learning':
            submissions = Submissions.objects.filter(task_type__in = ['ml_clf', 'ml_rgs'], proj_id__in = proj_id_list).order_by('-id')[:4]
            response_content['list']  = json.loads(serializers.serialize("json", submissions))
        elif analysis_type == 'Statistical Analysis':
            submissions = Submissions.objects.filter(task_type__in = ['sa_da_ttest', 'sa_da_anova', 'sa_ca_prson', 'sa_ca_spman'], proj_id__in = proj_id_list).order_by('-id')[:4]
            response_content['list']  = json.loads(serializers.serialize("json", submissions))

        total = Submissions.objects.filter()
        response_content['total_num'] = len(total)
        submitted = Submissions.objects.filter(task_status='Submitted')
        response_content['submitted_num'] = len(submitted)
        running = Submissions.objects.filter(task_status='Running')
        response_content['running_num'] = len(running)
        finished = Submissions.objects.filter(task_status='Finished')
        response_content['finished_num'] = len(finished)
        failed = Submissions.objects.filter(task_status='Failed')
        response_content['failed_num'] = len(failed)

        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def show_submissions(request):
    response_content = {}
    response = HttpResponse()
    try:
        analysis_type = request.GET.get('analysis_type')
        user_id = request.COOKIES.get('user_id')
        proj_ids = User_Proj_Auth.objects.filter(user_id=user_id).values('proj_id')
        proj_id_list = []
        for itm in proj_ids:
            proj_id_list.append(itm['proj_id'])
        if analysis_type == 'Machine Learning':
            submissions = Submissions.objects.filter(task_type__in = ['ml_clf', 'ml_rgs'], proj_id__in = proj_id_list).order_by('-id')
            response_content['list']  = json.loads(serializers.serialize("json", submissions))
        elif analysis_type == "Statistical Analysis":
            submissions = Submissions.objects.filter(task_type__in = ['sa_da_ttest', 'sa_da_anova', 'sa_ca_prson', 'sa_ca_spman'], proj_id__in = proj_id_list).order_by('-id')[:4]
            response_content['list']  = json.loads(serializers.serialize("json", submissions))
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def show_results(request):
    response_content = {}
    response = HttpResponse()
    try:
        task_id = request.GET.get('task_id')
        analysis_type = request.GET.get('analysis_type')
        
        task_info_query = Submissions.objects.filter(task_id=task_id).values('task_id', 'proj_id', 'task_name', 'task_type', 'task_config', 'task_status', 'task_result')
        task_info = list(task_info_query)[0]
        
        if analysis_type == 'Machine Learning':
            # response with task configuration list
            task_config = task_info['task_config']
            task_info_dict = json.loads(task_config)
            task_info_dict['task_name'] = task_info['task_name']
            task_info_dict['task_type'] = task_info['task_type']
            response_content['info'] = task_info_dict

            # response with task result table
            task_result_json = task_info['task_result']
            task_result_dict = json.loads(task_result_json)
            result_table_dict = task_result_dict.copy()
            if 'Feature Weights' in result_table_dict.keys():
                del(result_table_dict['Feature Weights'])
            if 'Optimization' in result_table_dict.keys():
                del(result_table_dict['Optimization'])
            if 'ROC fpr' in result_table_dict.keys():
                del(result_table_dict['ROC fpr'])
            if 'ROC tpr' in result_table_dict.keys():
                del(result_table_dict['ROC tpr'])
            result_table_dict['Optimal Parameters'] = str(result_table_dict['Optimal Parameters'])
            result_table = []
            for idx in range(len(list(result_table_dict.keys()))):
                result_table.append({'Item': list(result_table_dict.keys())[idx], 'Value': list(result_table_dict.values())[idx]})
            response_content['list'] = result_table

            # response with feature weights list if exists
            response_content['got_weights'] = 0
            if 'Feature Weights' in task_result_dict.keys():
                feature_weights_list = pd.DataFrame.from_records(task_result_dict['Feature Weights'])
                feature_weights_list.to_csv(path_or_buf='feature_weights.csv')
                response_content['got_weights'] = 1

            # response with image data if exists
            response_content['img_list'] = []
            if 'Optimization' in task_result_dict.keys():
                plt.figure()
                best_clfs = pd.DataFrame.from_records(task_result_dict['Optimization'])
                print(best_clfs.columns.values.tolist())
                components_col = best_clfs.columns.values.tolist()[3]
                best_clfs.plot(x=components_col, y='mean_test_score', yerr='std_test_score')
                plt.ylabel('Classification accuracy (val)')
                plt.xlabel('n_features_to_select')
                plt.title('Optimization Curve')
                plt.savefig('optimization_curve.png', dpi=300)
                plt.close()
                response_content['img_list'].append('optimization_curve.png')
            if 'ROC fpr' in task_result_dict.keys():
                plt.figure()
                mean_fpr = np.linspace(0, 1, 100)
                fpr = np.array(task_result_dict['ROC fpr'])
                tpr = np.array(task_result_dict['ROC tpr'])
                roc_auc = auc(fpr, tpr)
                plt.plot(fpr, tpr, lw=1, alpha=0.3, color='b',
                        label='AUC = %0.2f' % (roc_auc))
                plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
                        label='Chance', alpha=.8)
                plt.xlim([-0.05, 1.05])
                plt.ylim([-0.05, 1.05])
                plt.xlabel('False Positive Rate')
                plt.ylabel('True Positive Rate')
                plt.title('Receiver Operating Characteristic')
                plt.legend(loc="lower right")
                plt.savefig('ROC_curve.png', dpi=300)
                plt.close()
                response_content['img_list'].append('ROC_curve.png')

        elif analysis_type == 'Statistical Analysis':
            task_info = Submissions_SA_Demo.objects.filter(task_id=task_id, task_status='Finished')
            assert list(task_info)
            response_content['info'] = json.loads(serializers.serialize("json", task_info))

        response_content['msg'] = 'success'
        response_content['error_num'] = 0

    except Exception as e:
        traceback.print_exc()
        if analysis_type == 'Machine Learning':
            response_content['msg'] = json.dumps(Submissions.objects.get(task_id=task_id).task_result)
        elif analysis_type == 'Statistical Analysis':
            response_content['msg'] = json.dumps(Submissions.objects.get(task_id=task_id).task_result)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def show_img(request):
    response = {}
    img_name = request.GET.get('img_name')

    buf = io.BytesIO()
    img = Image.open(img_name)
    img.save(buf, 'png')

    return HttpResponse(buf.getvalue(), 'image/png')

@require_http_methods(["GET"])
def download_feature_weights(request):
    task_id = request.GET.get('task_id')
    feature_weights_file = open('feature_weights.csv', 'rb')
    
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
