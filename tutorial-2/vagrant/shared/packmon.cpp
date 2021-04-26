#include <stdio.h>
#include <string.h>
#include <iostream>
#include <pcap.h>
#include <net/ethernet.h>
#include <netinet/udp.h>
#include <netinet/tcp.h>
#include <netinet/ip.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>


#define TCP_FLAG 6
#define UDP_FLAG 17

long unsigned int packet_count = 1, dns_count = 1, syn_count = 1;

void print_payload(const u_char * pkt_data, size_t data_size) {
		printf("PAYLOAD: ");
		for(size_t j = 0; j < data_size; ++j ) {
			if( ' ' <= pkt_data[j] && pkt_data[j] <= '~' )
				printf( "%c", pkt_data[j]);
			else
				printf( ".");
		}
        printf( "\n");
}

bool isSYN(const pcap_pkthdr *pkt_header, const u_char * data) {
	iphdr *ip_header = (iphdr *)( data  + sizeof(ethhdr) );
    tcphdr *tcp_header=(tcphdr*)(data + ip_header->ihl*4 + sizeof(ethhdr));
    int header_size =  sizeof(ethhdr) + ip_header->ihl*4 + tcp_header->doff*4;

	in_addr source = {0};
	source.s_addr = ip_header->saddr;

    if ( ! tcp_header->syn )
        return false;

	printf("GOT %lu/%lu TCP PACKET FROM %s:%u TO PORT %u\n", 
				syn_count, packet_count, inet_ntoa(source), ntohs(tcp_header->source), ntohs(tcp_header->dest));

	int packet_size = pkt_header->caplen;
	print_payload(data+header_size, packet_size-header_size);
	return true;
}

bool isDNS(const pcap_pkthdr *pkt_header, const u_char * data) {
	iphdr *ip_header = (iphdr *)(data +  sizeof(ethhdr));
    udphdr *udp_header = (udphdr*)(data + ip_header->ihl*4 + sizeof(ethhdr));
    int header_size =  sizeof(ethhdr) + ip_header->ihl*4 + sizeof(udp_header);

	in_addr source = {0};
	source.s_addr = ip_header->saddr;

	if ( ntohs(udp_header->dest) != 53 && ntohs(udp_header->source) != 53 )
        return false;

	printf("GOT %lu/%lu UDP PACKET FROM %s:%u TO PORT %u\n",
	 			dns_count, packet_count, inet_ntoa(source), ntohs(udp_header->source), ntohs(udp_header->dest));

	int packet_size = pkt_header->caplen;
	print_payload(data+header_size, packet_size-header_size);
	return true;
}

void show_packet(u_char *user, const pcap_pkthdr *pkt_header, const u_char *pkt_data){
	iphdr * ip_header = (iphdr*) (pkt_data + sizeof(ethhdr));

	if ( ip_header->protocol == TCP_FLAG && isSYN(pkt_header, pkt_data)) {
		syn_count++;
		packet_count++;
	}

	if ( ip_header->protocol == UDP_FLAG && isDNS(pkt_header, pkt_data)) {
		dns_count++;
		packet_count++;
	}

}

int main() {

	char errbuf[PCAP_ERRBUF_SIZE];  // if failed, contains the error text
	memset(errbuf, 0, PCAP_ERRBUF_SIZE);  // errbuf initialized

	// Open device in promiscuous mode
	pcap_t * descr=pcap_open_live("enp0s8", 65536, true, 0, errbuf);

	if ( descr == NULL ) {
		printf("Ajaj handle neni\n");
	}

	printf("Program zacal\n");
	// Start infinite packet processing loop
	pcap_loop(descr, -1, show_packet, NULL);

	// Close the descriptor of the opened device
	pcap_close(descr);

	return 0;
}