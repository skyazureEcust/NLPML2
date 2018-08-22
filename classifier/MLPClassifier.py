# =============神经网络用于分类=============
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from util import CommonUtil
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
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
    csv_file = CommonUtil.read_csv('../files/files_train/files_' + str(n) +
                                   'min/REDUCED_FEATURE_VECTOR_' + str(n) + '.csv')
    dataNum = len(csv_file)
    featureNum = len(csv_file[0])-1
    print("Dimension of feature", featureNum)
    dataMat = np.array(csv_file)
    X = dataMat[1:, 0:featureNum].astype(float)
    y = dataMat[1:, featureNum].astype(float)
    y = convert2class(y, dataNum) # 转换为类别

    # 神经网络对数据尺度敏感，所以最好在训练前标准化，或者归一化，或者缩放到[-1,1]
    scaler = StandardScaler() # 标准化转换
    scaler.fit(X)  # 训练标准化对象
    X = scaler.transform(X)   # 转换数据集
    # solver='lbfgs',  MLP的求解方法：L-BFGS 在小数据上表现较好，Adam 较为鲁棒，SGD在参数调整较优时会有最佳表现（分类效果与迭代次数）；SGD标识随机梯度下降。
    # alpha:L2的参数：MLP是可以支持正则化的，默认为L2，具体参数需要调整
    # hidden_layer_sizes=(5, 2) hidden层2层,第一层5个神经元，第二层2个神经元)，2层隐藏层，也就有3层神经网络

    # 数据集分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    clf = MLPClassifier(solver='lbfgs',
                        learning_rate='constant',
                        learning_rate_init=0.1,
                        max_iter=100,
                        momentum=0.9,
                        alpha=1e-4,
                        hidden_layer_sizes=(5, 2),
                        random_state=0)  # 神经网络输入为2，第一隐藏层神经元个数为5，第二隐藏层神经元个数为2，输出结果为2分类。
    clf.fit(X_train, y_train)
    # print('每层网络层系数矩阵维度：\n',[coef.shape for coef in clf.coefs_])

    # 打印每个网络层的权重矩阵维度
    # cengindex = 0
    # for wi in clf.coefs_:
    #     cengindex += 1  # 表示底第几层神经网络。
    #     print('第%d层网络层:' % cengindex)
    #     print('权重矩阵维度:',wi.shape)
    #     print('系数矩阵:\n',wi)

    # 对测试集进行预测
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("神经网络准确率:", accuracy_score(y_test, y_pred))

    # 预测测试任务中特征向量的分类值和概率
    test_file_name = 'FEATURE_VECTOR_120_R'
    test_file = CommonUtil.read_csv('../dataFiles/' + test_file_name +'.csv')
    testData= np.array(test_file)
    featureData = testData[1:, 0:len(testData[0])].astype(float)
    print(len(featureData))
    print(featureData)

    test_pred = clf.predict(featureData)
    test_pred = test_pred.reshape(len(test_pred), 1)

    # print(test_pred)
    for i in range(len(featureData)):
        print(clf.predict([featureData[i]]))
        print(clf.predict_proba([featureData[i]]))




    # y_pred = clf.predict()
    # print('预测结果：',y_pred)
    # y_pred_pro =clf.predict_proba([[0.317029, 14.739025]])
    # print('预测结果概率：\n',y_pred_pro)

    test_result = np.zeros(len(X_test), dtype=np.float64)

    for i in range(len(X_test)):
        if i == 0: test_result[i]= clf.predict(X_test[i].reshape(1,-1))
        else: test_result[i] = clf.predict(X_test[i].reshape(1,-1))+test_result[i-1]


    '''
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

