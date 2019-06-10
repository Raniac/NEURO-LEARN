"""
Models including feature selection models, classifiers, and regressors.
"""

# ========================================
# Feature Selection Models
# ========================================

class PCA_Feat_Sel():
    def __init__(self, n_samples, n_features):
        from sklearn.decomposition import PCA
        self.model = PCA(
            n_components=10,
            random_state=1
        )
        self.name = 'pca'
        step = min(n_samples, n_features) // 20
        self.param_grid = {
            'pca__n_components': list(range(11, min(n_samples, n_features)-50, step))
        }

class ANOVA_Feat_Sel():
    def __init__(self, n_samples, n_features):
        from sklearn.feature_selection import f_classif, SelectPercentile
        self.model = SelectPercentile(
            percentile=5,
        )
        self.name = 'anova'
        self.param_grid = {
            'anova__percentile': list(range(5, 101, 5))
        }

class RFE_Feat_Sel():
    def __init__(self, n_samples, n_features):
        from sklearn.feature_selection import RFE
        from sklearn.svm import SVC
        from sklearn.linear_model import LogisticRegression
        estimator = SVC(kernel='linear')
        self.model = RFE(
            estimator, n_features_to_select=300, step=100, verbose=False
        )
        self.name = 'rfe'
        step = n_features // 20
        self.param_grid = {
            'rfe__n_features_to_select': list(range(10, n_features, step))
        }

# ========================================
# Classifiers
# ========================================

class SVM_CLF():
    def __init__(self):
        from sklearn.svm import SVC
        self.model = SVC(
            C=1.0,
            kernel='linear',
            probability=True
        )
        self.name = 'svm'
        self.param_grid = {
            'svm__C': [1]
        }

class RF_CLF():
    def __init__(self):
        from sklearn.ensemble import RandomForestClassifier
        self.model = RandomForestClassifier(
            bootstrap=True,
            criterion='entropy',
            max_depth=10,
            min_samples_leaf=5,
            min_samples_split=5,
            n_estimators=10,
            random_state=0
        )
        self.name = 'rf'
        self.param_grid = {
            "rf__max_depth": [2, 3, 4, 5],
            "rf__min_samples_split": [5],
            "rf__min_samples_leaf": [10],
            "rf__bootstrap": [True],
            "rf__criterion": ["entropy"],
            "rf__n_estimators": list(range(50, 51, 10))
        }

class LR_CLF():
    def __init__(self):
        from sklearn.linear_model import LogisticRegression
        self.model = LogisticRegression(
            random_state=0,
            solver='lbfgs',
            multi_class='multinomial'
        )
        self.name = 'lr'
        self.param_grid = {
            'lr__solver': ['newton-cg', 'lbfgs', 'sag', 'saga'],
            'lr__multi_class': ['ovr', 'multinomial']
        }

class LDA_CLF():
    def __init__(self):
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
        self.model = LinearDiscriminantAnalysis(
            solver='svd'
        )
        self.name = 'lda'
        self.param_grid = {
            'lda__solver':['svd', 'lsqr']
        }

class KNN_CLF():
    def __init__(self):
        from sklearn.neighbors import KNeighborsClassifier
        self.model = KNeighborsClassifier(
            n_neighbors=10,
            algorithm='auto',
            p=1
        )
        self.name = 'knn'
        self.param_grid = {
            'knn__n_neighbors': [5, 7, 9],
            'knn__algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
            'knn__p': [1, 2, 3]
        }

# ========================================
# Regressors
# ========================================

class OLS_RGS():
    def __init__(self):
        from sklearn.linear_model import LinearRegression
        self.model = LinearRegression()
        self.name = 'ols'
        self.param_grid = {}

class L1_RGS():
    def __init__(self):
        from sklearn.linear_model import Lasso
        self.model = Lasso()
        self.name = 'l1'
        self.param_grid = {
            'l1__alpha': list(range(4, 21, 2))
        }

class L2_RGS():
    def __init__(self):
        from sklearn.linear_model import Ridge
        self.model = Ridge()
        self.name = 'l2'
        self.param_grid = {
            'l2__alpha': list(range(0, 21, 2))
        }

class SVR_RGS():
    def __init__(self):
        from sklearn.svm import SVR
        self.model = SVR(kernel='linear')
        self.name = 'svr'
        self.param_grid = {
            'svr__C': [0.01, 0.1, 1, 10]
        }

class EN_RGS():
    def __init__(self):
        from sklearn.linear_model import ElasticNet
        self.model = ElasticNet()
        self.name = 'en'
        self.param_grid = {
            'en__alpha': list(range(4, 21, 2)),
            'en__l1_ratio': [0.1, 0.3, 0.5, 0.7, 0.9]
        }