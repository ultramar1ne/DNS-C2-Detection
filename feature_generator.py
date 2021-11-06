# from urllib.parse import urlparse
# todo: 我一直不知道Python代码如何较为工程的组织起来 (Class? Design Model?)
# todo: 暂时先假设所有输入的DNS Query都是“格式正确”的
# todo: 假设我对论文中“特征”的文字描述没有产生理解偏差（其实问题不大）
# todo: 目前只利用了FQDN生成我们自己的特征，某些数据集自带高维特征，是否采纳？

import csv
import math

csvFile = open("dataset/binary/dtqbc-b-train.csv", "r")
reader = csv.reader(csvFile)
DNSs = dict()
for item in reader:
    if reader.line_num == 1:
        continue
    DNSs[item[1][:-1]] = item[0]
csvFile.close()

sample = "traffic-manager.p4d.clouD.slb-ds.com"


def total_characters_counter(fqdn: str):
    return len(fqdn)


def subdomain_characters_counter(fqdn: str):
    list = fqdn.split(".")[:-1]
    result = 0
    for part in list:
        result += len(part)
    return result


def upperclass_letters_counter(fqdn: str):
    result = 0
    for s in fqdn:
        if s.islower():
            result += 1
    return result


def digits_counter(fqdn: str):
    result = 0
    for s in fqdn:
        if s.isnumeric():
            result += 1
    return result


def cal_entropy(fqdn: str):
    h = 0.0
    sum = 0
    letter = [0] * 62
    for i in range(len(fqdn)):
        if fqdn[i].islower():
            letter[ord(fqdn[i]) - ord('a')] += 1
            sum += 1
        elif fqdn[i].isnumeric():
            letter[ord(fqdn[i]) - ord('0') + 52] += 1
            sum += 1
        elif fqdn[i].isalpha():
            letter[ord(fqdn[i]) - ord('A') + 26] += 1
            sum += 1
    for i in range(62):
        p = 1.0 * letter[i] / sum
        if p > 0:
            h += -(p * math.log(p, 2))
    return h


def labels_counter(fqdn: str):
    return fqdn.count(".") + 1


def avg_label_legnth(fqdn: str):
    lists = fqdn.split(".")
    sum = 0
    for part in lists:
        sum += len(part)
    return sum / labels_counter(fqdn)


def max_label_legnth(fqdn: str):
    lists = fqdn.split(".")
    lists.sort(key=lambda x: len(x))
    return len(lists[-1])
