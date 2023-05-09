

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
        with open('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_rtt.csv', 'a') as f:
            v_columns = (
                            'idx' + ',' +
                            'l2_frame_len' + ',' +
                                
                            "l3_src" + ',' +
                            "l3_dst" + ',' +
                            
                            "l4_srcport" + ',' +
                            "l4_dstport" + ',' +
                            "l4_analysis_RTT_to_Ack"
                        )
            f.write(v_columns)
            f.write('\n')
            
        cap = pyshark.FileCapture(file_name, keep_packets=False, display_filter='tcp.analysis.ack_rtt > 0')
        cap.apply_on_packets(f_rtt_layers)
    
    elif option == 'ret':
        # Open saved trace file 
        with open('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_ret.csv', 'a') as f:
            v_columns = (
                        'idx' + ',' +
                        "l3_src" + ',' +
                        "l3_dst" + ',' +
                        "l4_srcport" + ',' +
                        "l4_dstport" + ',' +
                        'Analysis'
                        )
            f.write(v_columns)
            f.write('\n')
            
        cap = pyshark.FileCapture(file_name, display_filter='tcp.analysis.out_of_order or tcp.analysis.retransmission or tcp.analysis.spurious_retransmission')
        cap.apply_on_packets(f_ret_layers)
        
    elif option == 'thrpt':
        # Open saved trace file 
        with open('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_thrp.csv', 'a') as f:
            v_columns = (
                        'idx' + ',' +
                        'l2_Frame_length' + ',' +
                        "l3_src" + ',' +
                        "l3_dst"
                        )
            f.write(v_columns)
            f.write('\n')

        cap = pyshark.FileCapture(file_name, display_filter='data.data != 0')
        cap.apply_on_packets(f_thrpt_layers)
    
    return ()

def f_rtt_layers(packet):
    
    v_record = (
                packet.frame_info.time_epoch+ "," +
                packet.frame_info.len+ "," +
                    
                packet.ip.src+ "," +
                packet.ip.dst+ "," +
                
                packet.tcp.srcport+ "," +
                packet.tcp.dstport+ "," +
                packet.tcp.analysis_ack_rtt
                )
    
    with open('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_rtt.csv', 'a') as f:
        f.write(v_record)
        f.write('\n')

    return ()

def f_ret_layers(packet):
        
    v_record = (
                packet.frame_info.time_epoch + ',' +
                packet.ip.src + ',' +
                packet.ip.dst + ',' +
                packet.tcp.srcport + ',' +
                packet.tcp.dstport + ',' +
                packet.tcp._ws_expert 
                )
    
    with open('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_ret.csv', 'a') as f:
        f.write(v_record)
        f.write('\n')
     
    return ()

def f_thrpt_layers(packet):
        
    v_record = (
                packet.frame_info.time_epoch + ',' +
                packet.length + ',' +
                packet.ip.src + ',' +
                packet.ip.dst
                )
    
    with open('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_thrp.csv', 'a') as f:
        f.write(v_record)
        f.write('\n')
    
    
    return (v_record)

def f_df_rtt (v_capture,file):
    
    v_df_rtt = pd.read_csv ('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_rtt.csv')
    if v_df_rtt.empty:
        pass
    else:
        #do something
        
        # Move the column named time to the second position in the DataFrame
        v_df_rtt['l2_time'] = pd.to_datetime(v_df_rtt['idx'].astype(float) , unit='s', utc=True).map(lambda x: x.tz_convert('US/Mountain'))
        v_col = v_df_rtt.pop("l2_time")
        v_df_rtt.insert(1, "l2_time", v_col) 
        
        v_df_rtt['Capture'] = v_capture
        v_df_rtt['File'] = file
        f_postgresql_new_table (v_df_rtt,'readme_rtt')
        
        print (v_df_rtt.head(2))
    
    return ()

def f_df_ret (v_capture,file):
    
    v_df_ret = pd.read_csv ('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_ret.csv')
    if v_df_ret.empty:
        pass
    else:
        #do something
        v_df_ret['l2_time'] = pd.to_datetime(v_df_ret['idx'].astype(float) , unit='s', utc=True).map(lambda x: x.tz_convert('US/Mountain'))
        v_col = v_df_ret.pop("l2_time")
        v_df_ret.insert(1, "l2_time", v_col) 
        
        v_df_ret['Capture'] = v_capture
        v_df_ret['File'] = file
        f_postgresql_new_table (v_df_ret,'readme_ret')

        print (v_df_ret.head(2))
    
    return ()

