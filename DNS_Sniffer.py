import csv

import joblib
from bloom_filter2 import BloomFilter
from scapy.all import *
from scapy.layers.dns import *

import FQDN_Resolver

classifier = joblib.load("isoForest.m")
interface = input("Input an interface's name, like en0/eth1/WLAN: \n").strip()  # todo:搜集网卡名 多线程？
filter_bpf = 'udp and port 53'  # 伯克利过滤器

# 布隆过滤器-DNS白名单
csvFile = open("dataset/DNS_Whitelist/top-1m-DNS.csv", "r")
reader = csv.reader(csvFile)
bloom = BloomFilter(max_elements=1e5, error_rate=0.01)
wl_counter = 0
for item in reader:
    if reader.line_num == 1:
        continue
    bloom.add(".".join(item[1].split(".")[-3:]))
    wl_counter += 1
    if wl_counter >= 1e5 - 1:
        break
csvFile.close()


# DNS sniffer
def select_DNS(pkt):
    pkt_time = pkt.sprintf('%sent.time%')
    try:
        if (DNSQR in pkt) and pkt.dport == 53:
            qname = str(pkt[DNSQR].qname)

            fqdn = FQDN_Resolver.FQDN(qname)
            print("DNS with qname:", fqdn.name, "sent at time:", pkt_time)
            if fqdn.name in bloom or ".".join(fqdn.name.split(".")[-2:]) in bloom:
                print("website exists in whitelist as", fqdn.name, "\n")
            else:
                result = "Benign" if classifier.predict(fqdn.feat) == 1 else "Malicious"
                print("Test Result:", result, "\n")
    # todo: 消息队列之类的？唤起一个OCC_Tester?;  异常处理：
    except:
        print("err:")


print("Successfully initialized! Start DNS C2 detection!")
sniff(iface=interface, filter=filter_bpf, store=0, prn=select_DNS)
