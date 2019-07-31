import os
import time
import traceback
import logging
import pymysql

# ========================================
# Define the content of the project.
# ========================================
PROJECT_LABEL = 'SZ with BCN'
PROJECT_TITLE = 'Study of Schizophrenia with Pattern Analysis of Brain Connectivity Networks'
# Project Introduction (No more than 400 words)
PROJECT_INTRODUCTION = '''\
This is introduction.\
'''
# Project Methods (No more than 400 words)
PROJECT_METHEDS = '''\
This is methods.\
'''
# ========================================
# End of definition.
# ========================================

PROJECT_ID = 'PROJ' + time.strftime('%Y%m%d%H%M%S')

def create_project(sql, proj):
    try:
        conn = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
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
        'methods': PROJECT_METHEDS,
        'flowchart_url': '/api/show_flowchart?project_id=' + PROJECT_ID,
        'workflows_url': '/api/download_workflows?project_id' + PROJECT_ID,
        'templates_url': '/api/download_templates?project_id' + PROJECT_ID
    }

    sql = """
    insert into backend_projects_demo(project_id, label, title, introduction, methods, flowchart_url, workflows_url, templates_url) 
    values(%s, %s, %s, %s, %s, %s, %s, %s);
    """

    logging.info(project['project_id'])
    logging.info(project['label'])
    logging.info(project['title'])
    logging.info(project['introduction'])
    logging.info(project['methods'])

    print()
    print('Are you sure you want to create this project? [y/n]')
    confirm = input()

    if confirm == 'y':
        create_project(sql, project)

        project_path = 'projects/' + PROJECT_ID
        os.makedirs(project_path)
    else:
        logging.info('Exit without creating anything!')
