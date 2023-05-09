

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
                    SELECT * FROM public."Ookla_Jan_2022"
                    
                    ''')
    return (v_sql_commands)

def c_postgresql_locations ():
    v_databasae = 'vzw_truecall'
    
    cn = pg.Connection('vzw_truecall')
    
    
    v_data =cn.PostgreSQL_query_df (q_posgresql_truecall_query())
    
    print ("hello....")
        
    v_data = v_data.sample(frac=0.9, replace=True, random_state=1)

    cn.PostgreSQL_load_geo('vzw_ookla_geo_Jan_2022', v_data,'CLIENT_LONGITUDE','CLIENT_LATITUDE')
    
    return()    

# ///////// BEGIN 


c_postgresql_locations ()                                       # AFTER INFORMAITON IS EXTRACTED FROM FUZE VIA NDL THIS FUNCITON JOINS BOTH TABLES, AND GENERATES TWO TABLES, 
                                                                # 1ST TABLE) CONTAINING FUZE PROJECTS SOME BASIC INFORMAIOTN ABOUT THE PROJECT AND THE LAT LONG INFORMATION --- NAMED: vzw_fuze_loc
                                                                # 2ND TABLE) CONTAINING PROJECT INFORMATION AND DASHBOARD INFORMATION - NAMED: vzw_fuze_qgis

# ///////// END 
