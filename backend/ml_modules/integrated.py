import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

import codecs
import csv

from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, auc

def integrated(result_path, feat_sel, model, train_data, test_data, k):
    
    pipe = Pipeline(steps=[
        (feat_sel.name, feat_sel.model),
        (model.name, model.model)
    ])
    pipe_param_grid = dict(feat_sel.param_grid, **model.param_grid)

    search = GridSearchCV(pipe, pipe_param_grid, iid=False, cv=k, return_train_score=False, scoring='accuracy')
    search.fit(train_data.X, train_data.y)

    optimal_score = search.best_score_
    optimal_params = search.best_params_
    optimal_model = search.best_estimator_

    print('The best score is', optimal_score)
    print('The corresponding parameter setting is', optimal_params)

    # ========================================
    # Evaluation and Visualization
    # ========================================

    # Optimization Curve and Selected Features (if possible) 
    if feat_sel.name == 'pca':
        plt.figure()

        results = pd.DataFrame(search.cv_results_)
        components_col = 'param_pca__n_components'
        best_clfs = results.groupby(components_col).apply(lambda g: g.nlargest(1, 'mean_test_score'))
        best_clfs.plot(x=components_col, y='mean_test_score', yerr='std_test_score')
        
        plt.ylabel('Classification accuracy (val)')
        plt.xlabel('n_components')
        plt.title('Optimization Curve')

        plt.savefig(result_path + '/' + 'optimization_curve.png', dpi=300)

    elif feat_sel.name == 'anova':
        plt.figure()

        results = pd.DataFrame(search.cv_results_)
        components_col = 'param_anova__percentile'
        best_clfs = results.groupby(components_col).apply(lambda g: g.nlargest(1, 'mean_test_score'))
        best_clfs.plot(x=components_col, y='mean_test_score', yerr='std_test_score')
        
        plt.ylabel('Classification accuracy (val)')
        plt.xlabel('percentile')
        plt.title('Optimization Curve')

        plt.savefig(result_path + '/' + 'optimization_curve.png', dpi=300)

    elif feat_sel.name == 'rfe':
        plt.figure()

        results = pd.DataFrame(search.cv_results_)
        components_col = 'param_rfe__n_features_to_select'
        best_clfs = results.groupby(components_col).apply(lambda g: g.nlargest(1, 'mean_test_score'))
        best_clfs.plot(x=components_col, y='mean_test_score', yerr='std_test_score')
        
        plt.ylabel('Classification accuracy (val)')
        plt.xlabel('n_features_to_select')
        plt.title('Optimization Curve')

        plt.savefig(result_path + '/' + 'optimization_curve.png', dpi=300)

        selector = search.best_estimator_.named_steps['rfe'].fit(train_data.X, train_data.y)
        list_selected_features = []
        for i, feat in enumerate(selector.support_):
            if feat == True:
                list_selected_features.append(train_data.list_features[i])
        print(list_selected_features[:50])
    
    # ROC Curve and Confusion Matrix

    from scipy import interp
    from sklearn.metrics import roc_curve, auc

    optimal_model.probability = True
    predictions = optimal_model.predict(test_data.X)
    probas_ = optimal_model.predict_proba(test_data.X)

    from sklearn.metrics import confusion_matrix
    tn, fp, fn, tp = confusion_matrix(test_data.y, predictions).ravel()
    cnf_accuracy = (tn + tp) / (tn + fp + fn + tp)
    test_accuracy = cnf_accuracy
    cnf_sensitivity = tp / (tp + fn)
    test_sensitivity = cnf_sensitivity
    cnf_specificity = tn / (tn + fp)
    test_specificity = cnf_specificity
    
    plt.figure()
    mean_fpr = np.linspace(0, 1, 100)
    fpr, tpr, _ = roc_curve(test_data.y, probas_[:, 1])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, lw=1, alpha=0.3, color='b',
            label='AUC = %0.2f' % (roc_auc))
    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
            label='Chance', alpha=.8)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.savefig(result_path + '/' + 'ROC_curve.png', dpi=300)

    results_csv = codecs.open(result_path + '/' + 'results.csv', 'w+', encoding='gbk')
    writer = csv.writer(results_csv, delimiter=',')
    writer.writerow(['Item', 'Value'])
    writer.writerow(['Optimal CV Accuracy', optimal_score])
    writer.writerow(['Optimal Parameters', optimal_params])
    writer.writerow(['Test Accuracy', test_accuracy])
    writer.writerow(['Test Sensitivity', test_sensitivity])
    writer.writerow(['Test Specificity', test_specificity])
    writer.writerow(['Area Under Curve', roc_auc])
    results_csv.close()