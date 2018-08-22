#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from util import CommonUtil
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Load data
file_dir = 'C:/Users/yuzhe/Desktop/OptionAnalysis/files/'
csv_file = CommonUtil.read_csv(file_dir + 'TestUSDIndex.csv')
dataNum = len(csv_file)
print("数据量", dataNum)
featureNum = len(csv_file[0])-2
print("特征的维度", featureNum)

dataMat = np.array(csv_file)
X = dataMat[1:, 1: featureNum+1].astype(float)
print("X[0]", X[0])
y = dataMat[1:, featureNum+1].astype(float)
print("y[0]", y[0])


# Split the data into training/testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Create linear regression object
clf = linear_model.LinearRegression()
# Train the model using the training sets
clf.fit(X_train, y_train)
# Make predictions using the testing set
y_pred = clf.predict(X_test)

# The coefficients
print('回归系数: \n', clf.coef_)
print('截距: \n',clf.intercept_)

print("Mean Absolute error:", mean_absolute_error(y_test, y_pred))
# The mean squared error
print("Mean squared error:", mean_squared_error(y_test,y_pred))
# Explained variance score: 1 is perfect prediction
print('模型得分: %.2f',clf.score(X_test, y_test))
print('R2 score: %.2f' % r2_score(y_test, y_pred))



y_pred = clf.predict(X_test)
y_pred =y_pred.reshape(len(y_pred),1)
y_test =y_test.reshape(len(y_test),1)


# write_csv('C:/Users/yuzhe/Desktop/OptionAnalysis/files/result.csv', X_test)
CommonUtil.write_csv('C:/Users/yuzhe/Desktop/OptionAnalysis/files/y_test.csv', y_test)
CommonUtil.write_csv('C:/Users/yuzhe/Desktop/OptionAnalysis/files/y_pred.csv', y_pred)


###############################
# 用predic预测，这里预测输入x对应的值，进行画线
X_test = [i for i in range(len(y_test))]

plt.scatter(X_test, y_test, color='black')
plt.plot(X_test,y_pred, color='blue',
         linewidth=2)
plt.xticks(())
plt.yticks(np.linspace(6.5, 7, 10))
plt.show()
