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

    
    X = pd.read_csv(TRAIN_DATA_PATH, encoding='gbk').drop(['ID', 'LABEL'], axis=1) # load data file
    y = pd.read_csv(TRAIN_DATA_PATH, encoding='gbk').LABEL # load label file
    
    if len(train_data) > 0:
        for i in range(1, len(train_data)):
            X_temp = pd.read_csv(train_data[i], encoding='gbk').drop(['ID', 'LABEL'], axis=1) # load data file
            y_temp = pd.read_csv(train_data[i], encoding='gbk').LABEL # load label file
            X = pd.concat([X, X_temp], axis=0)
            y = pd.concat([y, y_temp], axis=0)
    
    my_data = Data(X, y) # instantiate data class
    my_data.data_preprocessing()
    (n_samples, n_features) = X.shape

    if feat_sel == "Principal Component Analysis":
        my_feat_sel = PCA_Feat_Sel(n_samples, n_features)
    elif feat_sel == "ANOVA":
        my_feat_sel = ANOVA_Feat_Sel(n_samples, n_features)
    elif feat_sel == "Recursive Feature Elimination":
        my_feat_sel = RFE_Feat_Sel(n_samples, n_features)
    
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
    
    integrated(RESULT_PATH, my_feat_sel, my_model, my_data, 10) # run integrated classification model