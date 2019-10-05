import os
import time
import traceback
import logging
import pymysql

# ========================================
# Define the content of the project.
# ========================================
PROJECT_LABEL = 'SZ with sfMRI'
PROJECT_TITLE = 'Study of Schizophrenia with Pattern Analysis of Structural/Functional MRI Data'
# Project Introduction (No more than 400 words)
PROJECT_INTRODUCTION = '''\
Fusing structural and functional MRI data, use DPABI on matlab to compute the features, and analyze SZ.\
'''
# Project Methods (No more than 400 words)
PROJECT_METHODS = '''\
Compute gray matter volume, regional homogeneity, amplitude of low frequency fluctuations and degree centrality.\
'''
# Flowchart Url
FLOWCHART_URL = 'https://raw.githubusercontent.com/Raniac/NEURO-LEARN/master/doc/img/neurolearn_framework.png'
# Workflows Url
WORKFLOWS_URL = 'https://github.com/Raniac/NEURO-LEARN/raw/master/projects/PROJ00000000000000/local_workflows.zip'
# Templates Url
TEMPLATES_URL = 'https://github.com/Raniac/NEURO-LEARN/raw/master/projects/PROJ20190626040404/dataset_templates.zip'
# ========================================
# End of definition.
# ========================================

PROJECT_ID = 'PROJ' + time.strftime('%Y%m%d%H%M%S')
# PROJECT_ID = 'PROJ00000000000000'

def create_project(sql, proj):
    try:
        conn = pymysql.connect(
            host = '127.0.0.1',
            user = 'neurolearn',
            password = 'nl4444_',
            database = 'neurolearn_dev',
            charset = 'utf8'
        )
        cursor = conn.cursor()
        cursor.execute(sql, [
            proj['project_id'],
            proj['label'],
            proj['title'],
            proj['introduction'],
            proj['methods'],
            proj['flowchart_url'],
            proj['workflows_url'],
            proj['templates_url']
        ])
        conn.commit() # required when a 'write' operation is involved
        logging.info('Project created! ID: ' + PROJECT_ID)
    except:
        logging.error('Database error!')
        traceback.print_exc()
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
    return
 
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(levelname)s] %(message)s')
    logging.basicConfig(level=logging.ERROR, format='[%(asctime)s %(levelname)s] %(message)s')

    project = {
        'project_id': PROJECT_ID,
        'label': PROJECT_LABEL,
        'title': PROJECT_TITLE,
        'introduction': PROJECT_INTRODUCTION,
        'methods': PROJECT_METHODS,
        'flowchart_url': FLOWCHART_URL,
        'workflows_url': WORKFLOWS_URL,
        'templates_url': TEMPLATES_URL
    }

    sql = """
    insert into backend_projects(proj_id, label, title, introduction, methods, flowchart_url, workflows_url, templates_url) 
    values(%s, %s, %s, %s, %s, %s, %s, %s);
    """

    logging.info('Project ID: '+project['project_id'])
    logging.info('Proj Label: '+project['label'])
    logging.info('Proj Title: '+project['title'])
    logging.info('Proj Intro: '+project['introduction'])
    logging.info('Proj Methd: '+project['methods'])

    print()
    print('Are you sure you want to create this project? [y/n]')
    confirm = input()

    if confirm in ['y', 'Y']:
        create_project(sql, project)
    else:
        logging.info('Exit without creating anything!')
