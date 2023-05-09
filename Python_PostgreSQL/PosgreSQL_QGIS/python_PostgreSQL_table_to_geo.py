

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

def q_posgresql_query (table):
    v_sql_commands = ('''
                    select * from public."%s"
                    
                    '''%table)
    return (v_sql_commands)

def c_postgresql_locations (database,table):
   
    v_databasae = database
    v_table = table
    
    cn = pg.Connection(v_databasae)
    
    v_data =cn.PostgreSQL_query_df (q_posgresql_query(table))
     
    print (v_data)    
    cn.PostgreSQL_load_append_geo(('%s_geo'%v_table), v_data,"lon","lat")
    return()       

# ///////// BEGIN 

v_database = 'vzw_fuze'
v_table = 'Root_State_HQ_Location_list'

c_postgresql_locations (v_database,v_table)                     # AFTER INFORMAITON IS EXTRACTED FROM FUZE VIA NDL THIS FUNCITON JOINS BOTH TABLES, AND GENERATES TWO TABLES, 
                                                                # 1ST TABLE) CONTAINING FUZE PROJECTS SOME BASIC INFORMAIOTN ABOUT THE PROJECT AND THE LAT LONG INFORMATION --- NAMED: vzw_fuze_loc
                                                                # 2ND TABLE) CONTAINING PROJECT INFORMATION AND DASHBOARD INFORMATION - NAMED: vzw_fuze_qgis

# ///////// END 
