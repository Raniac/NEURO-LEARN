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
FLOWCHART_URL = 'https://raw.githubusercontent.com/Raniac/NEURO-LEARN/master/projects/sz_sfmri_dpabi/flowchart.png'
# Workflows Url
WORKFLOWS_URL = 'https://github.com/Raniac/NEURO-LEARN/raw/master/projects/sz_sfmri_dpabi/local_workflows.zip'
# Templates Url
TEMPLATES_URL = 'https://github.com/Raniac/NEURO-LEARN/raw/master/projects/sz_sfmri_dpabi/data_templates.zip'

DB_HOST = '120.79.49.129'
DB_NAME = 'neurolearn'
# ========================================
# End of definition.
# ========================================

PROJECT_ID = 'PROJ' + time.strftime('%Y%m%d%H%M%S')
# PROJECT_ID = 'PROJ00000000000000'

def create_project(sql, proj):
    try:
        conn = pymysql.connect(
            host = DB_HOST,
            user = 'neurolearn',
            password = 'nl4444_',
            database = DB_NAME,
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
    print()
    print('\033[0;36;40mNL\033[0m \033[1;36mNEURO-LEARN\033[0m')
    print()
    print('\033[1mAuthored by Raniac\033[0m')
    print()
    logging.info('\033[0;36mThis is the content of your project:\033[0m')
    print()

    logging.info('\033[0;36mProject ID: \033[0m'+project['project_id'])
    logging.info('\033[0;36mProj Label: \033[0m'+project['label'])
    logging.info('\033[0;36mProj Title: \033[0m'+project['title'])
    logging.info('\033[0;36mProj Intro: \033[0m'+project['introduction'])
    logging.info('\033[0;36mProj Methd: \033[0m'+project['methods'])
    logging.info('\033[0;36mProj FlwCh: \033[0m'+project['flowchart_url'])
    logging.info('\033[0;36mProj WrkFl: \033[0m'+project['workflows_url'])
    logging.info('\033[0;36mProj TmpLt: \033[0m'+project['templates_url'])

    print()
    logging.info('\033[0;36mConfirm to create this project?\033[0m \033[1m[y/n]\033[0m')
    confirm = input()

    if confirm in ['y', 'Y']:
        create_project(sql, project)
    else:
        logging.info('Exit without creating anything!')
