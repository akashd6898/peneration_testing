#!/usr/bin/env python
#operation of scapy built program netdiscover
import scapy.all as scapy
#broadcast other computer in the network
def scan(ip):
    #scapy.arping(ip)
    arp_req = scapy.ARP(pdst = ip)
    #arp_req.pdst=ip,pdst name of the field we need to use and assigning ip value to pdst
    #arp_req.show()#shows a details of the ARP packet(class)
    #arp_req.pdst = ip
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # (ETHERNET FRAMEWORK) data is sent in network is using MAC address and so the ETHER class and
    # the source and destination MAC is stored in ETHER class #ff:ff:ff:ff:ff:ff virtual MAC but clients receives in network
    #broadcast.show() #shows the details of ETHER packet(class)
    arp_request_broadcast = broadcast/arp_req
    #combining arp_req and broadcast with arp_request_broadcast
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast,timeout=1, verbose=False)
    # sr means send and receive packets that allows custom ether part(arp_request_broadcast) to send and
    # receive but returns more than one values as two list(answered packets and unanswered packets),verbose doesnt print unwanted line
    #print(answered_list.summary())
#print("IP\t\t\tMAC address\n==============================")
    client_list = []
    for i in answered_list:
        #answered_list has two list within sent list and received list
        #print(i[1].show())#to know the fields
        client_dict = {"ip":i[1].psrc,"MAC":i[1].hwsrc}
        client_list.append(client_dict)
        #print(i[1].psrc +"\t\t\t" +i[i].hwsrc)#ip from the client of answered_list
        #print(i[i].hwsrc)MAC from the client of answered_list
    return client_list

def print_result(result_list):
    print("IP\t\t\tMAC ADDRESS\n===============================================")
    for client in result_list:
        print(client["ip"]+"\t\t"+client["MAC"])

    #arp_request_broadcast.show()#shows the details of both packet combined
    #print(arp_request_broadcast.summary())
    #scapy.ls(scapy.Ether)#to find the variable for destination MAC variable used in scapy module of class ETHER
    #print(arp_req.summary())#GIVES THE SUMMARY
    #print(broadcast.summary())
    #scapy.ls(scapy.ARP()) lists the variables in scapy module of class ARP to find field(pdst) to be used
scan_result = scan("10.0.2.1/24")#all possible ip
print_result(scan_result)