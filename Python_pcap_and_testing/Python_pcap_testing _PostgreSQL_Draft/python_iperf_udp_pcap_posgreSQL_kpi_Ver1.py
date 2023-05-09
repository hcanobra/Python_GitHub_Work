


# importing sys
import sys
  
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')

import pandas as pd
import os
import PostgreSQL_API as pg
import re



def f_formating (df,file):

    df2 = df[10]
    df = df[[2,4,6,8]]
    
    df2 = df2.str.split('/', expand=True)
    df2.columns = [
                    'Lost',
                    'Total'
                    ]

    

    df.columns = [
                    'Interval',
                    'Transfer',
                    'Bitrate',
                    'Jitter'
                    ]

    df = pd.concat([df,df2], axis=1)
    
    
    words = file.split('.')
    df['Source'] = words[0]
    
    df = df.astype({
                'Transfer': float,
                'Bitrate': float,
                'Jitter': float,
                'Lost': int,
                'Total': int
                })
    
    print (df)
    
    return (df)

def f_process_file (path,file):
    with open(path+file) as full_file:
        lines = [line.rstrip() for line in full_file]
        
    f_len = len(lines)

    v_list =  lines[5:f_len-7]

    v_list = [re.sub('\s+', ' ', x) for x in v_list]

    v_df = pd.DataFrame ([sub.split(" ") for sub in v_list])

    v_df = f_formating (v_df,file)

    return (v_df)

def f_postgresql_new_table (df):
    
    v_database = 'vzw_mec_sp'
    v_table = 'pcap_tables_udp'
    
    cn = pg.Connection(v_database)
    cn.PostgreSQL_load_append_df (v_table,df)

# ///////// BEGIN 
os.system('clear')

path = "/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_udp/"
#file = 'Readme_02142023.txt'

dir_list = os.listdir(path)

for file in os.listdir(path):
    if file.endswith(".txt"):

        print ("#######################################")
        os.system('date')

        print ("1) Processing file: ",file)
        f_df = f_process_file (path,file)
        
        # Load dataframe to PostgreSQL
        if f_df.empty == False:
            f_postgresql_new_table (f_df)
        
        print ("2) Done with file.....",file)
        
        os.system('date')
        print ("#######################################")
        
# ///////// END