"""


f_PostgreSQL_open

f_PostgreSQL_close
    conn

f_postgreSQL_inport 
    v_data
    v_table
    v_conn

c_sql_to_csv
    v_query

q_NDL_Fuze_PROJ_Query

q_NDL_Fuze_Dash_Query

c_NDL_Query
    v_query
    v_table

"""

# importing sys
import sys
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')


import ndl_API as ndl
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import time


def f_PostgreSQL_open ():
  
    engine = create_engine("postgresql+psycopg2://postgres:Tpztlan02VH@localhost/vzw_xlpt")
    conn = engine.connect()

    return(conn)

def f_PostgreSQL_close (conn):
    conn.close()
    return ()

def f_postgreSQL_inport (v_data, v_table, v_conn):
    
    v_data.to_sql(v_table, con = v_conn, if_exists = 'append', index=False)
    return()

def c_sql_to_csv (v_query):
    v_databasae = 'vzw_atoll'
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                        .format(user="hcanobra",
                                pw="Tpztlan02VH",
                                db=v_databasae))
    
    v_columns = engine.execute(v_query).keys() # Obtains the column names from the DB
    v_data = engine.execute (v_query) # Execure the Query on the DB
    
    v_data = pd.DataFrame(data=v_data) # Transform the result of the query into Pandas DataFrame 

    v_data.columns = v_columns # Add colum names to DataFrame

    return (v_data)

def q_NDL_xLPT_Query (y,m,d,mk):
    v_sql_commands = ('''
select 
        "day",
        "hr",
        "date_time",
        "mmepool",
        "region",
        "market",
        "market_desc",
        "site",
        "enodeb",
        "eutrancell",
        "carrier",
        "freq",
        "setup_fail_pct_num",
        "setup_fail_pct_den",
        "context_drop_pct_num",
        "context_drop_pct_den",
        "sector_dl_throughput",
        "rrc_setup_failure_pct_num",
        "rrc_setup_failure_pct_den",
        "bearer_setup_failure_pct_num",
        "bearer_setup_failure_pct_den",
        "bearer_drop_pct_num",
        "bearer_drop_pct_den",
        "context_setup_failure_pct_num",
        "context_setup_failure_pct_den",
        "cell_availability",
        "rrc_establishmentatt",
        "rrc_setup_failures",
        "ue_dolwnlink_latency_msec",
        "ue_downlink_throughput",
        "avg_ue_downlink_pkts_lost",
        "avg_ue_downlink_pkts",
        "avg_ue_uplink_pkts_lost",
        "avg_ue_uplink_pkts",
        "handover_preparation_att",
        "handover_attempts",
        "ue_uplink_throughput_mbps",
        "volte_mou",
        "volte_attempts",
        "bearer_setup_failure_pct_qci1_den",
        "bearer_setup_failure_pct_qci1_num",
        "cell_throughput_mbps",
        "downlink_throughput_in_mbps",
        "rtp_gap_count_large",
        "rtp_gap_count_medium",
        "rtp_gap_count_small",
        "rtp_gap_count_total",
        "rtp_gap_count_x_small",
        "rtp_gap_length_avg_sec_per_gap",
        "rtp_gap_length_total_sec",
        "s1u_sip_sc_avgcallsetuptime_ms",
        "s1u_sip_sc_avgcalltime_sec",
        "s1u_sip_sc_avgdisconnecttime_ms",
        "sip_sc_call_attempts",
        "sip_sc_call_completions",
        "sip_sc_call_drops",
        "rrc_drop_pct_num",
        "rrc_drop_pct_den",
        "bearer_drop_pct_voice_num",
        "bearer_drop_pct_voice_den",
        "bearer_setup_failure_pct_voice_den",
        "bearer_setup_failure_pct_voice_num",
        "rach_failure_pct_den",
        "rach_failure_pct_num",
        "adjusted_sip_sc_dc_pct_den",
        "adjusted_sip_sc_dc_pct_num",
        "volte_sc_ia_pct_den_airwave",
        "volte_sc_ia_pct_num_airwave",
        "trans_dt"
from elpt.elpt_enb_sec_carrier_hrlyv2_o

WHERE 
    mmepool = 'Mountain' 
    AND
    market = '%s'
    AND
    YEAR(trans_dt) = %s
    AND
    MONTH(trans_dt) = %s
    AND
    DAY(trans_dt) = %s
                    
                '''%(mk,y,m,d))
    return (v_sql_commands)

