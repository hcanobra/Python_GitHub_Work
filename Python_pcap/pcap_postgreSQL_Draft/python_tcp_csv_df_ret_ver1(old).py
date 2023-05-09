
'''

https://python-forum.io/thread-28096.html

https://thepacketgeek.com/pyshark/intro-to-pyshark/


https://pypi.org/project/pyshark/

http://kiminewt.github.io/pyshark/

https://kiminewt.github.io/pyshark/

https://wiki.wireshark.org/DisplayFilters

https://sh0ckflux.medium.com/data-visualization-using-pyshark-dafa9f70de2c


'''
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


def f_ret (file_name):
  
    v_file = file_name
    
    
    # Open saved trace file 
    capture = pyshark.FileCapture(file_name, display_filter='tcp.analysis.retransmission')
    
    v_ret_df = pd.DataFrame()
    v_record = {}
    
    for pkt in capture:
        if ("TCP" in pkt):
            v_record = {
                        'idx': pkt.frame_info.time_epoch, 
                        'Time_since_previous': pkt.frame_info.time_delta, 
                        'src': pkt.ip.src,
                        'dst': pkt.ip.dst,
                        'srcport': pkt.tcp.srcport,
                        'dstport': pkt.tcp.dstport,
                        'rel_ack' : pkt.tcp.ack,
                        'raw_ack' : pkt.tcp.ack_raw,
                        'rel_seq' : pkt.tcp.seq,
                        'raw_seq' : pkt.tcp.seq_raw,
                        'TCP_Flag' : pkt.tcp.flags,
                        'Analysis' : pkt.tcp.analysis_retransmission                        
                        }
            df_dictionary = pd.DataFrame([v_record])
            v_ret_df = pd.concat([v_ret_df, df_dictionary], ignore_index=True)
            
            v_ret_df['l2_time'] = pd.to_datetime(v_ret_df['idx'].astype(float) , unit='s', utc=True).map(lambda x: x.tz_convert('US/Mountain'))
            
            
            v_ret_df = v_ret_df[[
                                'idx',
                                'l2_time',
                                'Time_since_previous',
                                'src',
                                'dst',
                                'srcport',
                                'dstport',
                                'rel_ack',
                                'raw_ack',
                                'rel_seq',
                                'raw_seq',
                                'TCP_Flag',
                                'Analysis'
                                ]]
            
            
    return (v_ret_df)

def f_postgresql_new_table (df,table):
    
    v_database = 'vzw_mec_sp'
    v_table = 'pcap_tables_tcp_retransmition_%s'%table
    
    cn = pg.Connection(v_database)
    cn.PostgreSQL_load_append_df (v_table,df)

def q_query (table):
    v_query = '''
                WITH
                    TABLE_NAME AS
                        (
                        SELECT * FROM public.pcap_tables_tcp_retransmition_%s
                        ORDER BY "idx"
                        ),
                    FRAME_DELTA AS 
                        (
                            SELECT 
                                MIN (
                                    EXTRACT (EPOCH FROM (
                                                        SELECT CAST ("l2_time" - INTERVAL '7 HOURS' AS TIME)
                                                        )
                                        )
                                    ) 
                            FROM TABLE_NAME
                        ),
                    RELATIVE_TIME AS 
                        (
                            SELECT 
                                "idx",
                                "l2_time",

                                EXTRACT (EPOCH FROM (
                                                    SELECT CAST ("l2_time" - INTERVAL '7 HOURS' AS TIME)
                                                    ) 
                                        ) - (
                                            SELECT * FROM FRAME_DELTA
                                            ) AS "Relative_time",

                                EXTRACT
                                        (EPOCH FROM (
                                                    SELECT CAST ("l2_time" - INTERVAL '7 HOURS' AS TIME)
                                                    )
                                        ) - LAG (EXTRACT (
                                                            EPOCH FROM (
                                                                        SELECT CAST ("l2_time" - INTERVAL '7 HOURS' AS TIME)
                                                                        )
                                                        ), 1)
                                        OVER (
                                                ORDER BY EXTRACT (EPOCH FROM (
                                                                                SELECT CAST ("l2_time" - INTERVAL '7 HOURS' AS TIME)
                                                                                )
                                                                    )
                                            ) AS "Frame_Delta",

                                "Time_since_previous",
                                "src",
                                "dst",
                                "srcport",
                                "dstport",
                                "rel_ack",
                                "raw_ack",
                                "rel_seq",
                                "raw_seq",
                                "TCP_Flag",
                                "Analysis"
                            FROM TABLE_NAME

                        )

                SELECT 
                    *
                FROM RELATIVE_TIME
                '''%table
    return(v_query)

def f_postgresql_query (query):
    v_database = 'vzw_mec_sp'
    
    cn = pg.Connection (v_database)
    v_df = cn.PostgreSQL_query_df (query)
    
    return (v_df)


# ///////// BEGIN 
#os.system('clear')

path = "/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/"
v_file = '02132023'


dir_list = os.chdir(path)
v_files = os.system('ls | grep .pcap')


v_pcapmerge = []
for file in os.listdir(path):
    if file.endswith(".pcap"):
        v_pcapmerge.append(file)
        
v_cap_files = ' '.join(map(str,v_pcapmerge))
v_merge_command = ('mergecap -w  pcap_tcp_merge.pcap %s'%v_cap_files)
os.system(v_merge_command)


print ("1) Processing Retransmition analysis on file.....")

# Prints only pcap file present in My Folder
f_df = f_ret ('pcap_tcp_merge.pcap')

# Load dataframe to PostgreSQLß
f_postgresql_new_table (f_df,v_file)

print ("2) Done with Retransmition analysis on file.....")
print (" ######### ")

os.system('rm pcap_tcp_merge.pcap')

v_query = q_query(v_file)

v_df = f_postgresql_query (v_query)
v_df.to_csv ('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/tcp_retrans_%s.csv'%v_file)

print (v_df)

# ///////// END

