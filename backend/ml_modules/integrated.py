import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import decimal

import codecs
import csv

from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import permutation_test_score
from sklearn.metrics import roc_auc_score, auc

def integrated_clf_model(feat_sel, model, train_data, test_data, cv):
    starttime = time.time()

    feature_list = train_data.list_features

    if feat_sel == None:
        pipe = Pipeline(steps=[
            (model.name, model.model)
        ])
        pipe_param_grid = model.param_grid
    else:
        pipe = Pipeline(steps=[
            (feat_sel.name, feat_sel.model),
            (model.name, model.model)
        ])
        pipe_param_grid = dict(feat_sel.param_grid, **model.param_grid)

    search = GridSearchCV(pipe, pipe_param_grid, iid=False, cv=cv, return_train_score=False, scoring='accuracy')
    search.fit(train_data.X, train_data.y)

    optimal_score = search.best_score_
    optimal_params = search.best_params_
    optimal_model = search.best_estimator_

    _, _, pvalue_tested = permutation_test_score(
        optimal_model,
        train_data.X,
        train_data.y,
        scoring='accuracy',
        cv=cv,
        n_permutations=100,
        n_jobs=1,
        random_state=0
        )

    print('The best score is', optimal_score)
    print('The corresponding parameter setting is', optimal_params)

    # ========================================
    # Evaluation and Visualization
    # ========================================

    # Optimization Curve and Selected Features (if possible) 
    if feat_sel and feat_sel.name == 'pca':
        # plt.figure()

        results = pd.DataFrame(search.cv_results_)
        components_col = 'param_pca__n_components'
        best_clfs = results.groupby(components_col).apply(lambda g: g.nlargest(1, 'mean_test_score'))
        # best_clfs.plot(x=components_col, y='mean_test_score', yerr='std_test_score')
        
        # plt.ylabel('Classification accuracy (val)')
        # plt.xlabel('n_components')
        # plt.title('Optimization Curve')

        # plt.savefig(result_path + '/' + 'optimization_curve.png', dpi=300)

    elif feat_sel and feat_sel.name == 'anova':
        # plt.figure()

        results = pd.DataFrame(search.cv_results_)
        components_col = 'param_anova__percentile'
        best_clfs = results.groupby(components_col).apply(lambda g: g.nlargest(1, 'mean_test_score'))
        # best_clfs.plot(x=components_col, y='mean_test_score', yerr='std_test_score')
        
        # plt.ylabel('Classification accuracy (val)')
        # plt.xlabel('percentile')
        # plt.title('Optimization Curve')

        # plt.savefig(result_path + '/' + 'optimization_curve.png', dpi=300)

        selector = optimal_model.named_steps['anova'].get_support()
        selected_feature_list = np.array(feature_list)[selector]
        
        if model.name == 'svm':
            selected_weight_list = optimal_model.named_steps['svm'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

        elif model.name == 'rf':
            selected_weight_list = optimal_model.named_steps['rf'].feature_importances_
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

        elif model.name == 'lr':
            selected_weight_list = optimal_model.named_steps['lr'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

        elif model.name == 'lda':
            selected_weight_list = optimal_model.named_steps['lda'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

    elif feat_sel and feat_sel.name == 'rfe':
        # plt.figure()

        results = pd.DataFrame(search.cv_results_)
        components_col = 'param_rfe__n_features_to_select'
        best_clfs = results.groupby(components_col).apply(lambda g: g.nlargest(1, 'mean_test_score'))
        # best_clfs.plot(x=components_col, y='mean_test_score', yerr='std_test_score')
        
        # plt.ylabel('Classification accuracy (val)')
        # plt.xlabel('n_features_to_select')
        # plt.title('Optimization Curve')

        # plt.savefig(result_path + '/' + 'optimization_curve.png', dpi=300)

        selector = optimal_model.named_steps['rfe'].get_support()
        selected_feature_list = np.array(feature_list)[selector]
        
        if model.name == 'svm':
            selected_weight_list = optimal_model.named_steps['svm'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

        elif model.name == 'rf':
            selected_weight_list = optimal_model.named_steps['rf'].feature_importances_
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

        elif model.name == 'lr':
            selected_weight_list = optimal_model.named_steps['lr'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

        elif model.name == 'lda':
            selected_weight_list = optimal_model.named_steps['lda'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

    elif not feat_sel:
        if model.name == 'svm':
            selected_weight_list = optimal_model.named_steps['svm'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': feature_list, 'Weight': selected_weight_list})

        elif model.name == 'rf':
            selected_weight_list = optimal_model.named_steps['rf'].feature_importances_
            feature_weights_list = pd.DataFrame({'Feature': feature_list, 'Weight': selected_weight_list})

        elif model.name == 'lr':
            selected_weight_list = optimal_model.named_steps['lr'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': feature_list, 'Weight': selected_weight_list})

        elif model.name == 'lda':
            selected_weight_list = optimal_model.named_steps['lda'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': feature_list, 'Weight': selected_weight_list})

    # ROC Curve and Confusion Matrix

    from scipy import interp
    from sklearn.metrics import roc_curve, auc

    optimal_model.probability = True
    predictions = optimal_model.predict(test_data.X)
    probas_ = optimal_model.predict_proba(test_data.X)
    
    predictions_list = pd.DataFrame({
        'Original': test_data.y,
        'Predicted': predictions,
        'Proba: Group 0': probas_[:, 0],
        'Proba: Group 1': probas_[:, 1]
    })

    from sklearn.metrics import confusion_matrix
    tn, fp, fn, tp = confusion_matrix(test_data.y, predictions).ravel()
    cnf_accuracy = (tn + tp) / (tn + fp + fn + tp)
    test_accuracy = cnf_accuracy
    cnf_sensitivity = tp / (tp + fn)
    test_sensitivity = cnf_sensitivity
    cnf_specificity = tn / (tn + fp)
    test_specificity = cnf_specificity
    
    # plt.figure()
    mean_fpr = np.linspace(0, 1, 100)
    fpr, tpr, _ = roc_curve(test_data.y, probas_[:, 1])
    roc_auc = auc(fpr, tpr)
    # plt.plot(fpr, tpr, lw=1, alpha=0.3, color='b',
    #         label='AUC = %0.2f' % (roc_auc))
    # plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
    #         label='Chance', alpha=.8)
    # plt.xlim([-0.05, 1.05])
    # plt.ylim([-0.05, 1.05])
    # plt.xlabel('False Positive Rate')
    # plt.ylabel('True Positive Rate')
    # plt.title('Receiver Operating Characteristic')
    # plt.legend(loc="lower right")
    # plt.savefig(result_path + '/' + 'ROC_curve.png', dpi=300)
    
    endtime = time.time()
    runtime = str(endtime - starttime)
    runtime = str(decimal.Decimal(runtime).quantize(decimal.Decimal('0.00'))) + 's'
    print(runtime)

    result_dict = {}
    result_dict['Optimal CV Accuracy'] = optimal_score
    result_dict['Optimal Parameters'] = optimal_params
    result_dict['Permutation Test p-Value'] = pvalue_tested
    result_dict['Test Accuracy'] = test_accuracy
    result_dict['Test Sensitivity'] = test_sensitivity
    result_dict['Test Specificity'] = test_specificity
    result_dict['Area Under Curve'] = roc_auc
    result_dict['Run Time'] = runtime
    result_dict['ROC fpr'] = list(fpr)
    result_dict['ROC tpr'] = list(tpr)
    result_dict['Predictions'] = predictions_list.to_dict('records')
    try:
        result_dict['Feature Weights'] = feature_weights_list.to_dict('records')
    except:
        result_dict['Feature Weights'] = pd.DataFrame({"Error": ["This model doesn\'t support generating feature weights"]}).to_dict('records')
    if feat_sel:
        result_dict['Optimization'] = best_clfs.to_dict('records')

    return result_dict

def integrated_clf_model_notest(feat_sel, model, train_data, cv):
    starttime = time.time()

    feature_list = train_data.list_features

    if feat_sel == None:
        pipe = Pipeline(steps=[
            (model.name, model.model)
        ])
        pipe_param_grid = model.param_grid
    else:
        pipe = Pipeline(steps=[
            (feat_sel.name, feat_sel.model),
            (model.name, model.model)
        ])
        pipe_param_grid = dict(feat_sel.param_grid, **model.param_grid)

    search = GridSearchCV(pipe, pipe_param_grid, iid=False, cv=cv, return_train_score=False, scoring='accuracy')
    search.fit(train_data.X, train_data.y)

    optimal_score = search.best_score_
    optimal_params = search.best_params_
    optimal_model = search.best_estimator_

    _, _, pvalue_tested = permutation_test_score(
        optimal_model,
        train_data.X,
        train_data.y,
        scoring='accuracy',
        cv=cv,
        n_permutations=100,
        n_jobs=1,
        random_state=0
        )

    print('The best score is', optimal_score)
    print('The corresponding parameter setting is', optimal_params)

    # ========================================
    # Evaluation and Visualization
    # ========================================

    # Optimization Curve and Selected Features (if possible) 
    if feat_sel and feat_sel.name == 'pca':
        # plt.figure()

        results = pd.DataFrame(search.cv_results_)
        components_col = 'param_pca__n_components'
        best_clfs = results.groupby(components_col).apply(lambda g: g.nlargest(1, 'mean_test_score'))
        # best_clfs.plot(x=components_col, y='mean_test_score', yerr='std_test_score')
        
        # plt.ylabel('Classification accuracy (val)')
        # plt.xlabel('n_components')
        # plt.title('Optimization Curve')

        # plt.savefig(result_path + '/' + 'optimization_curve.png', dpi=300)

    elif feat_sel and feat_sel.name == 'anova':
        # plt.figure()

        results = pd.DataFrame(search.cv_results_)
        components_col = 'param_anova__percentile'
        best_clfs = results.groupby(components_col).apply(lambda g: g.nlargest(1, 'mean_test_score'))
        # best_clfs.plot(x=components_col, y='mean_test_score', yerr='std_test_score')
        
        # plt.ylabel('Classification accuracy (val)')
        # plt.xlabel('percentile')
        # plt.title('Optimization Curve')

        # plt.savefig(result_path + '/' + 'optimization_curve.png', dpi=300)

        selector = optimal_model.named_steps['anova'].get_support()
        selected_feature_list = np.array(feature_list)[selector]
        
        if model.name == 'svm':
            selected_weight_list = optimal_model.named_steps['svm'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

        elif model.name == 'rf':
            selected_weight_list = optimal_model.named_steps['rf'].feature_importances_
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

        elif model.name == 'lr':
            selected_weight_list = optimal_model.named_steps['lr'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

        elif model.name == 'lda':
            selected_weight_list = optimal_model.named_steps['lda'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

    elif feat_sel and feat_sel.name == 'rfe':
        # plt.figure()

        results = pd.DataFrame(search.cv_results_)
        components_col = 'param_rfe__n_features_to_select'
        best_clfs = results.groupby(components_col).apply(lambda g: g.nlargest(1, 'mean_test_score'))
        # best_clfs.plot(x=components_col, y='mean_test_score', yerr='std_test_score')
        
        # plt.ylabel('Classification accuracy (val)')
        # plt.xlabel('n_features_to_select')
        # plt.title('Optimization Curve')

        # plt.savefig(result_path + '/' + 'optimization_curve.png', dpi=300)

        selector = optimal_model.named_steps['rfe'].get_support()
        selected_feature_list = np.array(feature_list)[selector]
        
        if model.name == 'svm':
            selected_weight_list = optimal_model.named_steps['svm'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

        elif model.name == 'rf':
            selected_weight_list = optimal_model.named_steps['rf'].feature_importances_
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

        elif model.name == 'lr':
            selected_weight_list = optimal_model.named_steps['lr'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

        elif model.name == 'lda':
            selected_weight_list = optimal_model.named_steps['lda'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})
    
    elif not feat_sel:
        if model.name == 'svm':
            selected_weight_list = optimal_model.named_steps['svm'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': feature_list, 'Weight': selected_weight_list})

        elif model.name == 'rf':
            selected_weight_list = optimal_model.named_steps['rf'].feature_importances_
            feature_weights_list = pd.DataFrame({'Feature': feature_list, 'Weight': selected_weight_list})

        elif model.name == 'lr':
            selected_weight_list = optimal_model.named_steps['lr'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': feature_list, 'Weight': selected_weight_list})

        elif model.name == 'lda':
            selected_weight_list = optimal_model.named_steps['lda'].coef_[0]
            feature_weights_list = pd.DataFrame({'Feature': feature_list, 'Weight': selected_weight_list})

    endtime = time.time()
    runtime = str(endtime - starttime)
    runtime = str(decimal.Decimal(runtime).quantize(decimal.Decimal('0.00'))) + 's'
    print(runtime)

    result_dict = {}
    result_dict['Optimal CV Accuracy'] = optimal_score
    result_dict['Optimal Parameters'] = optimal_params
    result_dict['Permutation Test p-Value'] = pvalue_tested
    result_dict['Run Time'] = runtime
    try:
        result_dict['Feature Weights'] = feature_weights_list.to_dict('records')
    except:
        result_dict['Feature Weights'] = pd.DataFrame({"Error": ["This model doesn\'t support generating feature weights"]}).to_dict('records')
    if feat_sel:
        result_dict['Optimization'] = best_clfs.to_dict('records')

    return result_dict

def integrated_rgs_model(feat_sel, model, train_data, test_data, cv):
    starttime = time.time()

    feature_list = train_data.list_features
    
    if feat_sel == None:
        pipe = Pipeline(steps=[
            (model.name, model.model)
        ])
        pipe_param_grid = model.param_grid
    else:
        pipe = Pipeline(steps=[
            (feat_sel.name, feat_sel.model),
            (model.name, model.model)
        ])
        pipe_param_grid = dict(feat_sel.param_grid, **model.param_grid)

    search = GridSearchCV(pipe, pipe_param_grid, iid=False, cv=cv, return_train_score=False, scoring='neg_mean_absolute_error')
    search.fit(train_data.X, train_data.y)

    optimal_score = search.best_score_
    optimal_params = search.best_params_
    optimal_model = search.best_estimator_
    
    print('The best score is', search.best_score_)
    print('The corresponding parameter setting is', search.best_params_)

    # Optimization Curve and Selected Features (if possible) 
    if feat_sel and feat_sel.name == 'anova':

        results = pd.DataFrame(search.cv_results_)
        components_col = 'param_anova__percentile'
        best_clfs = results.groupby(components_col).apply(lambda g: g.nlargest(1, 'mean_test_score'))

        selector = optimal_model.named_steps['anova'].get_support()
        selected_feature_list = np.array(feature_list)[selector]
        
        selected_weight_list = optimal_model.named_steps[model.name].coef_[0]
        feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

    elif not feat_sel:
        selected_weight_list = optimal_model.named_steps[model.name].coef_[0]
        feature_weights_list = pd.DataFrame({'Feature': feature_list, 'Weight': selected_weight_list})

    predictions = optimal_model.predict(test_data.X)
    original = test_data.y
    predictions_list = pd.DataFrame({'Original': original, 'Predicted': predictions})

    import seaborn as sns
    import matplotlib.pyplot as plt
    import scipy
    pearson_r, pearson_p = scipy.stats.pearsonr(original, predictions)
    print('The pearsonr and pearsonp are:', pearson_r, 'and', pearson_p)
    # g = sns.jointplot(x='Original', y='Predicted', data=original_predicted, kind='reg', label='pearson_r = %.2f, pearson_p = %.4f' % (pearson_r, pearson_p))
    # plt.legend(loc='upper right')
    # g.savefig(result_path + '/' + 'Original_Predicted_Correlation.png', dpi=300)

    endtime = time.time()
    runtime = str(endtime - starttime)
    runtime = str(decimal.Decimal(runtime).quantize(decimal.Decimal('0.00'))) + 's'
    print(runtime)

    result_dict = {}
    result_dict['Optimal CV MAE'] = optimal_score
    result_dict['Optimal Parameters'] = optimal_params
    result_dict['Test Pearson r'] = pearson_r
    result_dict['Test Pearson p'] = pearson_p
    result_dict['Run Time'] = runtime
    result_dict['Predictions'] = predictions_list.to_dict('records')
    try:
        result_dict['Feature Weights'] = feature_weights_list.to_dict('records')
    except:
        result_dict['Feature Weights'] = pd.DataFrame({"Error": ["This model doesn\'t support generating feature weights"]}).to_dict('records')
    if feat_sel:
        result_dict['Optimization'] = best_clfs.to_dict('records')

    return result_dict

def integrated_rgs_model_notest(feat_sel, model, train_data, cv):
    starttime = time.time()

    feature_list = train_data.list_features
    
    if feat_sel == None:
        pipe = Pipeline(steps=[
            (model.name, model.model)
        ])
        pipe_param_grid = model.param_grid
    else:
        pipe = Pipeline(steps=[
            (feat_sel.name, feat_sel.model),
            (model.name, model.model)
        ])
        pipe_param_grid = dict(feat_sel.param_grid, **model.param_grid)

    search = GridSearchCV(pipe, pipe_param_grid, iid=False, cv=cv, return_train_score=False, scoring='neg_mean_absolute_error')
    search.fit(train_data.X, train_data.y)

    optimal_score = search.best_score_
    optimal_params = search.best_params_
    optimal_model = search.best_estimator_
    
    print('The best score is', search.best_score_)
    print('The corresponding parameter setting is', search.best_params_)

    # Optimization Curve and Selected Features (if possible) 
    if feat_sel and feat_sel.name == 'anova':

        results = pd.DataFrame(search.cv_results_)
        components_col = 'param_anova__percentile'
        best_clfs = results.groupby(components_col).apply(lambda g: g.nlargest(1, 'mean_test_score'))

        selector = optimal_model.named_steps['anova'].get_support()
        selected_feature_list = np.array(feature_list)[selector]
        
        selected_weight_list = optimal_model.named_steps[model.name].coef_[0]
        feature_weights_list = pd.DataFrame({'Feature': selected_feature_list, 'Weight': selected_weight_list})

    elif not feat_sel:
        selected_weight_list = optimal_model.named_steps[model.name].coef_[0]
        feature_weights_list = pd.DataFrame({'Feature': feature_list, 'Weight': selected_weight_list})

    endtime = time.time()
    runtime = str(endtime - starttime)
    runtime = str(decimal.Decimal(runtime).quantize(decimal.Decimal('0.00'))) + 's'
    print(runtime)

    result_dict = {}
    result_dict['Optimal CV MAE'] = optimal_score
    result_dict['Optimal Parameters'] = optimal_params
    result_dict['Run Time'] = runtime
    try:
        result_dict['Feature Weights'] = feature_weights_list.to_dict('records')
    except:
        result_dict['Feature Weights'] = pd.DataFrame({"Error": ["This model doesn\'t support generating feature weights"]}).to_dict('records')
    if feat_sel:
        result_dict['Optimization'] = best_clfs.to_dict('records')

    return result_dict