def q_NDL_xLPT_enb_hr (y,m,d,mk):
    v_sql_commands = ('''
select 
        "day",
        "hr",
        "date_time",
        "mmepool",
        "region",
        "market",
        "market_desc",
        "site",
        "enodeb",
        "eutrancell",
        "carrier",
        "freq",
        "setup_fail_pct_num",
        "setup_fail_pct_den",
        "context_drop_pct_num",
        "context_drop_pct_den",
        "sector_dl_throughput",
        "rrc_setup_failure_pct_num",
        "rrc_setup_failure_pct_den",
        "bearer_setup_failure_pct_num",
        "bearer_setup_failure_pct_den",
        "bearer_drop_pct_num",
        "bearer_drop_pct_den",
        "context_setup_failure_pct_num",
        "context_setup_failure_pct_den",
        "cell_availability",
        "rrc_establishmentatt",
        "rrc_setup_failures",
        "ue_dolwnlink_latency_msec",
        "ue_downlink_throughput",
        "avg_ue_downlink_pkts_lost",
        "avg_ue_downlink_pkts",
        "avg_ue_uplink_pkts_lost",
        "avg_ue_uplink_pkts",
        "handover_preparation_att",
        "handover_attempts",
        "ue_uplink_throughput_mbps",
        "volte_mou",
        "volte_attempts",
        "bearer_setup_failure_pct_qci1_den",
        "bearer_setup_failure_pct_qci1_num",
        "cell_throughput_mbps",
        "downlink_throughput_in_mbps",
        "rtp_gap_count_large",
        "rtp_gap_count_medium",
        "rtp_gap_count_small",
        "rtp_gap_count_total",
        "rtp_gap_count_x_small",
        "rtp_gap_length_avg_sec_per_gap",
        "rtp_gap_length_total_sec",
        "s1u_sip_sc_avgcallsetuptime_ms",
        "s1u_sip_sc_avgcalltime_sec",
        "s1u_sip_sc_avgdisconnecttime_ms",
        "sip_sc_call_attempts",
        "sip_sc_call_completions",
        "sip_sc_call_drops",
        "rrc_drop_pct_num",
        "rrc_drop_pct_den",
        "bearer_drop_pct_voice_num",
        "bearer_drop_pct_voice_den",
        "bearer_setup_failure_pct_voice_den",
        "bearer_setup_failure_pct_voice_num",
        "rach_failure_pct_den",
        "rach_failure_pct_num",
        "adjusted_sip_sc_dc_pct_den",
        "adjusted_sip_sc_dc_pct_num",
        "volte_sc_ia_pct_den_airwave",
        "volte_sc_ia_pct_num_airwave",
        "trans_dt"
from elpt.elpt_enb_sec_carrier_hrlyv2_o

WHERE 
    mmepool = 'Mountain' 
    AND
    market = '%s'
    AND
    YEAR(trans_dt) = %s
    AND
    MONTH(trans_dt) = %s
    AND
    DAY(trans_dt) = %s
                    
                '''%(mk,y,m,d))
    return (v_sql_commands)


def q_NDL_Fuze_Dash_Query ():
    v_sql_commands = ('''
    
                        SELECT *
                        FROM  fuze_presto_views.dmp_rfds_sp_fuze_dash_view 

                    ''')
    return (v_sql_commands)
    
def c_NDL_Query (v_query,v_table):
    cn = ndl.Connection()
    
    v_data = cn.commands(v_query)
    print (v_data.head())

    
    v_conn = f_PostgreSQL_open()
    f_postgreSQL_inport (v_data, v_table, v_conn)
    f_PostgreSQL_close (v_conn)
    

    cn.close
    
    return ()


# // Begining

v_year = [2021]
v_mrket = ['010']

for mk in v_mrket:
    for year in v_year:
        for month in range (1, 13):
            for day in range (1, 32):

                c_NDL_Query (q_NDL_xLPT_Query(year,month,day,mk),'elpt_presto_views_elpt_enb_sec_carrier_hrlyv2')
                time.sleep(30)


# // End


'''
                AND MONTH(to_date (day,'mm/dd/yyyy')) = %s



select * from elpt.f_daily_bh_ericssoncellkpisdata_sector_raw_v1 limit 2

xselect distinct (day)
from elpt.f_daily_bh_ericssoncellkpisdata_sector_raw_v1
WHERE mmepool in ('Mountain')


select  
    *
from elpt.f_daily_bh_ericssoncellkpisdata_sector_raw_v1
WHERE mmepool in ('Mountain','Kansas/Missouri')
AND to_date (day,'mm/dd/yyyy') between to_date ('2022-01-01','yyyy-mm-dd') and to_date ('2022-01-03','yyyy-mm-dd')
limit 2


select * from elpt.f_daily_bh_ericssoncellkpisvolte_sector_raw_v1  limit 2



########################

                SELECT  
                    *
                FROM elpt.f_daily_bh_ericssoncellkpisvolte_sector_raw_v1
                WHERE mmepool in ('Mountain','Kansas/Missouri')
                AND MONTH(to_date (day,'mm/dd/yyyy')) = %s
                AND YEAR(to_date (day,'mm/dd/yyyy')) = %s

'''