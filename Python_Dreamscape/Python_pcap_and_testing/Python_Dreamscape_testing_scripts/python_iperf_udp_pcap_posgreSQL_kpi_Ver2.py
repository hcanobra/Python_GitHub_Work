


# importing sys
import sys
  
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')

import pandas as pd
import os
import PostgreSQL_API as pg
import re



def f_formating (df,capture,file):

    df2 = df[15]
    df = df[[0,7,9,11,13]]
    
    df2 = df2.str.split('/', expand=True)
    df2.columns = [
                    'Lost',
                    'Total'
                    ]

    

    df.columns = [
                    'Date_time',
                    'Interval',
                    'Transfer',
                    'Bitrate',
                    'Jitter'
                    ]

    df = pd.concat([df,df2], axis=1)
        
    df['Capture'] = capture

    #words = file.split('/')
    #df['Source'] = words[8]
    
    
    df = df.astype({
                'Transfer': float,
                'Bitrate': float,
                'Jitter': float,
                'Lost': int,
                'Total': int
                })
    
    print (df)
    
    return (df)

def f_process_file (capture,file):
    
    with open(file) as full_file:
        lines = [line.rstrip() for line in full_file]
        
    f_len = len(lines)

    v_list =  lines[4:f_len-7]

    v_list = [re.sub('\s+', ' ', x) for x in v_list]

    v_df = pd.DataFrame ([sub.split(" ") for sub in v_list])
    
    v_df[0] = v_df[[1,2,4,3]].apply("_".join, axis=1)

    v_df = f_formating (v_df,capture,file)

    return (v_df)

def f_postgresql_new_table (df):
    
    v_database = 'vzw_mec_sp'
    v_table = 'udp_pcap'
    
    cn = pg.Connection(v_database)
    cn.PostgreSQL_load_append_df (v_table,df)

# ///////// BEGIN 
os.system('clear')

path = "/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_udp/"

dir_list = os.listdir(path)
dir_list = sorted(dir_list)

for file in dir_list:
    if file.endswith(".txt"):

        file_name = path+file
        print ("#######################################")
        os.system('date')

        print ("1) Processing file: ",file_name)
        v_capture = file.split('_')[3]+"_"+file.split('_')[4]+"_"+file.split('_')[5]+"_"+file.split('_')[6].split('.')[0]
        
        f_df = f_process_file (v_capture,file_name)
        
        # Load dataframe to PostgreSQL
        if f_df.empty == False:
            f_postgresql_new_table (f_df)
        
        print ("2) Done with file.....",file)
        
        os.system('date')
        print ("#######################################")
   
# ///////// END


''



''