'''
# importing sys
import sys
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')
'''

from npe import ndl2 as ndl
#import ndl2 as ndl
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import time


def c_NDL_Query ():
    cn = ndl.Connection()
            
    v_data = cn.commands('select * from truecall_core.f_truecall_lsr_raw_v1 limit 10 ')
    print (v_data.head())
            

    cn.close
    
    return ()


def f_using_halls ():

    #c_NDL_Query (q_NDL_truecall_Query())

    conn = ndl.Connection("canobhu", "Tpztlan02VH(")
    df = conn.hql_query_df(q_query1())
        
    print (df)
    # ALWAYS CLOSE CONNECTION AFTERWARDS!
    conn.close()
   
def q_query2 (): 
    v_query = ('''
                SELECT 
                    DISTINCT (to_date(trans_dt,'yyyymmdd')) AS trans_dt
                FROM truecall_core.f_truecall_lsr_raw_v1  
                ORDER BY trans_dt
                ''')
    return (v_query)
    
def q_query1 ():
    v_query = ('''
                SELECT 
                    environment,
                    end_location_lat,
                    end_location_lon,
                    make,
                    model,
                    service_type,
                    start_time,
                    end_time,
                    final_disposition,
                    start_enb,
                    end_enb,
                    s1_release_cause,
                    rsrp_dbm,
                    rsrq_db,
                    data_lost,
                    mac_volume_dl_bytes,
                    mac_volume_ul_bytes,
                    pdcp_volume_dl_bytes,
                    pdcp_volume_ul_bytes,
                    qci_list,
                    n1_rsrp_dbm,
                    n2_rsrp_dbm,
                    n3_rsrp_dbm,
                    pusch_sinr_db,
                    ue_power_headroom_db,
                    ta_distance_meters,
                    intersite_distance_meters,
                    imsi,
                    mean_ul_sinr_db,
                    nr_rsrp_dbm,
                    nr_rsrq_db,
                    nr_dl_sinr_db,
                    to_date(trans_dt,'yyyymmdd') AS trans_dt,
                    hr,
                    submkt
                FROM truecall_core.f_truecall_lsr_raw_v1  
                WHERE 
                    to_date(trans_dt,'yyyymmdd') = to_date('2022-07-11','yyyy-mm-dd')
                    AND
                    submkt = 'MTN'
                    AND
                    confidence IN ('High','Medium')
                    AND
                    rsrp_dbm < -124
                    AND
                    make IN ('APPLE','SAMSUNG','GOOGLE','MOTOROLA','LG')
                    AND
                    rsrp_dbm is not null
                        
                LIMIT 10
                ''')
    return (v_query)


# Begin
#c_NDL_Query ()
f_using_halls ()