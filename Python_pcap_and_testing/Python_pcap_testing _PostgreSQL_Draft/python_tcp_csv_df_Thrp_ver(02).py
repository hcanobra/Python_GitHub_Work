





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

def f_thrp (file_name,file, v_file):
    
    # Open saved trace file 
    capture = pyshark.FileCapture(file_name, display_filter='(tcp.stream == 1) && (data.data != 0)')
    
    #packets = capture._packets()
    
    #v_thrp_df = pd.DataFrame()
    
    v_thrp_df = pd.Series()

    v_record = {}
    
    for pkt in capture:
        
        '''
        v_record = {
                    'idx': pkt.frame_info.time_epoch, 
                    'Time_since_previous': pkt.frame_info.time_delta, 
                    'Frame_length': pkt.length,
                    'src': pkt.ip.src,
                    'dst': pkt.ip.dst

                    }
        
        v_thrp_df = v_thrp_df.append({
                                    'idx': pkt.frame_info.time_epoch, 
                                    'Time_since_previous': pkt.frame_info.time_delta, 
                                    'Frame_length': pkt.length,
                                    'src': pkt.ip.src,
                                    'dst': pkt.ip.dst
                                    }, ignore_index=True)
        '''
        print (pkt.number)
        
        v_thrp_df = pd.concat([
                                v_thrp_df,
                                                pd.Series (
                                                                {
                                                                'idx': pkt.frame_info.time_epoch, 
                                                                'Time_since_previous': pkt.frame_info.time_delta, 
                                                                'Frame_length': pkt.length,
                                                                'src': pkt.ip.src,
                                                                'dst': pkt.ip.dst
                                                                }, index=['idx']
                                                            )
                                
                                ], axis = 1)

    
            
    # Move the column named time to the second position in the DataFrame
    v_thrp_df['l2_time'] = pd.to_datetime(v_thrp_df['idx'].astype(float) , unit='s', utc=True).map(lambda x: x.tz_convert('US/Mountain'))
    v_col = v_thrp_df.pop("l2_time")
    v_thrp_df.insert(1, "l2_time", v_col)  
    
    v_thrp_df = v_thrp_df.astype({
                                'Frame_length' : int
                                })
                                    
            
    pd.to_datetime(v_thrp_df['test']).map(lambda x: x.tz_convert('US/Mountain'))
            
    # Define which capture this file belog to, multiple files one capture
    v_thrp_df['Capture'] = v_file
                 
    # Add a column with file name as a reference
    v_thrp_df['Source'] = file
    return (v_thrp_df)

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


def q_query (table):
    v_query = '''


                '''%table
    return(v_query)



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
        f_df = f_thrp (file_name,file,v_file)
        
        print ("2) Done with file.....")
                
        # Load dataframe to PostgreSQL
        if f_df.empty == False:
            f_postgresql_new_table (f_df,v_file)
        
        os.system('date')
        print ("#######################################")

# ///////// END

