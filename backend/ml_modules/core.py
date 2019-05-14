import os
import sys
import time
import pandas as pd
from .acquisition import Data
from .models import *
from .integrated import *

def test_task(task_id, task_type, train_data, test_data, label, feat_sel, estimator, cv_type):
    print(task_id, task_type, train_data, test_data, label, feat_sel, estimator, cv_type)
    
    RESULT_DIR = 'results/' + task_id
    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)

    TRAIN_DATA_PATH = train_data[0]
    TEST_DATA_PATH = test_data[0]
    
    X = pd.read_csv(TRAIN_DATA_PATH, encoding='gbk').drop(['ID', 'GROUP'], axis=1) # load data file
    y = pd.read_csv(TRAIN_DATA_PATH, encoding='gbk').GROUP # load label file
    my_data = Data(X, y) # instantiate data class
    my_data.data_preprocessing()
    (n_samples, n_features) = X.shape

    my_model = SVM_CLF()
    my_feat_sel = PCA_Feat_Sel(n_samples, n_features)
    integrated('', my_feat_sel, my_model, my_data, 10) # run integrated classification model