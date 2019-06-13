import os
import sys
import time
import pandas as pd
from .acquisition import Data
from .models import *
from .integrated import *

def test_task(task_id, task_type, train_data, test_data, label, feat_sel, estimator, cv_type):
    print(task_id, task_type, train_data[0], test_data[0], label, feat_sel, estimator, cv_type)
    
    RESULT_PATH = 'results/' + task_id
    if not os.path.exists(RESULT_PATH):
        os.makedirs(RESULT_PATH)

    TRAIN_DATA_PATH = train_data[0]
    TEST_DATA_PATH = test_data[0]

    data_columns = pd.read_csv(TRAIN_DATA_PATH, encoding='gbk').columns
    columns_to_drop = []
    for column in data_columns:
        if column == 'ID':
            columns_to_drop.append(column)
        elif column[:6] == 'LABEL_':
            columns_to_drop.append(column)
        else:
            break
    
    # Instantiate training dataset
    train_X = pd.read_csv(TRAIN_DATA_PATH, encoding='gbk').drop(columns_to_drop, axis=1) # load data file
    train_y = pd.read_csv(TRAIN_DATA_PATH, encoding='gbk')['LABEL_' + label] # load label file
    
    if len(train_data) > 0:
        for i in range(1, len(train_data)):
            train_X_temp = pd.read_csv(train_data[i], encoding='gbk').drop(columns_to_drop, axis=1) # load data file
            train_y_temp = pd.read_csv(train_data[i], encoding='gbk')['LABEL_' + label] # load label file
            train_X = pd.concat([train_X, train_X_temp], axis=0)
            train_y = pd.concat([train_y, train_y_temp], axis=0)
    
    my_train_data = Data(train_X, train_y) # instantiate data class
    my_train_data.data_preprocessing()
    (train_n_samples, train_n_features) = train_X.shape

    # Instantiate testing dataset
    test_X = pd.read_csv(TEST_DATA_PATH, encoding='gbk').drop(columns_to_drop, axis=1) # load data file
    test_y = pd.read_csv(TEST_DATA_PATH, encoding='gbk')['LABEL_' + label] # load label file
    
    if len(test_data) > 0:
        for i in range(1, len(test_data)):
            test_X_temp = pd.read_csv(test_data[i], encoding='gbk').drop(columns_to_drop, axis=1) # load data file
            test_y_temp = pd.read_csv(test_data[i], encoding='gbk')['LABEL_' + label] # load label file
            test_X = pd.concat([test_X, test_X_temp], axis=0)
            test_y = pd.concat([test_y, test_y_temp], axis=0)
    
    my_test_data = Data(test_X, test_y) # instantiate data class
    my_test_data.data_preprocessing()
    (test_n_samples, test_n_features) = test_X.shape

    if cv_type == '10-fold':
        cv = 10
    elif cv_type == '5-fold':
        cv = 5
    elif cv_type == '3-fold':
        cv = 3
    else:
        from sklearn.model_selection import LeaveOneOut
        cv = LeaveOneOut()

    if task_type == "Classification":
        if feat_sel == "Principal Component Analysis":
            my_feat_sel = PCA_Feat_Sel(train_n_samples, train_n_features)
        elif feat_sel == "Analysis of Variance":
            my_feat_sel = ANOVA_Feat_Sel(train_n_samples, train_n_features)
        elif feat_sel == "Recursive Feature Elimination":
            my_feat_sel = RFE_Feat_Sel(train_n_samples, train_n_features)
        elif feat_sel == "None":
            my_feat_sel = None
        
        if estimator == "Support Vector Machine":
            my_model = SVM_CLF()
        elif estimator == "Random Forest":
            my_model = RF_CLF()
        elif estimator == "Linear Discriminative Analysis":
            my_model = LDA_CLF()
        elif estimator == "Logistic Regression":
            my_model = LR_CLF()
        elif estimator == "K Nearest Neighbor":
            my_model = KNN_CLF()

        integrated_clf_model(RESULT_PATH, my_feat_sel, my_model, my_train_data, my_test_data, cv) # run integrated classification model
    elif task_type == "Regression":
        if feat_sel == "Analysis of Variance":
            my_feat_sel = ANOVA_Feat_Sel(train_n_samples, train_n_features)
        elif feat_sel == "None":
            my_feat_sel = None
        
        if estimator == "Support Vector Regression":
            my_model = SVR_RGS()
        elif estimator == "Elastic Net":
            my_model = EN_RGS()
        elif estimator == "Ordinary Least Square":
            my_model = OLS_RGS()
        elif estimator == "Lasso Regression":
            my_model = L1_RGS()
        elif estimator == "Ridge Regression":
            my_model = L2_RGS()
    
        integrated_rgs_model(RESULT_PATH, my_feat_sel, my_model, my_train_data, my_test_data, cv) # run integrated classification model