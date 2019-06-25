import os
import pandas as pd
from .components import *

def test_sa_task(task_id, task_type, test_var_data_x, group_var_data_y):
    print(task_id, task_type, test_var_data_x[0], group_var_data_y[0])
    
    RESULT_PATH = 'results/' + task_id
    if not os.path.exists(RESULT_PATH):
        os.makedirs(RESULT_PATH)

    if task_type[:2] == 'DA':
        TEST_VAR_PATH = test_var_data_x[0]
        GROUP_VAR = 'LABEL_' + group_var_data_y

        data_columns = pd.read_csv(TEST_VAR_PATH, encoding='gbk').columns
        columns_to_drop = []
        for column in data_columns:
            if column == 'ID':
                columns_to_drop.append(column)
            elif column[:6] == 'LABEL_':
                columns_to_drop.append(column)
            else:
                break

        test_variables = pd.read_csv(TEST_VAR_PATH, encoding='gbk').drop(columns_to_drop, axis=1)
        group_variables = pd.read_csv(TEST_VAR_PATH, encoding='gbk')[GROUP_VAR]

        if len(test_var_data_x) > 0:
            for i in range(1, len(test_var_data_x)):
                test_variables_temp = pd.read_csv(test_var_data_x[i], encoding='gbk').drop(columns_to_drop, axis=1)
                group_variables_temp = pd.read_csv(test_var_data_x[i], encoding='gbk')[GROUP_VAR]
                test_variables = pd.concat([test_variables, test_variables_temp], axis=0)
                group_variables = pd.concat([group_variables, group_variables_temp], axis=0)

        if task_type[3:] == 'T-test':
            integrated_ttest(RESULT_PATH, test_variables, group_variables)
        elif task_type[3:] == 'ANOVA':
            integrated_anova(RESULT_PATH, test_variables, group_variables)
    
    elif task_type[:2] == 'CA':
        DATA_X_PATH = test_var_data_x[0]
        DATA_Y_PATH = group_var_data_y[0]

        data_columns = pd.read_csv(DATA_X_PATH, encoding='gbk').columns
        columns_to_drop = []
        for column in data_columns:
            if column == 'ID':
                columns_to_drop.append(column)
            elif column[:6] == 'LABEL_':
                columns_to_drop.append(column)
            else:
                break

        data_x = pd.read_csv(DATA_X_PATH, encoding='gbk').drop(columns_to_drop, axis=1)
        data_y = pd.read_csv(DATA_Y_PATH, encoding='gbk').drop(columns_to_drop, axis=1)

        if len(test_var_data_x) > 0:
            for i in range(1, len(test_var_data_x)):
                data_x_temp = pd.read_csv(test_var_data_x[i], encoding='gbk').drop(columns_to_drop, axis=1)
                data_x = pd.concat([data_x, data_x_temp], axis=0)

        if len(group_var_data_y) > 0:
            for i in range(1, len(group_var_data_y)):
                data_y_temp = pd.read_csv(group_var_data_y[i], encoding='gbk').drop(columns_to_drop, axis=1)
                data_y = pd.concat([data_y, data_y_temp], axis=0)

        if task_type[3:] == 'Pearson':
            integrated_pearson(RESULT_PATH, data_x, data_y)
        elif task_type[3:] == 'Spearman':
            integrated_spearman(RESULT_PATH, data_x, data_y)