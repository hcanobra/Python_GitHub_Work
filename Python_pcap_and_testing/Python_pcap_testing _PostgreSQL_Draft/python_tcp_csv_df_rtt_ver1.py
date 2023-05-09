
'''

https://www.wireshark.org/docs/wsug_html_chunked/ChAdvTCPAnalysis.html //// TCP Analysis

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
import nest_asyncio



def f_rtt (file_name,file, v_file):
  
    #v_file = file_name
    
    # Open saved trace file 
    capture = pyshark.FileCapture(file_name, keep_packets=False, display_filter='tcp.analysis.ack_rtt > 0')
    
    v_rtt_df = pd.DataFrame()
    v_record = {}
    
    for pkt in capture:
        if ("TCP" in pkt):
            v_record = {
                        'idx': pkt.frame_info.time_epoch, 
                        'l2_frame_len': pkt.frame_info.len, 
                            
                        "l2_dst" : pkt.eth.dst,
                        "l2_src" : pkt.eth.src,
                        
                        "l3_ver" : pkt.ip.version,
                        "l3_hrd_len" : pkt.ip.hdr_len,
                        "l3_len" : pkt.ip.len,
                        "l3_ttl" : pkt.ip.ttl,
                        "l3_proto" : pkt.ip.proto,
                        "l3_cksum" : pkt.ip.checksum,
                        "l3_src" : pkt.ip.src,
                        "l3_dst" :pkt.ip.dst,
                        
                        "l4_srcport" : pkt.tcp.srcport,
                        "l4_dstport" : pkt.tcp.dstport,
                        "l4_len" : pkt.tcp.len,
                        "l4_seq_raw" : pkt.tcp.seq_raw,
                        "l4_ack_raw" : pkt.tcp.ack_raw,
                        "l4_hdr_len" : pkt.tcp.hdr_len,
                        "l4_window_size" : pkt.tcp.window_size_value,
                        "l4_cksum" : pkt.tcp.checksum,
                        "l4_tsval" : pkt.tcp.options_timestamp_tsval,
                        "l4_tsecr" : pkt.tcp.options_timestamp_tsecr,
                        "l4_analysis_RTT_to_Ack" : pkt.tcp.analysis_ack_rtt    
                        }    
            
            df_dictionary = pd.DataFrame([v_record])            
            v_rtt_df = pd.concat([v_rtt_df, df_dictionary], ignore_index=True)
            
            # Move the column named time to the second position in the DataFrame
            v_rtt_df['l2_time'] = pd.to_datetime(v_rtt_df['idx'].astype(float) , unit='s', utc=True).map(lambda x: x.tz_convert('US/Mountain'))
            v_col = v_rtt_df.pop("l2_time")
            v_rtt_df.insert(1, "l2_time", v_col)  
            
            v_rtt_df = v_rtt_df.astype({
                'l2_frame_len' : int,
                'l3_hrd_len' : int,
                'l3_len' : int,
                'l3_ttl' : int,
                'l4_len' : int,
                'l4_seq_raw' : int,
                'l4_ack_raw' : int,
                'l4_hdr_len' : int,
                'l4_window_size' : int,
                'l4_tsval' : int,
                'l4_tsecr' : int,
                'l4_analysis_RTT_to_Ack' : float
                })
    
    # Define which capture this file belog to, multiple files one capture
    v_rtt_df['Capture'] = v_file
                 
    # Add a column with file name as a reference
    v_rtt_df['Source'] = file
    return (v_rtt_df)

def f_postgresql_new_table (df,table):
    
    v_database = 'vzw_mec_sp'
    v_table = 'pcap_tables_tcp_rtt'
    
    cn = pg.Connection(v_database)
    cn.PostgreSQL_load_append_df (v_table,df)

def q_query (table):
    v_query = '''


WITH
	TABLE_NAME AS
		(
		SELECT * FROM  public.pcap_tables_tcp_rtt
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

				"l3_src",
				"l3_dst",
				"l4_seq_raw",
				"l4_ack_raw",
				"l4_srcport",
				"l4_dstport",
				"l4_analysis_RTT_to_Ack",
				"Thrp",
				"Source"
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
nest_asyncio.apply()
os.system('clear')

path = "/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/"
v_file = '02142023'

dir_list = os.listdir(path)

for file in os.listdir(path):
    if file.endswith(".pcap"):

        file_name = path+file
        print ("#######################################")
        os.system('date')

        print ("1) Processing file: ",file_name)

        # Rout trip delay calculation
        f_df = f_rtt (file_name,file,v_file)
        
        print ("2) Done with file.....")
                
        # Load dataframe to PostgreSQL
        if f_df.empty == False:
            f_postgresql_new_table (f_df,v_file)
        
        os.system('date')
        print ("#######################################")

#v_query = q_query(v_file)

#v_df = f_postgresql_query (v_query)
#v_df.to_csv ('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/tcp_rtt_%s.csv'%v_file,index=False)

#print (v_df)

#v_df["l4_analysis_ack_rtt"] = v_df["l4_analysis_ack_rtt"].astype(float) * 1000
      
#v_rtt_plot = v_df[["l4_analysis_ack_rtt","l2_time"]]


#print (v_rtt_plot.head())
#print (v_rtt_plot.info())

#v_rtt_plot.plot (kind ='scatter', x='l2_time', y='l4_analysis_ack_rtt')
#plt.show()

# ///////// END