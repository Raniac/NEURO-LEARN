# Dev Doc for NEURO-LEARN
## Contents
- [Dev Doc for NEURO-LEARN](#Dev-Doc-for-NEURO-LEARN)
  - [Contents](#Contents)
  - [Demand Analysis](#Demand-Analysis)
    - [Data Management](#Data-Management)
    - [Statistical Workflows](#Statistical-Workflows)
    - [Machine Learning Workflows](#Machine-Learning-Workflows)
    - [Deep Learning Workflows](#Deep-Learning-Workflows)
  - [Interface Definition](#Interface-Definition)
    - [Universal Interfaces](#Universal-Interfaces)
    - [Data Management Interfaces](#Data-Management-Interfaces)
    - [Workflow Management Interfaces](#Workflow-Management-Interfaces)
  - [Database Definition](#Database-Definition)
    - [User Management](#User-Management)
    - [Data Management](#Data-Management-1)
    - [Workflow Management](#Workflow-Management)

## Demand Analysis

### Data Management

### Statistical Workflows

### Machine Learning Workflows

### Deep Learning Workflows

## Interface Definition

### Universal Interfaces

### Data Management Interfaces

### Workflow Management Interfaces

## Database Definition

### User Management

- backend_user_demo

Field Name | Data Type | Max Length | Primary Key | Index | Description
:-: | :-: | :-: | :-: | :-: | :-:
id | INT | False | True | True | Primary ID
user_id | VARCHAR | 64 | False | True | 'USER' + time.strftime('%Y%m%d%H%M%S')
username | VARCHAR | 32 | False | False |
password | VARCHAR | 64 | False | False |

### Data Management

- backend_data_demo

Field Name | Data Type | Max Length | Primary Key | Index | Description
:-: | :-: | :-: | :-: | :-: | :-:
id | INT | False | True | True | Primary ID
data_id | VARCHAR | 64 | False | True | 'DATA' + time.strftime('%Y%m%d%H%M%S')
data_name | VARCHAR | 64 | False | False |
data_path | VARCHAR | 128 | False | False |

### Workflow Management

- backend_submissions_demo

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

- backend_submissions_sa_demo

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