# importing sys
import sys
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')


import PostgreSQL_API as pg

from sqlalchemy import create_engine, engine

def q_posgresql_query ():
    v_sql_commands = ('''
                    SELECT 
                    *,
                    ST_AsText(point) AS geo
                    FROM public.escalations_locations
                    ''')
    return (v_sql_commands)

def c_postgresql_query_table (v_databasae):

    
    cn = pg.Connection(v_databasae)
    
    v_data =cn.PostgreSQL_query_df (q_posgresql_query())
            
    print (v_data)    
    
    return()    


# ///////// BEGIN 

v_databasae = 'vzw_fuze'
#v_table = 'vzw_truecall'

c_postgresql_query_table (v_databasae)                                       # AFTER INFORMAITON IS EXTRACTED FROM FUZE VIA NDL THIS FUNCITON JOINS BOTH TABLES, AND GENERATES TWO TABLES, 
                                                                # 1ST TABLE) CONTAINING FUZE PROJECTS SOME BASIC INFORMAIOTN ABOUT THE PROJECT AND THE LAT LONG INFORMATION --- NAMED: vzw_fuze_loc
                                                                # 2ND TABLE) CONTAINING PROJECT INFORMATION AND DASHBOARD INFORMATION - NAMED: vzw_fuze_qgis

# ///////// END 
