#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from sklearn import ensemble
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from util import CommonUtil
from sklearn.model_selection import train_test_split


# #############################################################################
# 导入数据
# 加载数据集

file_dir = 'C:/Users/yuzhe/Desktop/OptionAnalysis/files/'
csv_file = CommonUtil.read_csv(file_dir + 'TestUSDIndex.csv')
dataNum = len(csv_file)
featureNum = len(csv_file[0])-2
print("特征的维度", featureNum)
dataMat = np.array(csv_file)
X = dataMat[1:, 1: featureNum].astype(float)
y = dataMat[1:, featureNum].astype(float)

'''
# 将y标签的增长率转化为增、跌、不变三种标签
for i in range(dataNum-1):
    if y[i] == 0: y[i] = 0
    elif y[i]<0: y[i] = -1
    else:y[i]= 1
'''
# 数据集分
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, shuffle=False)
print('测试集的数量：', len(X_test))

# #############################################################################
# 训练回归模型
print("开始训练...")
params = {'n_estimators': 80, 'max_depth': 4, 'min_samples_split': 2,
          'learning_rate': 0.1, 'loss': 'huber'}
clf = ensemble.GradientBoostingRegressor(**params)
clf.fit(X_train, y_train)
y_pre = clf.predict(X_test)
mse = mean_squared_error(y_test, y_pre)
mae = mean_absolute_error(y_test, y_pre)
# print('每次训练的得分：', clf.train_score_)
# print("特征的重要性:", clf.feature_importances_)

# 计算模型的误差
print("GDBT的均方误差MSE: %.4f" % mse)
print("GDBT的均方误差MAE: %.4f" % mae)
print('GDBT的R2误差: %.2f' % r2_score(y_test, y_pre))
# plt.plot(np.arange(100), clf.train_score_, 'b-')  # 绘制随着训练次数增加，训练得分的变化
# plt.show()

# #######################################################################
# 显示训练集和测试集的训练异常
test_score = np.zeros((params['n_estimators'],), dtype=np.float64)
for i, y_pred in enumerate(clf.staged_predict(X_test)):
    test_score[i] = clf.loss_(y_test, y_pred)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title('Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, clf.train_score_, 'b-',
         label='Training Set Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-',
         label='Test Set Deviance')
plt.legend(loc='upper right')
plt.xlabel('Boosting Iterations')
plt.ylabel('Deviance')

# #############################################################################
# 显示模型中特征的重要程度f
feature_importance = clf.feature_importances_
# make importances relative to max importance
# feature_importance = 100.0 * (feature_importance / feature_importance.max())
sorted_idx = np.argsort(feature_importance)
# print(sorted_idx)
# print(feature_importance[sorted_idx])
pos = np.arange(sorted_idx.shape[0]) + .5
plt.subplot(1, 2, 2)
plt.barh(pos, feature_importance[sorted_idx], align='center')
plt.yticks(pos,  dataMat[0][sorted_idx])
plt.xlabel('Relative Importance')
plt.title('Variable Importance')
plt.show()

# #############################################################################
'''
# 显示测试集预测的结果的人民币汇率的涨跌趋势
test_result = np.zeros(len(X_test), dtype=np.float64)

for i in range(len(X_test)):
    if i == 0: test_result[i]= clf.predict(X_test[i].reshape(1,-1))
    else: test_result[i] = clf.predict(X_test[i].reshape(1,-1))+test_result[i-1]

print('预测结果：\n',test_result)
plt.figure(figsize=(12, 6))
plt.title('result')
plt.plot(np.arange(len(X_test)) + 1, test_result, 'r-',
         label='Test Set Result')
plt.legend(loc='upper right')
plt.xlabel('Test Sample')
plt.ylabel('Growth Rate')
plt.show()
'''

