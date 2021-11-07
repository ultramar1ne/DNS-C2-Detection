# Author: Virgile Fritsch <virgile.fritsch@inria.fr>
# License: BSD 3 clause
import time

import numpy as np
import pandas as pd
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM

# Define "classifiers" to be used
# 参数瞎写的
classifiers = [EllipticEnvelope(support_fraction=1.0, contamination=0.25),
               OneClassSVM(nu=0.25, gamma=0.35),
               IsolationForest(random_state=0)]
data = pd.read_csv('new_features.csv', encoding='utf-8', header=0)
raw = data.values[:, 2:][:15000]  # todo: 这应该是个超参数——”异常“数据占比——待理论/炼丹确定
test_data = pd.read_csv("new_test.csv", encoding='utf-8', header=0)
test_raw = test_data.values[:, 2:]

# 开始炼丹！
for classifier in classifiers:
    T1 = time.time()
    classifier.fit(raw)  # todo:保存模型，测量”体积“
    y_pred = classifier.fit_predict(raw)
    '''
    err, right = 0, 0
    for i, test_feat in enumerate(raw):
        test_feat = np.reshape(test_feat, (1, -1))
        result = classifier.predict(test_feat)
        if (result == -1 and data.values[i][1] == 0) or (
                result == 1 and data.values[i][1] == 1):
            err += 1
        else:
            right += 1
        if i % 2001 == 0:
            T2 = time.time()
            print(T2 - T1, right, err, right / (right + err))
    T2 = time.time()
    print("For TrainSet:", "err:", err, "right:", right, "rate", right / (right + err), "Time:", (T2 - T1))
    '''
    err, right = 0, 0
    for i, test_feat in enumerate(test_raw):  # todo:封装
        test_feat = np.reshape(test_feat, (1, -1))
        result = classifier.predict(test_feat)
        if (result == -1 and test_data.values[i][1] == 0) or (
                result == 1 and test_data.values[i][1] == 1):
            err += 1
        else:
            right += 1
        if i % 3001 == 0:
            T2 = time.time()
            print(T2 - T1, right, err, right / (right + err))
    T2 = time.time()
    print("For Test Set:", "err:", err, "right:", right, "rate", right / (right + err), "Time:", (T2 - T1))
