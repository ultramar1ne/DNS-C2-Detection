import time

import joblib
import pandas as pd
from numpy import reshape
from sklearn.ensemble import IsolationForest

# Define "classifiers" to be used
# 参数瞎写的
classifiers = [  # EllipticEnvelope(support_fraction=1.0, contamination=0.25),
    # OneClassSVM(nu=0.25, gamma=0.35),
    IsolationForest(n_estimators=4, max_samples=16, contamination=0.105, random_state=70)]
data = pd.read_csv('new_features.csv', encoding='utf-8', header=0)
raw = data.values[:, 2:][:11000]  # todo: 这应该是个超参数——”异常“数据占比——待理论/炼丹确定
# todo:不知道需不需要随机化和正则。 需要：混淆矩阵等等...为中期报告做点图？  需要：兄弟们的调优技巧~
test_data = pd.read_csv("new_test.csv", encoding='utf-8', header=0)
test_raw = test_data.values[:, 2:]

# 开始炼丹！
same_err = 0
err_set = set()
for classifier in classifiers:
    T1 = time.time()
    classifier.fit(raw)  # todo:保存模型，测量”体积“
    joblib.dump(classifier, "isoForest.m")

    err, right = 0, 0
    for i, feat in enumerate(raw):
        feat = reshape(feat, (1, -1))
        result = classifier.predict(feat)
        if (result == -1 and data.values[i][1] == 0) or (
                result == 1 and data.values[i][1] == 1):
            err += 1
        else:
            right += 1
        if i % 3000 == 1:
            print(feat)
            T2 = time.time()
            print(T2 - T1, right, err, right / (right + err))
    T2 = time.time()
    print("For TrainSet:", "err:", err, "right:", right, "rate", right / (right + err), "Time:", (T2 - T1))
'''
    err, right = 0, 0

    for i, test_feat in enumerate(test_raw):  # todo:封装
        fqdn = test_data.values[i][0]
        test_feat = np.reshape(test_feat, (1, -1))
        result = classifier.predict(test_feat)
        if (result == -1 and test_data.values[i][1] == 0) or (
                result == 1 and test_data.values[i][1] == 1):
            err += 1
            if fqdn in err_set:
                same_err += 1
            else:
                err_set.add(fqdn)
        else:
            right += 1
        if i % 3000 == 1:
            T2 = time.time()
            print(T2 - T1, right, err, right / (right + err))
    T2 = time.time()
    print("For Test Set:", "err:", err, "right:", right, "rate", right / (right + err), "Time:", (T2 - T1), "same err:",
          same_err, "err_total", len(err_set))
'''
