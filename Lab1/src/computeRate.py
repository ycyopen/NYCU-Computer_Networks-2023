from scapy.config import conf
conf.ipv6_enabled = False
from scapy.all import *
import sys

def separate_flows(packets, flow1_port, flow2_port):
	flow1_packets = []
	flow2_packets = []
	for packet in packets:
		if IP in packet:
			if packet.dport == flow1_port:
				flow1_packets.append(packet)
			elif packet.dport == flow2_port:
				flow2_packets.append(packet)

	return flow1_packets, flow2_packets
    
def cal_throughput(packets):
	total_bytes = 0
	for packet in packets:
		total_bytes += len(packet)
	#print(f"total bytes:{total_bytes}")
	for packet in packets:
		if IP in packet:
			time_i = packet.time
			break
	for packet in reversed(packets):
		if IP in packet:
			time_f = packet.time
			break
	time = time_f - time_i
	#print(time)
	throughput_Mbps=(total_bytes*8)/(time*1000000)
	#bits*8=bytes bytes/sec=bps bps/10^6=Mbps
	return throughput_Mbps


if __name__ == "__main__":

	# get path of pcap file
	TCP_h3_PATH = "../out/TCP_h3.pcap"
	TCP_h4_PATH = "../out/TCP_h4.pcap"
	UDP_h3_PATH = "../out/UDP_h3.pcap"
	UDP_h4_PATH = "../out/UDP_h4.pcap"

	# read pcap
	packet_TCP_Flow12 = rdpcap(TCP_h3_PATH)
	packet_TCP_Flow1 , packet_TCP_Flow2 = separate_flows(packet_TCP_Flow12, 7777, 8763)
	packet_TCP_Flow3 = rdpcap(TCP_h4_PATH)
	packet_UDP_Flow12 = rdpcap(UDP_h3_PATH)
	packet_UDP_Flow1 , packet_UDP_Flow2 = separate_flows(packet_UDP_Flow12, 7777, 8763)
	packet_UDP_Flow3 = rdpcap(UDP_h4_PATH)

	print("--- TCP ---")
	print(f"Flow1(h1->h3):{cal_throughput(packet_TCP_Flow1)}Mbps")
	print(f"Flow2(h1->h3):{cal_throughput(packet_TCP_Flow2)}Mbps")
	print(f"Flow3(h2->h4):{cal_throughput(packet_TCP_Flow3)}Mbps")
	print("\n--- UDP ---")
	print(f"Flow1(h1->h3):{cal_throughput(packet_UDP_Flow1)}Mbps")
	print(f"Flow2(h1->h3):{cal_throughput(packet_UDP_Flow2)}Mbps")
	print(f"Flow3(h2->h4):{cal_throughput(packet_UDP_Flow3)}Mbps")

