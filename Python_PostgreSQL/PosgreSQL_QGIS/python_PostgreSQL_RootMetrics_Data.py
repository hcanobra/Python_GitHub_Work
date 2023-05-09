

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

def q_posgresql_rootmetrics_query (v_table):
    v_sql_commands = ('''
                        select *
                        from public."%s"
                        where "Data_Direction" = 'Download' 
               
                    '''%v_table)
    return (v_sql_commands)


def c_postgresql_locations ():
    
    v_databasae = 'vzw_root_metrics'
    v_table = 'Boise_ID_2022_2H_All_Data_Throughput_Tests'
    
    cn = pg.Connection(v_databasae)
    
    v_data =cn.PostgreSQL_query_df (q_posgresql_rootmetrics_query(v_table))
        
    cn.PostgreSQL_load_geo(('%s_geo'%v_table), v_data,"Start_Test_Longitude","Start_Test_Latitude")
    
    return()    


# ///////// BEGIN 



c_postgresql_locations ()                                       # AFTER INFORMAITON IS EXTRACTED FROM FUZE VIA NDL THIS FUNCITON JOINS BOTH TABLES, AND GENERATES TWO TABLES, 
                                                                # 1ST TABLE) CONTAINING FUZE PROJECTS SOME BASIC INFORMAIOTN ABOUT THE PROJECT AND THE LAT LONG INFORMATION --- NAMED: vzw_fuze_loc
                                                                # 2ND TABLE) CONTAINING PROJECT INFORMATION AND DASHBOARD INFORMATION - NAMED: vzw_fuze_qgis


#f_postgresql_locations_linestring()



# ///////// END 


