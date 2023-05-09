

# importing sys
import sys
  
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')

import PostgreSQL_API as pg
import pyshark  
import pandas as pd
import datetime as dt
from datetime import datetime
import numpy as np
import os
import matplotlib.pyplot as plt
import nest_asyncio
import re

def f_cap_filter (option):
    
    if option == 'rtt':
        # Open saved trace file 
        cap = pyshark.FileCapture(file_name, keep_packets=False, display_filter='tcp.analysis.ack_rtt > 0')
        cap.apply_on_packets(f_rtt_layers)
    
    elif option == 'ret':
        # Open saved trace file 
        cap = pyshark.FileCapture(file_name, display_filter='tcp.analysis.out_of_order or tcp.analysis.retransmission or tcp.analysis.spurious_retransmission')
        cap.apply_on_packets(f_ret_layers)
        
    elif option == 'thrpt':
        # Open saved trace file 
        cap = pyshark.FileCapture(file_name, display_filter='(tcp.stream == 1) && (data.data != 0)')
        cap.apply_on_packets(f_thrpt_layers)
    
    return ()

def f_rtt_layers(packet):
    
    print ('RTT_Frame_ID: ' + packet.number)

    v_record = (
                packet.frame_info.time_epoch+ "," +
                packet.frame_info.len+ "," +
                    
                packet.eth.dst+ "," +
                packet.eth.src+ "," +
                
                packet.ip.version+ "," +
                packet.ip.hdr_len+ "," +
                packet.ip.len+ "," +
                packet.ip.ttl+ "," +
                packet.ip.proto+ "," +
                packet.ip.checksum+ "," +
                packet.ip.src+ "," +
                packet.ip.dst+ "," +
                
                packet.tcp.srcport+ "," +
                packet.tcp.dstport+ "," +
                packet.tcp.len+ "," +
                packet.tcp.seq_raw+ "," +
                packet.tcp.ack_raw+ "," +
                packet.tcp.hdr_len+ "," +
                packet.tcp.window_size_value+ "," +
                packet.tcp.checksum+ "," +
                packet.tcp.options_timestamp_tsval+ "," +
                packet.tcp.options_timestamp_tsecr+ "," +
                packet.tcp.analysis_ack_rtt + ","
                )
    
    with open('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_rtt.txt', 'a') as f:
        f.write(v_record)
        f.write('\n')

    return ()

def f_ret_layers(packet):
    
    print ('ret_Frame_ID: ' + packet.number)
    
    v_record = (
                'idx:' + packet.frame_info.time_epoch+ " " +
                'Time_since_previous:' + packet.frame_info.time_delta+ " " + 
                'src:' + packet.ip.src+ " " +
                'dst:' + packet.ip.dst+ " " +
                'srcport:' + packet.tcp.srcport+ " " +
                'dstport:' + packet.tcp.dstport+ " " +
                'rel_ack:' + packet.tcp.ack+ " " +
                'raw_ack:' + packet.tcp.ack_raw+ " " +
                'rel_seq:' + packet.tcp.seq+ " " +
                'raw_seq:' + packet.tcp.seq_raw+ " " +
                'TCP_Flag:' + packet.tcp.flags+ " " +
                'Analysis:' + packet.tcp._ws_expert 
                )
    
    with open('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_ooo.txt', 'a') as f:
        f.write(v_record)
        f.write('\n')
     
    return ()

def f_thrpt_layers(packet):
    
    print ('Thrpt_Frame_ID: ' + packet.number)
    
    v_record = (
    'Frame_ID:' + packet.number+ " " +
    'idx:' + packet.frame_info.time_epoch+ " " +
    'Time_since_previous:' + packet.frame_info.time_delta+ " " +
    'Frame_length:' + packet.length+ " " +
    'src:' + packet.ip.src+ " " +
    'dst:' + packet.ip.dst
        )
    
    with open('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_thrp.txt', 'a') as f:
        f.write(v_record)
        f.write('\n')
    
    
    return (v_record)

def f_postgresql_new_table (df,table):
    
    v_database = 'vzw_mec_sp'
    v_table = 'pcap_tables_tcp_thrp'
    
    cn = pg.Connection(v_database)
    cn.PostgreSQL_load_append_df (v_table,df)

def f_postgresql_query (query):
    v_database = 'vzw_mec_sp'
    
    cn = pg.Connection (v_database)
    v_df = cn.PostgreSQL_query_df (query)
    
    return (v_df)

def f_df_rtt ():
    for file in os.listdir(path):
        if file.endswith(".txt"):
            print (file)

            with open(path+file) as full_file:
                v_list = [line.rstrip() for line in full_file]
                
            v_list = [re.sub('\s+', ' ', x) for x in v_list]

            v_df = pd.DataFrame ([sub.split(" ") for sub in v_list])
            
            print (v_df)

        
        v_columns = (
                        'idx',
                        'l2_frame_len',
                            
                        "l2_dst",
                        "l2_src" ,
                        
                        "l3_ver",
                        "l3_hrd_len",
                        "l3_len",
                        "l3_ttl",
                        "l3_proto",
                        "l3_cksum",
                        "l3_src",
                        "l3_dst",
                        
                        "l4_srcport",
                        "l4_dstport",
                        "l4_len",
                        "l4_seq_raw",
                        "l4_ack_raw",
                        "l4_hdr_len",
                        "l4_window_size",
                        "l4_cksum",
                        "l4_tsval",
                        "l4_tsecr",
                        "l4_analysis_RTT_to_Ack"
                        )
        
        '''    
            with open('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_rtt.txt', 'a') as f:
                f.write(v_columns)
                f.write('\n')
        '''
    return ()

def q_query (table):
    v_query = '''


                '''
    return(v_query)


# ///////// BEGIN 
nest_asyncio.apply()
os.system('clear')

path = "/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/"
v_file = '02142023'

record = []

dir_list = os.listdir(path)

for file in os.listdir(path):
    if file.endswith(".pcap"):

        file_name = path+file
        print ("#######################################")
        os.system('date')

        print ("1) Processing file: ",file_name)

        # Rout trip delay calculation
        v_cap = f_cap_filter ('rtt')
        
        # Rout trip delay calculation
        v_cap = f_cap_filter ('ret')
        
        # Rout trip delay calculation
        v_cap = f_cap_filter ('thrpt')
        
        # Data Frame creation
        f_df_rtt ()
        
        print ("2) Done with file.....")
                
        # Load dataframe to PostgreSQL
        #if f_df.empty == False:
        #    f_postgresql_new_table (f_df,v_file)
        
        os.system('date')
        print ("#######################################")

# ///////// END

