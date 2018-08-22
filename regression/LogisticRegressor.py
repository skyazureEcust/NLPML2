#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
from util import CommonUtil
from sklearn.model_selection import train_test_split
# Load data
# file_dir = 'C:/Users/yuzhe/Desktop/OptionAnalysis/files/'
# csv_file = read_csv(file_dir + 'TestUSDIndex.csv')
# dataNum = len(csv_file)
# print("数据量", dataNum)
# featureNum = len(csv_file[0])-2
# print("特征的维度", featureNum)
#
# dataMat = np.array(csv_file)
# X = dataMat[1:, 1: featureNum+1].astype(float)
# print("X[0]", X[0])
# y = dataMat[1:, featureNum+1].astype(float)
# print("y[0]", y[0])


def convert2class(y, dataNum):
    print(dataNum)
    for i in range(dataNum - 1):
        if y[i] == 0: y[i] = 0
        elif y[i] < 0: y[i] = -1
        else: y[i] = 1
    return y


if __name__ == "__main__":
    # 加载样本数据集
    n = 120
    csv_file = CommonUtil.read_csv('C:/Users/yuzhe/Desktop/OptionAnalysis/files/files_'
                        + n.__str__()
                        + 'min/REDUCED_FEATURE_VECTOR_' + n.__str__() + '.csv')
    dataNum = len(csv_file)
    featureNum = len(csv_file[0])-1
    print("特征的维度", featureNum)
    dataMat = np.array(csv_file)
    X = dataMat[1:, 0:featureNum].astype(float)
    y = dataMat[1:, featureNum].astype(float)
    y = convert2class(y, dataNum) #转换为类别

    X = StandardScaler().fit_transform(X)
    # 数据集分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    lr = LogisticRegression() # Logistic回归模型

    lr.fit(X, y) # 根据数据[x,y]，计算回归参数


    # 训练集上的预测结果
    y_hat = lr.predict(X_test)
    y = y.reshape(-1)
    #  acc = np.mean(y,y_hat)
    print('R2 score:', lr.score(X_test, y_test))

  #  print ('准确度: %.2f%%' % (100 * acc))