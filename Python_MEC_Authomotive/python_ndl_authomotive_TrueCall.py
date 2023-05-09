"""


f_PostgreSQL_open

f_PostgreSQL_close
    conn

f_postgreSQL_inport 
    v_data
    v_table
    v_conn

q_NDL_Fuze_PROJ_Query


c_NDL_Query


"""

# importing sys
import sys
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')
sys.path.append('/Users/canobhu/Library/Python/3.8/lib/python/site-packages/npe')


import ndl as ndl
import PostgreSQL_API as pg
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from sqlalchemy import text
import time


def f_PostgreSQL_open ():
  
    engine = create_engine("postgresql+psycopg2://postgres:Tpztlan02VH@localhost/vzw_truecall")
    conn = engine.connect()

    return(conn)

def f_PostgreSQL_close (conn):
    conn.close()
    return ()

def f_postgreSQL_inport (v_data, v_table, v_conn):
    
    v_data.to_sql(v_table, con = v_conn, if_exists = 'append', index=False)
    return()

def q_NDL_truecall_Query ():
    v_sql_commands = ('''
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
                    trans_dt AS trans_dt,
                    hr,
                    submkt
                FROM truecall_core.f_truecall_lsr_raw_v1  
                WHERE 
                    trans_dt = '20221015'
                    AND
                    submkt = 'MTN'
                    AND
                    imsi = '311480636968915'
                ''')
    return (v_sql_commands)
    
def c_NDL_Query (v_query,v_table):
    conn = ndl.Connection("canobhu", "Tpztlan02VH(")        
    print (v_query)    
    v_data = conn.hql_query_df(v_query)
    print (v_data.head())

    v_conn = f_PostgreSQL_open()
    f_postgreSQL_inport (v_data, v_table, v_conn)
    f_PostgreSQL_close (v_conn)
            

    conn.close
    
    return ()

def f_dataframe (v_date,v_market,v_mk):
    
    c_NDL_Query (q_NDL_truecall_Query(v_date,i_records,j_records,k_records),'truecall_presto_views_f_truecall_lsr_raw_v0_mk%s_%s'%(v_market,v_date))

    return ()

# // Begining
v_date = '20221015'
v_market = '12' 
v_mk = ['12%',"312%"]

c_NDL_Query (q_NDL_truecall_Query(),'truecall_presto_views_f_truecall_lsr_raw_v0_mk%s_%s'%(v_market,v_date))
#f_dataframe (v_date,v_market,v_mk)

# // End


