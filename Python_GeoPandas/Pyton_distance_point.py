# importing sys
import sys
from turtle import distance
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_GeoPandas')

import PostgreSQL_API as pg
import Python_geopandas_distance as gpd


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
    v_table = 'hq_Sunil_vs_SGFI'
    
    cn = pg.Connection(v_databasae)
    
    v_data =v_sub_data
        
    cn.PostgreSQL_load_geo(('%s_geo'%v_table), v_data,"lon","lat")
    return()    

def f_distance_geo (p1,source):
    
    v_list = {'Distance' : [],'id' : [], 'Source' : []}
    v_record = []

    
    for index, row in source.iterrows():  
        p2 = str(row['lat'])+","+str(row['lon'])
        v_dist = geopy.distance.geodesic(p1,p2)

        v_list['Distance'].append(v_dist.miles)
        v_list['id'].append(row['id'])
        v_list['Source'].append(row['Source'])

    v_list= pd.DataFrame(v_list)
    v_closest= v_list.sort_values(by = 'Distance',inplace=False)

    return(v_closest.iloc[0])

def q_posgresql_target_query ():
    v_sql_commands = ('''
                        select 
                            "Cluster Record",	
                            lat,			
                            lon,
                            "State",
                            "Root Priority Rank",
                            "Root Priority Percentile"
                        from public."MTNPLNS_State_Root_SunilStateRoot_geo"
                        where "State" IN ('Utah','Idaho','Montana','Wyoming')	
                    ''')
    return (v_sql_commands)

def q_posgresql_source_query ():
    v_sql_commands = ('''
                        select 
							"Combine Names" as id,
							'SGFI_list' as "Source",
							lat,
							lon
                        from public."Coverage_model_SPT_OPT_Jul2020_and_Jan2021_geo"
                        where "State" IN ('UT','ID','MT','WY')
                    ''')
    return (v_sql_commands)

def f_main (v_databasae,v_query):
    
    query = v_query
    databasae = v_databasae
    
    v_records = c_postgresql_query_table (databasae,query)
    
    print (v_records)
    
    return(v_records)

# ///////// BEGIN 

'''
1) Definition of parameters

'''

v_target_query = ['vzw_fuze',q_posgresql_target_query()]
v_source_query = ['vzw_fuze',q_posgresql_source_query()]

# TARGET : main table to comapre agains HQ_ROOT
v_databasae = v_target_query[0]
v_query = v_target_query[1]
v_target = f_main(v_databasae,v_query)
v_target = pd.DataFrame(v_target)
v_target_df_colums = v_target.columns

# SOURCE : table to comapre SGFI, Complains, ETC.
v_databasae = v_source_query[0]
v_query = v_source_query[1]
v_source = f_main(v_databasae,v_query)
v_source = pd.DataFrame(v_source)

# FINAL DATAFRAME
v_final = pd.DataFrame()

for index, row in v_target.iterrows(): 
    p1 = str(row['lat'])+","+str(row['lon'])
    v_closest_value = f_distance_geo (p1,v_source)
    #v_target.iloc[index].append(v_closest_value)
    v_final = v_final.append(v_target.iloc[index].append(v_closest_value),ignore_index=True)


print (v_final)
f_postgresql_locations (v_final)



# ///////// END 

