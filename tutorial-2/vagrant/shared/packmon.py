from scapy.all import *
from pprint import pprint

interface = "enp0s8"

def show_packet(packt):
    if IP in packt:
        src_ip = packt[IP].src

        # if UDP in packt and str(packt[UDP].dport) == "53":
        if UDP in packt and packt.haslayer(DNS):
            print(f'Got DNS packet from {src_ip}')
            pprint(packt.getlayer(DNS))

        if TCP in packt and str(packt.getlayer(TCP).flags).upper() == "S":
            print(f'Got SYN packet from {src_ip}')
            pprint(packt.getlayer(TCP))


sniff(iface = interface, prn = show_packet, store = 0)