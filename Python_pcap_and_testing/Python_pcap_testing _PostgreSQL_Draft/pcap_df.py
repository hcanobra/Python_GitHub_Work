

from scapy.all import *
#from scapy.utils import RawPcapReader
#from scapy.layers.l2 import Ether
#from scapy.layers.inet import IP, TCP

import pandas as pd
import scapy 
import time


# // BEGIN

file_name = '/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/example-02.pcap'


packets_list = rdpcap(file_name)

pkt = packets_list.res[0]



print (pkt)

# // END