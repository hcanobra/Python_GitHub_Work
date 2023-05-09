

# importing sys
import sys
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')

from numpy import isnan
import numpy as np
import PostgreSQL_API as pg
import pandas as pd
import geopandas as gp
import time


from sqlalchemy import create_engine, engine

def q_posgresql_truecall_query ():
    v_sql_commands = ('''
                    SELECT * FROM public.truecall_presto_views_f_truecall_lsr_raw_v0_mk13_03162022
                    
                    ''')
    return (v_sql_commands)

def c_postgresql_locations ():
    v_databasae = 'vzw_truecall'
    
    cn = pg.Connection('vzw_truecall')
    
    
    v_data =cn.PostgreSQL_query_df (q_posgresql_truecall_query())
    
    print ("hello....")
        
    v_data = v_data.sample(frac=0.9, replace=True, random_state=1)

    cn.PostgreSQL_load_geo('vzw_truecall_geo_mk13_03162022', v_data,'end_location_lon','end_location_lat')
    
    return()    

def q_posgresql_Fuze_cband_ready_query ():
    v_sql_commands = ('''
                    SELECT 
                    fp.Projects_Fuze_project_id,
                    fp.Projects_Site_name,
                    fp.Projects_site_info_id,
                    STR_TO_DATE(Projects_activation_forecast_date,'%m/%d/%Y') as Project_Activation_Withdraw_Milestone_F,
                    fp.Projects_trans_contr_bandwidth,
                    fp.Projects_plan_year,
                    fp.Projects_Subtype,
                    fp.Projects_atoll_site_latitude,
                    fp.Projects_atoll_site_longitude,
                    ds.Dashboar_C_Band_bucket,
                    fp.Projects_local_market,
                    fp.Projects_Status,
                    ds.Dashboar_Status,
                    "CBand_Ready" as CBand_Status,
                    fp.Projects_trans_dt

                    FROM public.vzw_fuze_proj fp
                    JOIN public.vzw_fuze_dash ds on fp.Projects_Fuze_project_id = ds.Dashboar_Fuze_project_id

                    WHERE 
                    ds.Dashboar_C_Band_bucket = 'Built/Capable'
                    AND
                    fp.Projects_Subtype = '5G L-Sub6 - Carrier Add'
                        
                    ''')
    return (v_sql_commands)


# ///////// BEGIN 


c_postgresql_locations ()                                       # AFTER INFORMAITON IS EXTRACTED FROM FUZE VIA NDL THIS FUNCITON JOINS BOTH TABLES, AND GENERATES TWO TABLES, 
                                                                # 1ST TABLE) CONTAINING FUZE PROJECTS SOME BASIC INFORMAIOTN ABOUT THE PROJECT AND THE LAT LONG INFORMATION --- NAMED: vzw_fuze_loc
                                                                # 2ND TABLE) CONTAINING PROJECT INFORMATION AND DASHBOARD INFORMATION - NAMED: vzw_fuze_qgis

# ///////// END 
