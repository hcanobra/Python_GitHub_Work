# importing sys
import sys
import os

import time
from datetime import datetime
from scapy.all import *
import pandas as pd

# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')

import PostgreSQL_API as pg

def f_initiate ():
    v_df1 = pd.DataFrame([])
    v_destination = ""
    v_ttl = 1
    data = {}
    v_delay = 10
    return (v_df1,v_destination,v_ttl,data,v_delay)

def f_postgresql_new_table (df):
    
    v_database = 'vzw_mec_sp'
    v_table = 'icmp_trace_pcap_test'
    
    cn = pg.Connection(v_database)
    cn.PostgreSQL_load_append_df (v_table,df)


#/// Begin

v_df1,v_destination,v_ttl,data,v_delay = f_initiate ()

v_df = pd.DataFrame([])
v_host = "15.181.163.0"

for cycle in range(2):

    while v_destination != v_host:

        ans,unans=sr(IP
                    (
                        dst=v_host,
                        ttl=v_ttl,
                        
                        
                    )/
                ICMP(), timeout=0.3
                )
        try:  
            data['Cycle'] = cycle
            data['Time'] = datetime.now()
            data['host'] = ans[0][0].dst
            data['dest'] = ans[0][1].src
            data['ttl'] = ans[0][0].ttl
            data['sent_time'] = ans[0][0].sent_time
            data['recv_time'] = ans[0][1].time
            
            data['RTT_ms'] = (ans[0][1].time - ans[0][0].sent_time)*1000
            
            v_df1 = v_df1.append(data,ignore_index=True)
            v_destination = ans[0][1].src

        except:
            pass
            
        v_ttl = v_ttl + 1
        
    print (v_df1)
    '''
    #Load dataframe to PostgreSQL
    if v_df1.empty == False:
        f_postgresql_new_table (v_df1)
    '''

    #v_df = pd.concat([v_df,v_df1], axis=0)
    
    v_df1,v_destination,v_ttl,data,v_delay = f_initiate ()


    time.sleep(v_delay)

#print (v_df)

#/// End