def f_df_thrpt (v_capture,file):
    
    v_df_thrpt = pd.read_csv ('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_thrp.csv')
    if v_df_thrpt.empty:
        pass
    else:
        #do something
        v_df_thrpt['l2_time'] = pd.to_datetime(v_df_thrpt['idx'].astype(float) , unit='s', utc=True).map(lambda x: x.tz_convert('US/Mountain'))
        v_col = v_df_thrpt.pop("l2_time")
        v_df_thrpt.insert(1, "l2_time", v_col) 
        
        v_df_thrpt['Capture'] = v_capture
        v_df_thrpt['File'] = file
        f_postgresql_new_table (v_df_thrpt,'readme_thrp')

        print (v_df_thrpt.head(2))
    
    return ()

def f_postgresql_new_table (df,table):
    
    v_database = 'vzw_mec_sp'
    v_table = table
    
    cn = pg.Connection(v_database)
    cn.PostgreSQL_load_append_df (v_table,df)

def f_postgresql_query (query):
    v_database = 'vzw_mec_sp'
    
    cn = pg.Connection (v_database)
    v_df = cn.PostgreSQL_query_df (query)
    
    return (v_df)

# ///////// BEGIN 
nest_asyncio.apply()
os.system('clear')

path = "/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/"
#v_file = '02142023'

record = []

dir_list = os.listdir(path)
dir_list = sorted(dir_list)


for file in dir_list:
    if file.endswith(".pcap"):

        file_name = path+file
        print ("#######################################")
        os.system('date')

        print ("1) Processing file: ",file_name)
        v_capture = file.split('_')[2]+"_"+file.split('_')[3]+"_"+file.split('_')[4]+"_"+file.split('_')[5]
        
        # Rout trip delay calculation
        v_cap = f_cap_filter ('rtt')
        f_df_rtt (v_capture,file)
        if os.path.exists('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_rtt.csv'):
            os.remove('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_rtt.csv')
                
        # Rout trip delay calculation
        v_cap = f_cap_filter ('ret')
        f_df_ret (v_capture,file)
        if os.path.exists('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_ret.csv'):
            os.remove('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_ret.csv')
        # Rout trip delay calculation
        v_cap = f_cap_filter ('thrpt')
        f_df_thrpt (v_capture,file)
        if os.path.exists('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_thrp.csv'):
            os.remove('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_thrp.csv')
                
        print ("2) Done with file.....")
        
        os.system('date')
        print ("#######################################")

# ///////// END





# RTT Query
'''
select * from public.readme_rtt


WITH
	TABLE_NAME AS
		(
		SELECT * FROM  public.readme_rtt
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
				"Capture"
				"File"
			FROM TABLE_NAME

		)

SELECT 
	*
FROM RELATIVE_TIME



select * from public.readme_rtt


WITH 
	MINUTE_AGG AS
	(
		SELECT 
			date_trunc('SECOND', "l2_time") AS MINUTE,
			AVG("l4_analysis_RTT_to_Ack") AS RTT,
			"l3_src",
			"l3_dst",
			"Capture",
			"File"
		FROM public.readme_rtt
		GROUP BY 
			date_trunc('SECOND', "l2_time"),
			"l3_src",
			"l3_dst",
			"Capture",
			"File"
		ORDER BY date_trunc('SECOND', "l2_time")

	)
	
SELECT * FROM MINUTE_AGG 


'''

# Throughut Query

'''
SELECT * FROM public.readme_thrp


WITH
	TABLE_NAME AS
		(
		SELECT * FROM  public.readme_thrp
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

				"Frame_ID",
				"Frame_length",
				"src",
				"dst",
				"Capture",
				"File"
			FROM TABLE_NAME

		)

SELECT 
	*
FROM RELATIVE_TIME


WITH 
	MINUTE_AGG AS
	(
		SELECT 
			date_trunc('SECOND', "l2_time") AS MINUTE,
			(SUM("Frame_length"))*8/1000000 AS Thrpht_Mbps,
			"src",
			"dst",
			"Capture",
			"File"
		FROM public.readme_thrp
		GROUP BY 
			date_trunc('SECOND', "l2_time"),
			"src",
			"dst",
			"Capture",
			"File"
		ORDER BY date_trunc('SECOND', "l2_time")

	)
	
SELECT * FROM MINUTE_AGG 


'''