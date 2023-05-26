'''

https://stackoverflow.com/questions/46276152/scapy-timestamp-measurement-for-outgoing-packets

https://vnetman.github.io/pcap/python/pyshark/scapy/libpcap/2018/10/25/analyzing-packet-captures-with-python-part-1.html


https://medium.com/hackervalleystudio/learning-packet-analysis-with-data-science-5356a3340d4e

'''

from scapy.all import *
#from scapy.utils import RawPcapReader
#from scapy.layers.l2 import Ether
#from scapy.layers.inet import IP, TCP

import pandas as pd
import scapy 
import time
import datetime


file_name = '/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/sftp/tftp_test_00012_20221219203921.pcap'


paket_list= rdpcap(file_name)


v_data = paket_list[1].show()

#print (v_data)
'''
for pkt in paket_list:
    print (pkt)
    

    print (pkt.show())

    print (hexdump(pkt)) #yes


    print (ls(pkt))

    print (pkt.show2())

'''
    
'''
v_eth_ip.name = Define IP layer  
v_eth_ip.version = Deine Version of IP
v_eth_ip.proto = Define type of Protocol TCP (6) 
v_eth_ip.src = Source ip address
v_eth_ip.dst = Destination IP Address
v_eth_ip.chksum =  Checksum
v_eth_ip.frag = Fragmentation
v_eth_ip.id = Frame identifier (we can see if ther is retransmition)
v_eth_ip.ihl = Header length: 20 bytes (5*4 bytes)
v_eth_ip.tos = Type of services
v_eth_ip.ttl = TTL (Time To Live)

Notes:
No sure if I want to add Total length: 145



v_eth_tcp = v_eth_ip.payload
v_eth_tcp_data = [
                    v_eth_tcp.name,
                    v_eth_tcp.chksum,
                    v_eth_tcp.seq,
                    v_eth_tcp.ack,
                    str(v_eth_tcp.flags),
                    v_eth_tcp.window,
                    v_eth_tcp.sport,
                    v_eth_tcp.dport
                ]

v_eth_tcp.name = TCP/UDP
v_eth_tcp.chksum = 
v_eth_tcp.seq = Sequence number
v_eth_tcp.ack = Aknowledgmen number
str(v_eth_tcp.flags)  = Fag (AK, Syn, Fin, AP)
v_eth_tcp.window = Window size
v_eth_tcp.sport = Soure port
v_eth_tcp.dport = Destination port

v_eth_L5 = v_eth_tcp.payload

print (v_eth_l2)
print (v_eth_ip_data)
print (v_eth_tcp_data)

print ("**** END OF RECORD *****")





print (len(pkt))

v_pkt = pkt[index]

print (type(v_pkt))

print (dir(v_pkt))

hexdump(v_pkt)

v_pkt.show()

v_datetime = time.asctime(time.localtime(pkt[index].time))
v_datetime2 = time.strptime(v_datetime, '%a %b %d %H:%M:%S %Y')

print (v_datetime)
print (pkt[index])
#print (pkt[index].summary())

print (pkt[index].show())

print (hexdump(pkt[index]))


#print (pkt[index].show())
#print (raw(pkt[index]))
print (ls(pkt[index]))

#print (pkt[index].show2())
#print (pkt[index].sprintf())
#print (pkt[index].decode_payload_as())
print (pkt[index].psdump())
print (pkt[index].pdfdump())
print (pkt[index].command())


{'sport': 59057, 'dport': 22, 'seq': 31309701, 'ack': 3988793156, 'dataofs': 11, 'reserved': 0, 'flags': <Flag 16 (A)>, 'window': 64198, 'chksum': 60479, 'urgptr': 0, 'options': [('NOP', None), ('NOP', None), ('Timestamp', (2666350770, 3789678)), ('NOP', None), ('NOP', None), ('SAck', (3988880036, 3988937956))]}

{
    'sport': 59057, 
    'dport': 22, 
    'seq': 31309701, 
    'ack': 3988793156, 
    'dataofs': 11, 
    'reserved': 0, 
    'flags': <Flag 16 (A)>, 
    'window': 64198, 
    'chksum': 60479, 
    'urgptr': 0, 
    'options': [
                ('NOP', None), 
                ('NOP', None), 
                ('Timestamp', (2666350770, 3789678)), 
                ('NOP', None), 
                ('NOP', None), 
                ('SAck', (3988880036, 3988937956))
                ]
}
\((\d+(?:,\s*\d+)*)\)




'''


















chksum
seq
window
tcp_pkt_sc.options[0][0] 
tcp_pkt_sc.options[0][1]
TSVal_TSecr = tcp_pkt_sc.options[1][0]
tcp_pkt_sc.options[1][1]
tcp_pkt_sc.options[2][0]
SAck = tcp_pkt_sc.options[2][1]


{"
 ('NOP', None),
 ('NOP', None), 
 ('Timestamp', (1650887831, 1365336617)), 
 ('NOP', None), 
 ('NOP', None), 
 ('SAck', (2600457171, 2600457289))
 "}