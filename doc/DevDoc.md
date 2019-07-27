# Dev Doc of NEURO-LEARN
## Contents
- [Dev Doc of NEURO-LEARN](#dev-doc-of-neuro-learn)
  - [Contents](#contents)
  - [Demand Analysis and Functionality Design](#demand-analysis-and-functionality-design)
    - [Data Management](#data-management)
      - [Project Overview](#project-overview)
      - [Data Uploading](#data-uploading)
    - [Workflow Management](#workflow-management)
      - [Analysis Overview](#analysis-overview)
      - [Statistical Analysis](#statistical-analysis)
        - [Difference Analysis](#difference-analysis)
        - [Correlation Analysis](#correlation-analysis)
      - [Machine Learning](#machine-learning)
        - [Classification/Regression](#classificationregression)
      - [Deep Learning](#deep-learning)
      - [Submission Management](#submission-management)
      - [View Reports](#view-reports)
  - [API Definition](#api-definition)
    - [Universal APIs](#universal-apis)
      - [User Login](#user-login)
      - [User Register](#user-register)
    - [Data Management APIs](#data-management-apis)
      - [Show Project Overview](#show-project-overview)
      - [Download Templates](#download-templates)
      - [Upload Data](#upload-data)
      - [Show Data](#show-data)
    - [Workflow Management APIs](#workflow-management-apis)
      - [New Machine Learning Task](#new-machine-learning-task)
      - [New Statistical Analysis Task](#new-statistical-analysis-task)
      - [Overview Submissions](#overview-submissions)
      - [Show Submissions](#show-submissions)
      - [Show Results](#show-results)
      - [Show Images](#show-images)
      - [Download Feature Weights](#download-feature-weights)
      - [Download Significance Values](#download-significance-values)
  - [Database Definition](#database-definition)
    - [User Management](#user-management)
      - [backend_user_demo](#backenduserdemo)
    - [Data Management](#data-management-1)
      - [backend_projects_demo](#backendprojectsdemo)
      - [backend_data_demo](#backenddatademo)
    - [Workflow Management](#workflow-management-1)
      - [backend_submissions_demo](#backendsubmissionsdemo)
      - [backend_submissions_sa_demo](#backendsubmissionssademo)

## Demand Analysis and Functionality Design

### Data Management

#### Project Overview

Define data and workflow templates in the project overview page, which can be downloaded for users to use. The templates should contain necessary information that helps users to prepare their data correctly and uniformly.

#### Data Uploading

If one had prepared a dataset according to the templates, he/she should be able to upload it to the cloud for further usage. He/She should also be able to see formerly uploaded datasets under one certain project.

### Workflow Management

#### Analysis Overview

In this page, users can see the statics of submitted tasks and the most recent submitted ones. Further, the configuration of the tasks should also be included in the table of submissions.

#### Statistical Analysis

##### Difference Analysis

Configure a difference analysis task and submit it to run. The types of difference analysis should at least include t-test and ANOVA.

##### Correlation Analysis

Configure a correlation analysis task and submit it to run. The types of correlation analysis should at least include Pearson and Spearman.

#### Machine Learning

##### Classification/Regression

Configure a machine learning task and submit it to run. The types of task should include classification and regression.

#### Deep Learning

#### Submission Management

In this page, users can see all of the submitted tasks and the configuration of them. They should also be able to filter the tasks by their status and names.

#### View Reports

User should be able to view multiple reports, which should include sufficient information about the evaluation of the tasks.

## API Definition

### Universal APIs

#### User Login
- Request Information
  - Address: /api/user_login
  - Method: GET
- Response Information
  - Type: HTTP
  - Content:
    - error_num: request status
    - msg: request result
- Parameter Definition:

Parameter Name | Description | Necessary | Type | Default Value
:-: | :-: | :-: | :-: | :-:
username | Username | True | STRING |
password | Password | True | STRING |

#### User Register
- Request Information
  - Address: /api/user_register
  - Method: POST
- Response Information
  - Type: JSON
  - Content:
    - error_num: request status
    - msg: request result
- Parameter Definition:

Parameter Name | Description | Necessary | Type | Default Value
:-: | :-: | :-: | :-: | :-:
username | Username | True | STRING |
password | Password | True | STRING |

### Data Management APIs

#### Show Project Overview
- Request Information
  - Address: /api/show_project_overview
  - Method: GET
- Response Information
  - Type: JSON
  - Content:
    - error_num: request status
    - msg: request result
    - list: projects list

#### Download Templates
- Request Information
  - Address: /api/download_templates
  - Method: GET
- Response Information
  - Type: FILE
  - Content:
    - Content-Type: 'application/octet-stream'
    - Content-Disposition: 'attachment;filename=\"' + template_type + '.zip\"'
- Parameter Definition:

Parameter Name | Description | Necessary | Type | Default Value
:-: | :-: | :-: | :-: | :-:
template_type | Template Type | True | STRING |

#### Upload Data
- Request Information
  - Address: /api/upload_data
  - Method: POST
- Response Information
  - Type: HTTP
  - Content:
    - error_num: request status
    - msg: request result

#### Show Data
- Request Information
  - Address: /api/show_data
  - Method: GET
- Response Information
  - Type: JSON
  - Content:
    - error_num: request status
    - msg: request result
    - list: data list
- Parameter Definition:

Parameter Name | Description | Necessary | Type | Default Value
:-: | :-: | :-: | :-: | :-:
project_id | Project ID | True | STRING |

### Workflow Management APIs

#### New Machine Learning Task
- Request Information
  - Address: /api/new_task
  - Method: POST
- Response Information
  - Type: HTTP
  - Content:
    - error_num: request status
    - msg: request result
- Parameter Definition:

Parameter Name | Description | Necessary | Type | Default Value
:-: | :-: | :-: | :-: | :-:
task_name | Task Name | True | STRING |
task_type | Task Type | True | STRING |
project_name | Project Name | True | STRING |
train_data | Train Data | True | STRING |
enable_test | Enable Test | True | BOOLEAN |
test_data | Test Data | True | STRING |
label | Label | True | STRING |
feat_sel | Feature Selection | True | STRING |
estimator | Estimator | True | STRING |
cv_type | CV Type | True | STRING |
note | Note | True | STRING |
verbose | Verbose | True | BOOLEAN |

#### New Statistical Analysis Task
- Request Information
  - Address: /api/new_sa_task
  - Method: POST
- Response Information
  - Type: HTTP
  - Content:
    - error_num: request status
    - msg: request result
- Parameter Definition:

Parameter Name | Description | Necessary | Type | Default Value
:-: | :-: | :-: | :-: | :-:
task_name | Task Name | True | STRING |
task_type | Task Type | True | STRING |
project_name | Project Name | True | STRING |
test_var_data_x | Train Data | True | STRING |
group_var_data_y | Test Data | True | STRING |
note | Note | True | STRING |
verbose | Verbose | True | BOOLEAN |

#### Overview Submissions
- Request Information
  - Address: /api/overview_submissions
  - Method: GET
- Response Information
  - Type: JSON
  - Content:
    - error_num: request status
    - msg: request result
    - list: submissions list
    - total_num: number of total submissions
    - submitted_num: number of submitted submissions
    - running_num: number of running submissions
    - finished_num: number of finished submissions
    - failed_num: number of failed submissions
- Parameter Definition:

Parameter Name | Description | Necessary | Type | Default Value
:-: | :-: | :-: | :-: | :-:
analysis_type | Analysis Type | True | STRING |

#### Show Submissions
- Request Information
  - Address: /api/show_submissions
  - Method: GET
- Response Information
  - Type: JSON
  - Content:
    - error_num: request status
    - msg: request result
    - list: submissions list
- Parameter Definition:

Parameter Name | Description | Necessary | Type | Default Value
:-: | :-: | :-: | :-: | :-:
analysis_type | Analysis Type | True | STRING |

#### Show Results
- Request Information
  - Address: /api/show_results
  - Method: GET
- Response Information
  - Type: JSON
  - Content:
    - error_num: request status
    - msg: request result
    - list: result table
    - info: task info
    - got_weights: whether feature_weights is available
    - img_list: list of all result images
- Parameter Definition:

Parameter Name | Description | Necessary | Type | Default Value
:-: | :-: | :-: | :-: | :-:
task_id | Task ID | True | STRING |
analysis_type | Analysis Type | True | STRING |

#### Show Images
- Request Information
  - Address: /api/show_img
  - Method: GET
- Response Information
  - Type: HTTP
  - Content:
    - io/buf: result images
- Parameter Definition:

Parameter Name | Description | Necessary | Type | Default Value
:-: | :-: | :-: | :-: | :-:
task_id | Task ID | True | STRING |
img_name | Image Name | True | STRING |

#### Download Feature Weights
- Request Information
  - Address: /api/download_feature_weights
  - Method: GET
- Response Information
  - Type: FILE
  - Content:
    - Content-Type: 'application/octet-stream'
    - Content-Disposition: 'attachment;filename=\"' + task_id + '/' + 'feature_weights.csv\"'
- Parameter Definition:

Parameter Name | Description | Necessary | Type | Default Value
:-: | :-: | :-: | :-: | :-:
task_id | Task ID | True | STRING |

#### Download Significance Values
- Request Information
  - Address: /api/download_significance_values
  - Method: GET
- Response Information
  - Type: FILE
  - Content:
    - Content-Type: 'application/octet-stream'
    - Content-Disposition: 'attachment;filename=\"' + task_id + '/' + 'significance.csv\"'
- Parameter Definition:

Parameter Name | Description | Necessary | Type | Default Value
:-: | :-: | :-: | :-: | :-:
task_id | Task ID | True | STRING |

## Database Definition

### User Management

#### backend_user_demo

Field Name | Data Type | Max Length | Primary Key | Index | Description
:-: | :-: | :-: | :-: | :-: | :-:
id | INT | False | True | True | Primary ID
user_id | VARCHAR | 64 | False | True | 'USER' + time.strftime('%Y%m%d%H%M%S')
username | VARCHAR | 32 | False | False |
password | VARCHAR | 64 | False | False |

### Data Management

#### backend_projects_demo

Field Name | Data Type | Max Length | Primary Key | Index | Description
:-: | :-: | :-: | :-: | :-: | :-:
id | INT | False | True | True | Primary ID
project_id | VARCHAR | 64 | False | True | 'PROJ' + time.strftime('%Y%m%d%H%M%S')
label | VARCHAR | 64 | False | False |
title | VARCHAR | 128 | False | False |
introduction | TEXT | 4096 | False | False |
methods | TEXT | 4096 | False | False |
flowchart_url | VARCHAR | 128 | False | False |
workflow_templates_url | VARCHAR | 128 | False | False |
data_templates_url | VARCHAR | 128 | False | False |

#### backend_data_demo

Field Name | Data Type | Max Length | Primary Key | Index | Description
:-: | :-: | :-: | :-: | :-: | :-:
id | INT | False | True | True | Primary ID
data_id | VARCHAR | 64 | False | True | 'DATA' + time.strftime('%Y%m%d%H%M%S')
data_name | VARCHAR | 64 | False | False |
data_path | VARCHAR | 128 | False | False |

### Workflow Management

#### backend_submissions_demo

Field Name | Data Type | Max Length | Primary Key | Index | Description
:-: | :-: | :-: | :-: | :-: | :-:
id | INT | False | True | True | Primary ID
task_id | VARCHAR | 64 | False | True | 'TASK' + time.strftime('%Y%m%d%H%M%S')
task_name | VARCHAR | 64 | False | False |
task_type | VARCHAR | 64 | False | False |
project_name | VARCHAR | 64 | False | False |
train_data | VARCHAR | 1024 | False | False |
enable_test | BOOLEAN | False | False | False |
test_data | VARCHAR | 64 | False | False |
label | VARCHAR | 64 | False | False |
feat_sel | VARCHAR | 64 | False | False |
estimator | VARCHAR | 64 | False | False |
cv_type | VARCHAR | 64 | False | False |
note | VARCHAR | 64 | False | False |
verbose | BOOLEAN | False | False | False |
task_status | VARCHAR | 64 | False | False | 'Submitted'
task_result | VARCHAR | 1024 | False | False |

#### backend_submissions_sa_demo

Field Name | Data Type | Max Length | Primary Key | Index | Description
:-: | :-: | :-: | :-: | :-: | :-:
id | INT | False | True | True | Primary ID
task_id | VARCHAR | 64 | False | True | 'TASK' + time.strftime('%Y%m%d%H%M%S')
task_name | VARCHAR | 64 | False | False |
task_type | VARCHAR | 64 | False | False |
project_name | VARCHAR | 64 | False | False |
test_var_data_x | VARCHAR | 1024 | False | False |
group_var_data_y | VARCHAR | 1024 | False | False |
note | VARCHAR | 64 | False | False |
verbose | BOOLEAN | False | False | False |
task_status | VARCHAR | 64 | False | False | 'Submitted'
task_result | VARCHAR | 1024 | False | False |