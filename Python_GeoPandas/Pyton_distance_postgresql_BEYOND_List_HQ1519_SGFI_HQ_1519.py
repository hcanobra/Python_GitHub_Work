# importing sys
import sys
from turtle import distance
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_GeoPandas')

import PostgreSQL_API as pg
import Python_geopandas_distance as gpdc


import pandas as pd
import geopandas as gpd
import geopy.distance
from shapely.geometry import Point


from sqlalchemy import create_engine, engine


def c_postgresql_query_table (v_databasae,v_query):  
    cn = pg.Connection(v_databasae)  
    v_data =cn.PostgreSQL_query_df (v_query)
            
    return(v_data)    

def f_postgresql_locations (v_sub_data):
    
    v_databasae = 'vzw_fuze'
    v_table = 'postgresql_BEYOND_List_HQ1519'
    
    cn = pg.Connection(v_databasae)
    
    v_data =v_sub_data


    cn.PostgreSQL_load_geo(('%s_geo'%v_table), v_data,"lon","lat")
    return()    

def q_posgresql_target_query ():
    v_sql_commands = ('''

                    SELECT 
                        ESC.idx_id,
                        ESC.pdx_id,
                        ESC.priority,
                        ESC."Fuze",
                        ESC."KID",
                        ESC."KID_Rank",
                        ESC."SP_Eng",
                        ESC."Description",
                        ESC."Comments",
                        ESC."Fuze_Status",
                        ESC."Location",
                        RIGHT ((ST_AsX3D (LOC.point)),(LENGTH((ST_AsX3D (LOC.point))) - POSITION(' '  IN (ST_AsX3D (LOC.point))))) AS lat,
                        LEFT((ST_AsX3D (LOC.point)),(POSITION(' '  IN (ST_AsX3D (LOC.point)))-1)) AS lon

                    FROM public.postgresql_locations_list ESC
                    JOIN public.escalations_locations LOC ON ESC.pdx_id = LOC.pdx_id
                    WHERE priority = 'BEYOND'
                    ORDER BY ESC."SP_Eng", ESC.idx_id,ESC.pdx_id
                    
                    ''')
    return (v_sql_commands)

def q_posgresql_source_query ():
    v_sql_commands = ('''        

                        SELECT 
                        "Cluster Record" :: TEXT as id,
                            'HQ_Sunil' as "Source",
                            lat,
                            lon
                        FROM public."MTNPLNS_2022_HQ_1519_LOCATIONS_geo"
                    ''')
    return (v_sql_commands)

def f_main (v_databasae,v_query):
    
    query = v_query
    databasae = v_databasae
    
    v_records = c_postgresql_query_table (databasae,query)
    
    print (v_records)
    
    return(v_records)

def f_closest_df (v_target,v_source):
    # FINAL DATAFRAME
    v_final = pd.DataFrame()

    for index, row in v_target.iterrows(): 
        
        v_lat = row['lat']
        v_lon = row['lon']
        v_df = v_source
        v_closest_value = gpdc.f_closest(v_lat,v_lon,v_df)
        
        v_closest_value = v_closest_value.drop(labels = ['lat'])
        v_closest_value = v_closest_value.drop(labels = ['lon'])
        v_final = v_final.append(v_target.iloc[index].append(v_closest_value),ignore_index=True)


    return (v_final)
# ///////// BEGIN 

'''
1) Definition of parameters
'''

v_target_query = ['vzw_fuze',q_posgresql_target_query()]
v_source_query = ['vzw_fuze',q_posgresql_source_query()]

# TARGET
v_databasae = v_target_query[0]
v_query = v_target_query[1]
v_target = f_main(v_databasae,v_query)
v_target = pd.DataFrame(v_target)
v_target_df_colums = v_target.columns


# SOURCE : SGFI , LEASE , CROWN.
v_databasae = v_source_query[0]
v_query = v_source_query[1]
v_source = f_main(v_databasae,v_query)
v_source = pd.DataFrame(v_source)


# Cal.
v_final = f_closest_df (v_target,v_source)

f_postgresql_locations (v_final)


# ///////// END 

