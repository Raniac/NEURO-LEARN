# Dev Doc of NEURO-LEARN
## Contents
- [Dev Doc of NEURO-LEARN](#Dev-Doc-of-NEURO-LEARN)
  - [Contents](#Contents)
  - [Demand Analysis](#Demand-Analysis)
    - [Data Management](#Data-Management)
    - [Statistical Workflows](#Statistical-Workflows)
    - [Machine Learning Workflows](#Machine-Learning-Workflows)
    - [Deep Learning Workflows](#Deep-Learning-Workflows)
  - [API Definition](#API-Definition)
    - [Universal APIs](#Universal-APIs)
      - [User Login](#User-Login)
      - [User Register](#User-Register)
    - [Data Management APIs](#Data-Management-APIs)
      - [Download Templates](#Download-Templates)
      - [Upload Data](#Upload-Data)
      - [Show Data](#Show-Data)
    - [Workflow Management APIs](#Workflow-Management-APIs)
      - [New Machine Learning Task](#New-Machine-Learning-Task)
      - [New Statistical Analysis Task](#New-Statistical-Analysis-Task)
      - [Overview Submissions](#Overview-Submissions)
      - [Show Submissions](#Show-Submissions)
      - [Show Results](#Show-Results)
      - [Show Images](#Show-Images)
      - [Download Feature Weights](#Download-Feature-Weights)
      - [Download Significance Values](#Download-Significance-Values)
  - [Database Definition](#Database-Definition)
    - [User Management](#User-Management)
      - [backend_user_demo](#backenduserdemo)
    - [Data Management](#Data-Management-1)
      - [backend_data_demo](#backenddatademo)
    - [Workflow Management](#Workflow-Management)
      - [backend_submissions_demo](#backendsubmissionsdemo)
      - [backend_submissions_sa_demo](#backendsubmissionssademo)

## Demand Analysis

### Data Management

### Statistical Workflows

### Machine Learning Workflows

### Deep Learning Workflows

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