

#from scapy.all import *
#from scapy.utils import RawPcapReader
#from scapy.layers.l2 import Ether
#from scapy.layers.inet import IP, TCP

import pandas as pd
from scapy.all import rdpcap
import time
import numpy as np


def f_l2 (packets_list):

    fields = {
                'Ethernet' : ['time','name','src','dst','type','wirelen'],
                }

    df_l2 = pd.DataFrame(
        {
            field: [
                    getattr(pkt, field) if layer in pkt else pd.NA
                            for pkt in packets_list
                    ]
                    for layer, field_list in fields.items()
                    for field in field_list
        })       

    # Renaming columns
    v_columns = ['idx','L2_Name','l2_src','l2_dst','l2_type','l2_wirelen']
    df_l2.columns = v_columns
    
    # Creating Index for refereence
    df_l2['idx'] = df_l2['idx'].astype(object)
    df_l2['l2_wirelen'] =  df_l2['l2_wirelen']*8
    
    # Creating a field time on the pkt as a new column date time
    df_l2['l2_time'] = pd.to_datetime(df_l2['idx'].astype(float) , unit='s', utc=True).map(lambda x: x.tz_convert('US/Mountain'))
    
    return (df_l2)

def f_l3(packets_list):
    fields = {
                'IP' : ['name','version','proto','src','dst','chksum','frag','id','ihl','tos','ttl']
                }

    df_l3 = pd.DataFrame(
        {
            field: [
                    getattr(pkt.payload, field) if layer in pkt else pd.NA
                            for pkt in packets_list
                    ]
                    for layer, field_list in fields.items()
                    for field in field_list
        })
    
    # Renaming columns
    v_columns = ['l3_name','l3_version','l3_proto','l3_src','l3_dst','l3_chksum','l3_flag','l3_id','l3_ihl','l3_tos','l3_ttl']
    df_l3.columns = v_columns
        
    
    # Transforming procol numbers into protocol IDs
    df_l3 = df_l3.replace({'l3_proto' : { 
                                        1 : 'ICMP', 
                                        17 : 'UDP', 
                                        6 : 'TCP', 
                                        4 : 'IPv4'
                                        }
                           }
                          )
    
    return (df_l3)

def f_l4 (packets_list):
    fields = {
                'TCP': ['chksum','seq','ack','flags','window','sport','dport'],
                'UDP': ['sport','dport'],
                'ICMP': ['chksum','seq']

            }

    df_l4 = pd.DataFrame(
        {
            field: [
                    getattr(pkt.payload.payload, field) if layer in pkt else pd.NA
                            for pkt in packets_list
                    ]
                    for layer, field_list in fields.items()
                    for field in field_list
        })
    
    # Renaming columns
    v_columns = ['l4_chksum','l4_seq','l4_ack','l4_flags','l4_window','l4_sport','l4_dport']
    df_l4.columns = v_columns
        
    return (df_l4)

# // BEGIN

file_name = '/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/example-04.pcap'


packets_list = rdpcap(file_name)

# Calling the functions for each OSI layer
v_l2 = f_l2 (packets_list)
v_l3 = f_l3(packets_list)
v_l4 = f_l4 (packets_list)

# Concatenate all OSI layers
dfs = [v_l2, v_l3, v_l4]
f_df = dfs[0].join(dfs[1:])


print (f_df)

# // END