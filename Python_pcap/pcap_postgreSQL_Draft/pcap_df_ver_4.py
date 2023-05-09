'''
## Iperf3 Website and functions:
https://www.mankier.com/1/iperf3


How TCP Works - The Timestamp Option
https://www.networkdatapedia.com/post/2018/10/08/how-tcp-works-the-timestamp-option

TCP Extensions for High Performance
https://www.rfc-editor.org/rfc/rfc1323#section-4

How to Derive the TSVal and TSecr TCP option fields using python?
https://stackoverflow.com/questions/27812542/how-to-derive-the-tsval-and-tsecr-tcp-option-fields-using-python

Understanding time stamps in Packet Capture Data (.pcap) files
https://www.elvidence.com.au/understanding-time-stamps-in-packet-capture-data-pcap-files/

Understanding TCP Sequence and Acknowledgment Numbers
https://packetlife.net/blog/2010/jun/7/understanding-tcp-sequence-acknowledgment-numbers/

https://scapy.readthedocs.io/en/latest/usage.html
https://www.programcreek.com/python/example/103591/scapy.all.rdpcap
https://stackoverflow.com/questions/65038769/how-to-convert-scapy-packetlist-to-dataframe-in-python

IEEE 802 Numbers
https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml

dpkt Tutorial #2: Parsing a PCAP File
https://jon.oberheide.org/blog/2008/10/15/dpkt-tutorial-2-parsing-a-pcap-file/
https://dpkt.readthedocs.io/en/latest/examples.html
https://stackoverflow.com/questions/18256342/parsing-a-pcap-file-in-python


https://vnetman.github.io/pcap/python/pyshark/scapy/libpcap/2018/10/25/analyzing-packet-captures-with-python-part-1.html

import time

def printable_timestamp(ts, resol):
    ts_sec = ts // resol
    ts_subsec = ts % resol
    ts_sec_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts_sec))
    return '{}.{}'.format(ts_sec_str, ts_subsec)
    
'''

#from scapy.all import *
#from scapy.utils import RawPcapReader
#from scapy.layers.l2 import Ether
#from scapy.layers.inet import IP, TCP



# importing sys
import sys
  
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')


import pandas as pd
from scapy.all import rdpcap
import time
import PostgreSQL_API as pg
import os
import re
import numpy as np
from datetime import datetime, timedelta




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
    df_l2['l2_wirelen'] =  df_l2['l2_wirelen']
    
    # Creating a field time on the pkt as a new column date time
    df_l2['l2_time'] = pd.to_datetime(df_l2['idx'].astype(float) , unit='s', utc=True).map(lambda x: x.tz_convert('US/Mountain'))
    
    # For individual records 
                # // datetime.fromtimestamp(float(packets_list[7].time)).isoformat(sep=' ', timespec='milliseconds')
                # // float (packets_list[8].time)
    
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
            'TCP': ('chksum','seq','ack','flags','window','sport','dport','fields'),
            'UDP': ('sport','dport'),
            'ICMP': ('chksum','seq')
            # ...
            }

    # Building Pandas DF
    # I am using the Layer information and parameter to create the collumn.   " layer+"_"+field "
    # eg.      chksum_TCP       seq_TCP     ack_TCP     flags_TCP   window_TCP      sport_TCP   dport_TCP   sport_UDP   dport_UDP   chksum_ICMP seq_ICMP
    #          30050            2998762674  2794455351  A           442             443         62111       <NA>        <NA>        <NA>        <NA>

    df_l4 = pd.DataFrame({layer+"_"+field: [str(getattr(pkt[layer], field)) if layer in pkt else pd.NA
                            for pkt in packets_list]
                    for layer, field_list in fields.items()
                    for field in field_list})
                    


    # Extract values TSval, TSecr from column Fields, this will be used to calculate time stamps between frame streams and RTT
    # https://stackoverflow.com/questions/27812542/how-to-derive-the-tsval-and-tsecr-tcp-option-fields-using-python
    # https://www.rfc-editor.org/rfc/rfc1323#section-4
    
    df_l4.to_csv ('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/frame.csv')     # --- FOR TROUBLESHOOTING PURPOSES 
    
    df_l4['TCP_fields'] = df_l4['TCP_fields'].replace(np.nan, '(0,0)')  #   Fill the packets which does not contain values with zeros
    df_l4['TCP_fields'] = df_l4['TCP_fields'].apply(lambda x: re.findall(r'(?<=\[)([^]]+)(?=\])', x))    
    
    
    df_l4 = df_l4.rename(columns={'TCP_fields':'TCP_TSval_TSecr'})

    # Regunal rexpression to match anyting devided by comma \((\d+(?:,\s*\d+)*)\)
    return (df_l4)

def f_pkt_miss (packets_list):
    
    # Setting limit for string in Pandas
    pd.options.display.max_colwidth = 1000
        
    
    df_miss = pd.DataFrame(
        {
            'Frame_flow': [
                    str(pkt)
                        for pkt in packets_list
                    ]
        })
            
    return(df_miss)

def f_postgresql (df):
    
    v_database = 'vzw_mec_sp'
    v_table = 'pcap_tables_tcp_02022023'
    
    cn = pg.Connection(v_database)
    cn.PostgreSQL_load_append_df (v_table,df)


# ///////// BEGIN 

#file_name = '/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/sftp/tftp_test_00010_20221219203907.pcap'

path = "/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/"
dir_list = os.listdir(path)

for file in os.listdir(path):
    if file.endswith(".pcap"):


        
        file_name = path+file

        print ("1) Processing file: ",file_name)

        # Prints only pcap file present in My Folder
    
        packets_list = rdpcap(file_name)

        # Calling the functions for each OSI layer
        v_l2 = f_l2 (packets_list)
        v_l3 = f_l3(packets_list)
        v_l4 = f_l4 (packets_list)
        v_miss = f_pkt_miss(packets_list)

        # Concatenate all OSI layers
        dfs = [v_l2, v_l3, v_l4,v_miss]
        f_df = dfs[0].join(dfs[1:])
        
        # Add file name as part of the dataframe
        f_df['Source'] = file[:(
                                    len(file) - 
                                    (
                                        len(file) - file.find('.')
                                    )
                                )
                            ]

        # Load dataframe to PostgreSQL
        f_postgresql (f_df)
        
        print ("2) Done with file: ",file_name)
        print (" ######### ")
        
        
# // END 