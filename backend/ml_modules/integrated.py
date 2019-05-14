import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, auc

def integrated(result_path, feat_sel, model, data, k):
    
    pipe = Pipeline(steps=[
        (feat_sel.name, feat_sel.model),
        (model.name, model.model)
    ])
    pipe_param_grid = dict(feat_sel.param_grid, **model.param_grid)

    search = GridSearchCV(pipe, pipe_param_grid, iid=False, cv=k, return_train_score=False, scoring='accuracy')
    search.fit(data.X, data.y)

    print('The best score is', search.best_score_)
    print('The corresponding parameter setting is', search.best_params_)

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

        plt.savefig(result_path + '/' + time.strftime('%y%m%d') + '_optimization_curve_' + feat_sel.name + '_' + model.name + '_' + data.name + '.png', dpi=300)

    elif feat_sel.name == 'anova':
        plt.figure()

        results = pd.DataFrame(search.cv_results_)
        components_col = 'param_anova__percentile'
        best_clfs = results.groupby(components_col).apply(lambda g: g.nlargest(1, 'mean_test_score'))
        best_clfs.plot(x=components_col, y='mean_test_score', yerr='std_test_score')
        
        plt.ylabel('Classification accuracy (val)')
        plt.xlabel('percentile')
        plt.title('Optimization Curve')

        plt.savefig(result_path + '/' + time.strftime('%y%m%d') + '_optimization_curve_' + feat_sel.name + '_' + model.name + '_' + data.name + '.png', dpi=300)

    elif feat_sel.name == 'rfe':
        plt.figure()

        results = pd.DataFrame(search.cv_results_)
        components_col = 'param_rfe__n_features_to_select'
        best_clfs = results.groupby(components_col).apply(lambda g: g.nlargest(1, 'mean_test_score'))
        best_clfs.plot(x=components_col, y='mean_test_score', yerr='std_test_score')
        
        plt.ylabel('Classification accuracy (val)')
        plt.xlabel('n_features_to_select')
        plt.title('Optimization Curve')

        plt.savefig(result_path + '/' + time.strftime('%y%m%d') + '_optimization_curve_' + feat_sel.name + '_' + model.name + '_' + data.name + '.png', dpi=300)

        selector = search.best_estimator_.named_steps['rfe'].fit(data.X, data.y)
        list_selected_features = []
        for i, feat in enumerate(selector.support_):
            if feat == True:
                list_selected_features.append(data.list_features[i])
        print(list_selected_features[:50])
    
    # ROC Curve and Confusion Matrix
    optimal_model = search.best_estimator_

    from scipy import interp
    from sklearn.metrics import roc_curve, auc

    list_weight_vectors = []
    accuracy = []
    sensitivity = []
    specificity = []
    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)
    dict_split_data = data.data_k_split(k)
    optimal_model.probability = True
    c = 0
    plt.figure()
    for i in range(1, k+1):
        train_X = dict_split_data['train_X_'+str(i)]
        train_y = dict_split_data['train_y_'+str(i)]
        test_X = dict_split_data['test_X_'+str(i)]
        test_y = dict_split_data['test_y_'+str(i)]

        optimal_model.fit(train_X, train_y)
        predictions = optimal_model.predict(test_X)

        probas_ = optimal_model.predict_proba(test_X)

        from sklearn.metrics import confusion_matrix
        tn, fp, fn, tp = confusion_matrix(test_y, predictions).ravel()
        cnf_accuracy = (tn + tp) / (tn + fp + fn + tp)
        accuracy.append(cnf_accuracy)
        cnf_sensitivity = tp / (tp + fn)
        sensitivity.append(cnf_sensitivity)
        cnf_specificity = tn / (tn + fp)
        specificity.append(cnf_specificity)

        fpr, tpr, _ = roc_curve(test_y, probas_[:, 1])
        tprs.append(interp(mean_fpr, fpr, tpr))
        tprs[-1][0] = 0.0
        roc_auc = auc(fpr, tpr)
        aucs.append(roc_auc)
        plt.plot(fpr, tpr, lw=1, alpha=0.3,
                label='ROC fold %d (AUC = %0.2f)' % (c, roc_auc))

        c += 1

    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
            label='Chance', alpha=.8)

    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0

    import codecs
    import csv
    roc_to_csv = codecs.open(result_path + '/' + time.strftime('%y%m%d') + '_fpr_tpr_' + feat_sel.name + '_' + model.name + '_' + data.name + '.csv', 'w+', encoding='gbk')
    writer = csv.writer(roc_to_csv, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(mean_fpr)
    writer.writerow(mean_tpr)
    roc_to_csv.close()

    mean_auc = auc(mean_fpr, mean_tpr)
    std_auc = np.std(aucs)
    print('The mean auc is:', mean_auc)
    print('The std auc is:', std_auc)
    plt.plot(mean_fpr, mean_tpr, color='b',
            label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
            lw=2, alpha=.8)

    std_tpr = np.std(tprs, axis=0)
    tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
    tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
    plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                    label=r'$\pm$ 1 std. dev.')

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.savefig(result_path + '/' + time.strftime('%y%m%d') + '_ROC_curve_' + feat_sel.name + '_' + model.name + '_' + data.name + '.png', dpi=300)

    mean_accuracy = sum(accuracy) / len(accuracy)
    print('The mean accuracy is %.2f' % mean_accuracy)
    mean_sensitivity = sum(sensitivity) / len(sensitivity)
    print('The mean sensitivity is %.2f' % mean_sensitivity)
    mean_specificity = sum(specificity) / len(specificity)
    print('The mean specificity is %.2f' % mean_specificity)