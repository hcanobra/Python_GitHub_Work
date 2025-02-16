

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
            'TCP': ('chksum','seq','ack','flags','window','sport','dport'),
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
                    
    
    # Renaming columns

            
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
    
    v_database = 'vzw_mec'
    v_table = 'pcap_tables_test'
    
    cn = pg.Connection(v_database)
    cn.PostgreSQL_load_append_df (v_table,df)


# ///////// BEGIN 

#file_name = '/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/sftp/tftp_test_00010_20221219203907.pcap'

path = "/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/sftp/"
dir_list = os.listdir(path)

for file in os.listdir(path):
    if file.endswith(".pcap"):
        file_name = path+file

        
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

        f_postgresql (f_df)
        
        
        print ("Done with file:",file_name)

# // END