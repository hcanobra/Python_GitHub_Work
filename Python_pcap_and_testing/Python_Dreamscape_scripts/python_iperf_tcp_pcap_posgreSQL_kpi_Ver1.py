

# importing sys
import sys
  
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')

import PostgreSQL_API as pg
import pyshark  
import pandas as pd
from datetime import datetime
import os
import nest_asyncio


def f_postgresql_query (query):
    v_database = 'vzw_mec_sp'
    
    cn = pg.Connection (v_database)
    v_df = cn.PostgreSQL_query_df (query)
    
    return (v_df)

def f_postgresql_new_table (df,table):
    
    v_database = 'vzw_mec_sp'
    v_table = table
    
    cn = pg.Connection(v_database)
    cn.PostgreSQL_load_append_df (v_table,df)

def f_pcap_df (v_capture,file):
    
    v_df = pd.read_csv ('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_pcap.csv')
    if v_df.empty:
        pass
    else:
        #do something
        
        # Move the column named time to the second position in the DataFrame
        v_df['l2_time'] = pd.to_datetime(v_df['idx_time'].astype(float) , unit='s', utc=True).map(lambda x: x.tz_convert('US/Mountain'))
        v_col = v_df.pop("l2_time")
        v_df.insert(1, "l2_time", v_col) 
        
        v_df['Capture'] = v_capture
        v_df['File'] = file
        f_postgresql_new_table (v_df,'tcp_pcap')
        
        print (v_df.head(2))
    
    return ()

def f_pkt_csv (packet):
    
    v_thrghp = ''
    v_rtt = ''
    v_ret = ''
    
    if hasattr(packet, 'DATA'):
        v_thrghp = packet.length
    
    if hasattr(packet.tcp, 'analysis_ack_rtt'):
        v_rtt = packet.tcp.analysis_ack_rtt
    
    if hasattr(packet.tcp, '_ws_expert'):
        v_ret = packet.tcp._ws_expert 
        
    v_record = (
                packet.frame_info.time_epoch + ',' +
                packet.ip.src + ',' +
                packet.ip.dst + ',' +

                packet.tcp.srcport + ',' +
                packet.tcp.dstport + ',' +
                
                v_thrghp + ',' +
                v_rtt + ',' +
                v_ret
                )
    
    with open('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_pcap.csv', 'a') as f:
        f.write(v_record)
        f.write('\n')
        

    return ()


def f_pcap_filter ():
    
    
    with open('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_pcap.csv', 'a') as f:
        v_columns = (
                    'idx_time' + ',' +
                    "l3_src" + ',' +
                    "l3_dst" + ',' +

                    "l4_srcport" + ',' +
                    "l4_dstport" + ',' +

                    "l2_frame_size_thrp" + ',' +
                    "l2_rtt" + ',' +
                    "l2_ret"
                    )
        
        f.write(v_columns)
        f.write('\n')
    

    cap = pyshark.FileCapture(file_name, keep_packets=False)
    cap.apply_on_packets(f_pkt_csv)
    
    
    return ()


# ///////// BEGIN 
nest_asyncio.apply()
os.system('clear')

path = "/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/"

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
        

        
        f_pcap_filter ()
        f_pcap_df (v_capture,file_name)
        
        if os.path.exists('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_pcap.csv'):
            os.remove('/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/readme_pcap.csv')

                
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







WITH 
	RTT_AGG AS
	(
		SELECT 
			date_trunc('SECOND', "l2_time") AS MINUTE,
			AVG("l2_rtt")*1000 AS RTT,
			l3_src,
			l3_dst,
			"Capture",
			"File"
		FROM public.tcp_pcap
		GROUP BY 
			date_trunc('SECOND', "l2_time"),
			"Capture",
			"File"
		ORDER BY date_trunc('SECOND', "l2_time")

	)
	
SELECT * FROM RTT_AGG

'''