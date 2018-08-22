import numpy as np
import xgboost as xgb
from sklearn.model_selection import cross_val_score
from util import CommonUtil
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.metrics import accuracy_score,recall_score
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

# #############################################################################
# 加载数据集

# 加载样本数据集
n = 120
csv_file = CommonUtil.read_csv('../files/files_train/files_' + str(n) +
                               'min/REDUCED_FEATURE_VECTOR_' + str(n) + '.csv')
dataNum = len(csv_file)
featureNum = len(csv_file[0])-1
print("特征的维度", featureNum)
dataMat = np.array(csv_file)
X = dataMat[1:, 0:featureNum].astype(float)
y = dataMat[1:, featureNum].astype(float)

print('数据量', dataNum)
for i in range(dataNum-1):
    if y[i] == 0:
        y[i] = 0
    elif y[i] < 0:
        y[i] = -1
    else:
        y[i] = 1
print(y)


# 拆分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, shuffle=False) # 数据集分割

# ==============XGBOOST 分类================
clf = xgb.XGBClassifier(max_depth=3, learning_rate=0.1, n_estimators=80, silent=True, objective='binary:logistic')
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
# 计算准确率
print("XGBOOST准确率：", accuracy_score(y_test, y_pred))


#
# ==============GBDT分类================
# 创建模型
clf = GradientBoostingClassifier(n_estimators=80, learning_rate=0.1,max_depth=3, random_state=0)
# 交叉验证
# scores = cross_val_score(clf, X, y)
# print ('GBDT准确率：',scores.mean())

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print("GBDT准确率:", accuracy_score(y_test, y_pred))

# print("precision_score:", metrics.precision_score(y_test, y_pred))
# print("recall_score:", metrics.recall_score(y_test, y_pred))
# print("f1_score:", metrics.f1_score(y_test, y_pred))


# ==============决策树 分类================
# 创建模型
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(max_depth=3, min_samples_split=2, random_state=0)
# 交叉验证
# scores = cross_val_score(clf, X, y)
# print('决策树准确率：',scores.mean())

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print("决策树准确率:", accuracy_score(y_test, y_pred))
#print("决策树召回率:",recall_score(y_test, y_pred, labels=None, pos_label=1,average='binary', sample_weight=None))

# ==============随机森林 分类================
# 创建模型
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=80,max_features=2)
clf = clf.fit(X, y)
# 交叉验证
scores = cross_val_score(clf, X, y)
print('随机森林准确率：',scores.mean())


# ==============极限随机树 分类================
# 创建模型
from sklearn.ensemble import ExtraTreesClassifier
clf = ExtraTreesClassifier(n_estimators=10, max_depth=None,min_samples_split=2, random_state=0)
clf = clf.fit(X, y)
# 交叉验证
scores = cross_val_score(clf, X, y)
print('极限随机树准确率：',scores.mean())
# print('模型中各属性的重要程度：',clf.feature_importances_)

'''
print("accuracy_score:", accuracy_score(y_true, y_pred))
print("precision_score:", metrics.precision_score(y_true, y_pred))
print("recall_score:", metrics.recall_score(y_true, y_pred))
print("f1_score:", metrics.f1_score(y_true, y_pred))
print("f0.5_score:", metrics.fbeta_score(y_true, y_pred, beta=0.5))
'''

