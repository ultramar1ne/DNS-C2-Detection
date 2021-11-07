# from urllib.parse import urlparse
# todo: 暂时先假设所有输入的DNS Query都是“格式正确”的
# todo: 假设我对论文中“特征”的文字描述没有产生理解偏差（其实问题不大）
# todo: 目前只利用了FQDN生成我们自己的特征，某些数据集自带高维特征，是否采纳？
import csv

import pandas as pd

from FQDN import FQDN


def generate_features(input_filename="dataset/binary/dtqbc-b-train.csv", output_filename="new_features.csv"):
    csvFile = open(input_filename, "r")
    reader = csv.reader(csvFile)
    FQDNs = []
    for item in reader:
        if reader.line_num == 1:
            continue
        FQDNs.append((FQDN(item[1], item[0])))
    csvFile.close()

    new_feature = pd.DataFrame([FQDNs[_].csv for _ in range(len(FQDNs))],
                               columns=['FQDN', 'class_0_1', 'max_label_legnth', 'avg_label_legnth', 'labels_num',
                                        'digits_num', 'total_characters', 'upperclass_letters_num', 'entropy'])
    new_feature.to_csv(output_filename, index=None, encoding="utf8")

    print("new features successfully generated as in", output_filename)
# 统计生成的数据集
    csvFile = open(output_filename, "r", encoding="utf8")
    reader = csv.reader(csvFile)
    mal_counter, heal_counter = 0, 0
    for item in reader:
        if item[1] == '0':
            if heal_counter < 5:
                print("healthy", item[0])
            heal_counter += 1
        if item[1] == '1':
            if mal_counter < 5:
                print("malicious", item[0])
            mal_counter += 1
    csvFile.close()
    print("0:", heal_counter, "1:", mal_counter)


generate_features("dataset/binary/dtqbc-b-train.csv", "new_features.csv")
generate_features("dataset/binary/dtqbc-b-test.csv", "new_test.csv")
