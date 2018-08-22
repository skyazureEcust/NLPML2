#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.linear_model import Lasso, Ridge
from util import CommonUtil

if __name__ == "__main__":

    # Load data
    file_dir = 'C:/Users/yuzhe/Desktop/OptionAnalysis/files/'
    csv_file = CommonUtil.read_csv(file_dir + 'TestUSDIndex.csv')
    dataNum = len(csv_file)
    print("数据量", dataNum)
    featureNum = len(csv_file[0]) - 2
    print("特征的维度", featureNum)

    dataMat = np.array(csv_file)
    x = dataMat[1:, 1: featureNum + 1].astype(float)
    print("X[0]", x[0])
    y = dataMat[1:, featureNum + 1].astype(float)
    print("y[0]", y[0])

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.2)
    # model = Lasso()
    model = Ridge()
    alpha_can = np.logspace(-3, 2, 10)

    # 在控制台输出过程中，默认小数会以科学计数法的形式输出,默认值为False
    np.set_printoptions(suppress=True)                    # 即输出小数

    print('alpha_can = ', alpha_can)
    lasso_model = GridSearchCV(model, param_grid={'alpha': alpha_can}, cv=5)
    # GridSearchCV 用法参考 http://blog.csdn.net/cherdw/article/details/54970366
    lasso_model.fit(x_train, y_train)
    print('超参数：\n', lasso_model.best_params_)

    # order = y_test.argsort(axis=0)
    # # argsort()函数是将x中的元素从小到大排列，提取其对应的index(索引)，然后输出到y_test
    # print('order: \n',order)
    # y_test = y_test.values[order]
    # #当把索引对应的赋值给y_test时，输出的y_test自动从小到大排序
    # print('y_test:',y_test)
    # x_test = x_test.values[order,:]
    y_hat = lasso_model.predict(x_test)
    print('score:',lasso_model.score(x_test, y_test))
    mse = np.average((y_hat - np.array(y_test)) ** 2)  # Mean Squared Error
    rmse = np.sqrt(mse)  # Root Mean Squared Error
    print({'mse':mse},{'rmse': rmse})

    t = np.arange(len(x_test))
    mpl.rcParams['font.sans-serif'] = ['simHei']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.figure(facecolor='w')
    plt.plot(t, y_test, 'r-', linewidth=2, label='真实数据')
    plt.plot(t, y_hat, 'g-', linewidth=2, label='预测数据')
    plt.title('回归预测结果', fontsize=18)
    plt.legend(loc='upper left')
    plt.grid(b=True, ls=':')
    plt.show()