import numpy as np
import pandas as pd
import time
import decimal
import seaborn as sns
import csv
import scipy
import statsmodels.stats.weightstats as st

def integrated_ttest(result_path, test_variables, group_variables):
    feature_list = test_variables.columns
    ttest_results = pd.DataFrame({'Feature Name': [],'t value': [], 'p value': []})
    t_value_list = []
    p_value_list = []

    group0_var = test_variables[group_variables == 0]
    group1_var = test_variables[group_variables == 1]

    for feature_name in feature_list:
        t_value, p_value, df = st.ttest_ind(group0_var[feature_name], group1_var[feature_name], usevar='unequal')
        t_value_list.append(t_value)
        p_value_list.append(p_value)

    ttest_results['Feature Name'] = feature_list
    ttest_results['t value'] = t_value_list
    ttest_results['p value'] = p_value_list

    ttest_results.to_csv(path_or_buf=result_path + '/' + 'significance.csv')

def integrated_anova(result_path, test_variables, group_variables):
    pass

def integrated_pearson(result_path, data_x, data_y):
    x_feature_list = data_x.columns
    y_feature_list = data_y.columns
    pearson_results = pd.DataFrame({'X Feature Name': [], 'Y Feature Name': [], 'r value': [], 'p value': []})
    x_feature_names = []
    y_feature_names = []
    r_value_list = []
    p_value_list = []

    for x_feature_name in x_feature_list:
        for y_feature_name in y_feature_list:
            r_value, p_value = scipy.stats.pearsonr(data_x[x_feature_name], data_y[y_feature_name])
            x_feature_names.append(x_feature_name)
            y_feature_names.append(y_feature_name)
            r_value_list.append(r_value)
            p_value_list.append(p_value)

    pearson_results['X Feature Name'] = x_feature_names
    pearson_results['Y Feature Name'] = y_feature_names
    pearson_results['r value'] = r_value_list
    pearson_results['p value'] = p_value_list
    
    pearson_results.to_csv(path_or_buf=result_path + '/' + 'significance.csv')

def integrated_spearman(result_path, data_x, data_y):
    pass