from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.model_selection import train_test_split
from util import CommonUtil
# 加载样本数据集
if __name__=='__main__':
    n = 180
    csv_file = CommonUtil.read_csv('C:/Users/yuzhe/Desktop/OptionAnalysis/files/files_' + n.__str__() + 'min/REDUCED_FEATURE_VECTOR_' + n.__str__() + '.csv')
    dataNum = len(csv_file)
    featureNum = len(csv_file[0])-1
    print("Dimension of feature", featureNum)
    dataMat = np.array(csv_file)
    X = dataMat[1:, 0:featureNum].astype(float)
    y = dataMat[1:, featureNum].astype(float)
    print(dataNum)
    for i in range(dataNum-1):
        if y[i] == 0: y[i] = 0
        elif y[i]<0: y[i] = -1
        else:y[i]= 1

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0) # 数据集分割
    pipe_scv = Pipeline([('scl', StandardScaler()), ('clf', SVC(random_state=1))])

    param_range = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
    param_grid = [{'clf_C': param_range, 'clf_kernel': ['linear']},
          {'clf_C': param_range, 'clf_gamma': param_range, 'clf_kernel': ['rbf']}]

    gs = GridSearchCV(estimator = pipe_scv ,
              param_grid=param_grid,
              scoring='accuracy',
              cv=10,
              n_jobs=-1)

    gs = gs.fit(X_train, y_train)
    print(gs.best_score_)
    print(gs.best_params_)

    # 获取最优模型进行评估
    clf = gs.best_estimator_
    clf.fit(X_train, y_train)
    y_pre = clf.score(X_test, y_test)
    print(y_pre)
