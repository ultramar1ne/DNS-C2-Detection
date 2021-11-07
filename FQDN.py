import math


class FQDN:
    def total_characters_counter(self, fqdn: str):
        return len(fqdn)

    def subdomain_characters_counter(self, fqdn: str):
        list = fqdn.split(".")[:-1]
        result = 0
        for part in list:
            result += len(part)
        return result

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

    def avg_label_length_counter(self, fqdn: str):
        lists = fqdn.split(".")
        sum = 0
        for part in lists:
            sum += len(part)
        return sum / self.labels_counter(fqdn)

    def max_label_length_counter(self, fqdn: str):
        lists = self.name.split(".")
        lists.sort(key=lambda x: len(x))
        return len(lists[-1])

    def __init__(self, fqdn, class_0_1):  # todo:我不会python的“反射”
        self.name = fqdn
        self.max_label_legnth = self.max_label_length_counter(fqdn)
        self.avg_label_legnth = self.avg_label_length_counter(fqdn)
        self.labels_num = self.labels_counter(fqdn)
        self.digits_num = self.digits_counter(fqdn)
        self.total_characters = self.total_characters_counter(fqdn)
        self.subdomain_characters = self.subdomain_characters_counter(fqdn)
        self.upperclass_letters_num = self.upperclass_letters_counter(fqdn)
        self.entropy = self.cal_entropy(fqdn)  # todo:有Bug!!:特殊符号不知道咋处理——找个entropy的库吧
        self.class_0_1 = 0 if class_0_1 == '0' else 1  # todo:他给出了不同隧道工具的分类
        self.csv = [self.name[:-1], self.class_0_1, self.max_label_legnth, self.avg_label_legnth, self.labels_num,
                    self.digits_num, self.total_characters, self.upperclass_letters_num, self.entropy]
