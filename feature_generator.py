# from urllib.parse import urlparse
# todo: 我一直不知道Python代码如何较为工程的组织起来 (Class? Design Model?)
# todo: 暂时先假设所有输入的DNS Query都是“格式正确”的
# todo: 假设我对论文中“特征”的文字描述没有产生理解偏差（其实问题不大）
# todo: 目前只利用了FQDN生成我们自己的特征，某些数据集自带高维特征，是否采纳？

import csv
import math




class FQDN:
    def total_characters_counter(self,fqdn: str):
        return len(fqdn)

    def subdomain_characters_counter(self,fqdn: str):
        list = fqdn.split(".")[:-1]
        result = 0
        for part in list:
            result += len(part)
        return result

    def upperclass_letters_counter(self,fqdn: str):
        result = 0
        for s in fqdn:
            if s.islower():
                result += 1
        return result

    def digits_counter(self,fqdn: str):
        result = 0
        for s in fqdn:
            if s.isnumeric():
                result += 1
        return result

    def cal_entropy(self,fqdn: str):
        h = 0.0
        sum = 0
        letter = [0] * 62
        for i in range(len(fqdn)):
            if fqdn[i].islower():
                letter[(ord(fqdn[i]) - ord('a'))%62] += 1
                sum += 1
            elif fqdn[i].isnumeric():
                letter[(ord(fqdn[i]) - ord('0') + 52)%62] += 1
                sum += 1
            elif fqdn[i].isalpha():
                letter[(ord(fqdn[i]) - ord('A') + 26)%62] += 1
                sum += 1
        for i in range(62):
            p = 1.0 * letter[i] / sum
            if p > 0:
                h += -(p * math.log(p, 2))
        return h

    def labels_counter(self,fqdn: str):
        return fqdn.count(".") + 1

    def avg_label_legnth_counter(self,fqdn: str):
        lists = fqdn.split(".")
        sum = 0
        for part in lists:
            sum += len(part)
        return sum / self.labels_counter(fqdn)

    def max_label_legnth_counter(self,fqdn: str):
        lists = self.name.split(".")
        lists.sort(key=lambda x: len(x))
        return len(lists[-1])

    def __init__(self, fqdn):
        self.name = fqdn
        self.max_label_legnth = self.max_label_legnth_counter(fqdn)
        self.avg_label_legnth = self.avg_label_legnth_counter(fqdn)
        self.labels_num = self.labels_counter(fqdn)
        self.digits_num = self.digits_counter(fqdn)
        self.total_characters = self.total_characters_counter(fqdn)
        self.subdomain_characters = self.subdomain_characters_counter(fqdn)
        self.upperclass_letters_num = self.upperclass_letters_counter(fqdn)
        self.entropy = self.cal_entropy(fqdn)# todo:有Bug!!:特殊符号不知道咋处理——找个库吧

csvFile = open("dataset/binary/dtqbc-b-train.csv", "r")
reader = csv.reader(csvFile)
FQDNs = []
for item in reader:
    if reader.line_num == 1:
        continue
    FQDNs.append((FQDN(item[1])))
csvFile.close()

print("!!!",FQDNs[0].name,FQDNs[0].labels_num,FQDNs[0].max_label_legnth)