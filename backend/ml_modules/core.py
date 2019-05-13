import sys
import time
import pandas as pd
from .acquisition import Data
from .models import *
from .integrated import *

def test_task():
    X = pd.read_csv('data/fMRI_90.csv', encoding='gbk').drop(['ID', 'GROUP'], axis=1) # load data file
    y = pd.read_csv('data/fMRI_90.csv', encoding='gbk').GROUP # load label file
    my_data = Data(X, y) # instantiate data class
    my_data.data_preprocessing()
    (n_samples, n_features) = X.shape

    my_model = SVM_CLF()
    my_feat_sel = PCA_Feat_Sel(n_samples, n_features)
    integrated('', my_feat_sel, my_model, my_data, 10) # run integrated classification model