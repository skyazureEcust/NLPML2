# ==============基于XGBoost 进行舆情分析分类================

import xgboost as xgb
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from util import CommonUtil
import numpy as np
import warnings
warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)


def convert2class(y, dataNum):
    print(dataNum)
    for i in range(dataNum - 1):
        if y[i] == 0:
            y[i] = 0
        elif y[i] < 0:
            y[i] = -1
        else:
            y[i] = 1
    return y


if __name__ == "__main__":
    # 加载样本数据集
    n = 120
    csv_file = CommonUtil.read_csv('../files/files_train/files_' + str(n) + 'min/REDUCED_FEATURE_VECTOR_' +
                                   str(n) + '.csv')
    dataNum = len(csv_file)
    featureNum = len(csv_file[0])-1
    print("Dimension of feature", featureNum)
    dataMat = np.array(csv_file)
    X = dataMat[1:, 0:featureNum].astype(float)
    y = dataMat[1:, featureNum].astype(float)
    y = convert2class(y, dataNum) # 转换为类别

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0) # 数据集分割

    # 训练模型
    model = xgb.XGBClassifier(max_depth=3, learning_rate=0.1, n_estimators=80, silent=True, objective='liner:logistic')
    model.fit(X_train, y_train)

    # 对测试集进行预测
    y_pred = model.predict(X_test)
    # 计算准确率
    print("accuarcy:", accuracy_score(y_test, y_pred))

    # 显示重要特征
    feature_importance = model.feature_importances_
    # make importances relative to max importance
    feature_importance = 100.0 * (feature_importance / feature_importance.max())
    sorted_idx = np.argsort(feature_importance)
    # print(sorted_idx)
    # print(feature_importance[sorted_idx])

    pos = np.arange(sorted_idx.shape[0]) + .5
    plt.barh(pos, feature_importance[sorted_idx], align='center')
    plt.yticks(pos, dataMat[0][sorted_idx])
    plt.xlabel('Relative Importance')
    plt.title('Variable Importance')
    plt.show()

    '''
    # 网格搜索调优超参
    from sklearn.model_selection import GridSearchCV
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    
    pipe_lr = Pipeline([('scl',StandardScaler()),('clf',LogisticRegression(random_state=0))])
    param_range=[0.0001,0.001,0.01,0.1,1,10,100,1000]
    param_penalty=['l1','l2']
    param_grid=[{'clf__C':param_range,'clf__penalty':param_penalty}]
    gs = GridSearchCV(estimator=pipe_lr, param_grid=param_grid, scoring='f1', cv=10, n_jobs=-1)
    gs = gs.fit(X_train,y_train)
    print(gs.best_score_)
    print(gs.best_params_)
    '''
