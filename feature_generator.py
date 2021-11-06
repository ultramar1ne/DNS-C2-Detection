# from urllib.parse import urlparse
# todo: 暂时先假设所有输入的DNS Query都是“格式正确”的
# todo: 假设我对论文中“特征”的文字描述没有产生理解偏差（其实问题不大）
# todo: 目前只利用了FQDN生成我们自己的特征，某些数据集自带高维特征，是否采纳？

import csv
import math
import pandas as pd




def total_characters_counter(fqdn: str):
    return len(fqdn)


def subdomain_characters_counter(fqdn: str):
    list = fqdn.split(".")[:-1]
    result = 0
    for part in list:
        result += len(part)
    return result


class FQDN:

    def upperclass_letters_counter(self, fqdn: str):
        result = 0
        for s in fqdn:
            if s.islower():
                result += 1
        return result

    def digits_counter(self, fqdn: str):
        result = 0
        for s in fqdn:
            if s.isnumeric():
                result += 1
        return result

    def cal_entropy(self, fqdn: str):
        h = 0.0
        sum = 0
        letter = [0] * 62
        for i in range(len(fqdn)):
            if fqdn[i].islower():
                letter[(ord(fqdn[i]) - ord('a')) % 62] += 1
                sum += 1
            elif fqdn[i].isnumeric():
                letter[(ord(fqdn[i]) - ord('0') + 52) % 62] += 1
                sum += 1
            elif fqdn[i].isalpha():
                letter[(ord(fqdn[i]) - ord('A') + 26) % 62] += 1
                sum += 1
        for i in range(62):
            p = 1.0 * letter[i] / sum
            if p > 0:
                h += -(p * math.log(p, 2))
        return h

    def labels_counter(self, fqdn: str):
        return fqdn.count(".") + 1

    def avg_label_legnth_counter(self, fqdn: str):
        lists = fqdn.split(".")
        sum = 0
        for part in lists:
            sum += len(part)
        return sum / self.labels_counter(fqdn)

    def max_label_legnth_counter(self, fqdn: str):
        lists = self.name.split(".")
        lists.sort(key=lambda x: len(x))
        return len(lists[-1])

    def __init__(self, fqdn, class_0_1):  # todo:我不会python的“反射”
        self.name = fqdn
        self.max_label_legnth = self.max_label_legnth_counter(fqdn)
        self.avg_label_legnth = self.avg_label_legnth_counter(fqdn)
        self.labels_num = self.labels_counter(fqdn)
        self.digits_num = self.digits_counter(fqdn)
        self.total_characters = total_characters_counter(fqdn)
        self.subdomain_characters = subdomain_characters_counter(fqdn)
        self.upperclass_letters_num = self.upperclass_letters_counter(fqdn)
        self.entropy = self.cal_entropy(fqdn)  # todo:有Bug!!:特殊符号不知道咋处理——找个entropy的库吧
        self.class_0_1 = 0 if class_0_1=='0' else 1 #todo:他给出了不同隧道工具的分类
        self.csv=[self.name[:-1],self.class_0_1,self.max_label_legnth,self.avg_label_legnth,self.labels_num,self.digits_num,self.total_characters,self.upperclass_letters_num,self.entropy]


csvFile = open("dataset/binary/dtqbc-b-train.csv", "r")
reader = csv.reader(csvFile)
FQDNs = []
for item in reader:
    if reader.line_num == 1:
        continue
    FQDNs.append((FQDN(item[1], item[0])))
csvFile.close()

new_feature = pd.DataFrame([ FQDNs[_].csv for _ in range(len(FQDNs))], columns=['FQDN','class_0_1','max_label_legnth','avg_label_legnth','labels_num','digits_num','total_characters','upperclass_letters_num','entropy'])
new_feature.to_csv('new_features.csv',index=None,encoding="utf8")

print("new features successfully generated as in new_features.csv")

csvFile = open("new_features.csv", "r", encoding="utf8")
reader = csv.reader(csvFile)
mal_counter,heal_counter=0,0
for item in reader:
    if item[1]=='0':
        if heal_counter<5:
            print("healthy",item[0])
        heal_counter+=1
    if item[1]=='1':
        if mal_counter<5:
            print("malicious",item[0])
        mal_counter+=1
csvFile.close()
print("0:",heal_counter,"1:",mal_counter)