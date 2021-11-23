import joblib
from scapy.all import *
from scapy.layers.dns import *

import FQDN

classifier = joblib.load("isoForest.m")
interface = 'WLAN'  # todo:搜集网卡名 多线程？
filter_bpf = 'udp and port 53'  # 伯克利过滤器


def select_DNS(pkt):
    pkt_time = pkt.sprintf('%sent.time%')
    try:
        if (DNSQR in pkt) and pkt.dport == 53:
            qname = str(pkt[DNSQR].qname)
            print("QName:", qname, "at time:", pkt_time)
            result = "Benign" if classifier.predict(FQDN.FQDN(qname).feat) == 1 else "Malicious"
            print("Test Result:", result)
    # todo: 消息队列之类的？唤起一个OCC_Tester?;  异常处理：
    except:
        print("err:")

sniff(iface=interface, filter=filter_bpf, store=0, prn=select_DNS)
