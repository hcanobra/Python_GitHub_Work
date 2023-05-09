# importing sys
import sys
from turtle import distance
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')


import PostgreSQL_API as pg


import pandas as pd
import geopandas as gpd
import geopy.distance
from shapely.geometry import Point


from sqlalchemy import create_engine, engine


def f_postgresql_locations (v_sub_data):
    
    v_databasae = 'vzw_root_metrics'
    v_table = 'All_Data_mobile_to_Mobile_Tests_ID'
    
    cn = pg.Connection(v_databasae)
    
    v_data =v_sub_data
        
    cn.PostgreSQL_load_append_geo(('%s_geo'%v_table), v_data,"lon","lat")
    
    return()    

def q_posgresql_root_state_all ():
    v_sql_commands = ('''
        SELECT 
            "State",
            "Collection",
            "Network",
            "Access_Summary",
            "Task_Summary",
            "Call_Result",
            ST_AsX3D (geometry) AS geo,
            geometry
        FROM public.postgres_state_drive_all_mobile_to_mobile_test_geo
        WHERE ST_AsX3D (geometry) != ''
                        
                    ''')
    return (v_sql_commands)

def q_posgresql_state_traffic_all ():
    v_sql_commands = ('''
        SELECT 
            state,
			description,
			aadt,
            ST_AsX3D (central_point) AS geo,
            central_point
        FROM public.postgresql_ut_id_mt_state_traffic
        WHERE central_point IS NOT NULL
                    ''')
    return (v_sql_commands)

def f_distance_traffic_geo (p1,v_matrix,v_data_loc_ss,v_data_traffic_ss):

    
    v_aadt = v_data_traffic_ss["aadt"]
    v_sub_data = v_data_traffic_ss['geo'].str.split(" ", expand=True)
    v_sub_data = pd.concat([v_aadt,v_sub_data], axis=1)
    v_sub_data.columns = ["aadt","lon","lat"]

    for index, row in v_sub_data.iterrows():  
        p2 = v_sub_data.loc[index,'lat']+", "+v_sub_data.loc[index,'lon']
        v_dist = geopy.distance.geodesic(p1,p2)
        #v_data_traffic_ss.loc[index,'Distance'] = v_dist.miles

        if v_dist.miles < 5:
            v_matrix = v_matrix.append({
                    'State': v_data_loc_ss["State"], 
                    'Collection': v_data_loc_ss["Collection"], 
                    'Network': v_data_loc_ss["Network"], 
                    'Call_Result': v_data_loc_ss["Call_Result"], 
                    'aadt': f"{row['aadt']}", 
                    'Distance': v_dist.miles, 
                    'geo': v_data_loc_ss["geo"]
                    }, ignore_index=True)
    
 
    if v_matrix.empty:
        pass
    else:
        v_aadt = v_matrix[["State","Collection","Network","Call_Result","aadt","Distance"]]
        v_sub_geo = v_matrix['geo'].str.split(" ", expand=True)
        v_sub_geo.columns = ["lon","lat"]
        v_sub_data = pd.concat([v_aadt,v_sub_geo], axis=1)
        
        print (v_sub_data)
        #f_postgresql_locations(v_sub_data)
    

    

    return()

def q_posgresql_query ():
    v_sql_commands = ('''
                    SELECT 
                    *,
                    ST_AsX3D (point) AS geo
                    FROM public.escalations_locations
                    where  point is not null
                    ''')
    return (v_sql_commands)

def q_posgresql_root_state_vzw_query ():
    v_text = "ROOT_STATE_P%"
    v_sql_commands = ('''
                        SELECT 
                            LIST.priority,
                            LIST.idx_id,
                            LOC.pdx_id,
                            ST_AsX3D (LOC.point) AS geo
                        FROM public.escalations_locations LOC
                        JOIN public.postgresql_locations_list LIST ON LOC.pdx_id = LIST.pdx_id
                        ORDER BY LIST.idx_id
                        
                    ''')
    return (v_sql_commands)

def q_posgresql_fuze_location_query ():
    v_sql_commands = ('''
                        SELECT 
                            "Projects_Fuze_project_id",
                            "Projects_parent_solution_id",
                            ST_AsX3D (geometry) AS geo
                        FROM public.vzw_fuze_qgis
                    ''')
    return (v_sql_commands)

def c_postgresql_query_table (v_databasae,v_query):

    
    cn = pg.Connection(v_databasae)
    
    v_data =cn.PostgreSQL_query_df (v_query)
            
    
    return(v_data)    

def f_distance_geo (p1,v_data):
    
    v_sub_data = v_data['geo'].str.split(" ", expand=True)
    v_sub_data.columns = ["lon","lat"]
    #print (v_sub_data)

    for index, row in v_sub_data.iterrows():  
        p2 = v_sub_data.loc[index,'lat']+", "+v_sub_data.loc[index,'lon']
        v_dist = geopy.distance.geodesic(p1,p2)
        v_data.loc[index,'Distance'] = v_dist.miles
    return(v_data)

def f_lat_lon_format (v_data):
    v_sub_data = v_data['geo'].str.split(" ", expand=True)
    v_sub_data.columns = ["lon","lat"]
    #print (v_sub_data)
    return (v_sub_data)

def f_fuze ():
    v_databasae = 'vzw_fuze'
    #v_table = 'vzw_truecall'



    v_query = q_posgresql_root_state_vzw_query()
    v_data_loc = c_postgresql_query_table (v_databasae,v_query)             # AFTER INFORMAITON IS EXTRACTED FROM FUZE VIA NDL THIS FUNCITON JOINS BOTH TABLES, AND GENERATES TWO TABLES,        
    v_data_loc_ss = v_data_loc[v_data_loc['priority'] == 'ROOT_STATE_P%']   # CREATE A SUBSET WITH JUS TTHE ROOT METRICS POINTS

    v_data_loc_ss = v_data_loc_ss.head()
    print (v_data_loc_ss)


    v_query = q_posgresql_fuze_location_query()
    v_data_fuze = c_postgresql_query_table (v_databasae,v_query)            # AFTER INFORMAITON IS EXTRACTED FROM FUZE VIA NDL THIS FUNCITON JOINS BOTH TABLES, AND GENERATES TWO TABLES, 
    #print (v_data_fuze.head())

    v_matrix = {'pdx_id': [], 'Fuze_Proj': []}

    for index, row in v_data_loc_ss.iterrows():
        #print (v_data_loc_ss.loc[index,"pdx_id"])
        v_matrix["pdx_id"].append(v_data_loc_ss.loc[index,"pdx_id"])
        v_matrix["Fuze_Proj"].append(v_data_loc_ss.loc[index,"pdx_id"])

        v_data_loc_ss_geo1 = f_lat_lon_format (v_data_loc_ss)
        p1 = v_data_loc_ss_geo1.loc[index,'lat']+", "+v_data_loc_ss_geo1.loc[index,'lon']
        print (p1)

        v_data_distance = f_distance_geo (p1,v_data_fuze)
        v_data_distance = v_data_distance[v_data_distance['Distance'] < 5]   # GIVES ME THE RECORDS BELOW 10 MILES
        print (v_data_distance.head())
        

    v_matrix = pd.DataFrame (v_matrix)
    print (v_matrix)
    '''
    for index, row in v_data_loc_ss.iterrows():
        v_data_loc_ss_geo1 = f_lat_lon_format (v_data_loc_ss)
        p1 = v_data_loc_ss_geo1.loc[index,'lat']+", "+v_data_loc_ss_geo1.loc[index,'lon']
        print (p1)

        v_data_distance = f_distance_geo (p1,v_data_fuze)
        v_data_distance = v_data_distance[v_data_distance['Distance'] < 10]   # GIVES ME THE RECORDS BELOW 10 MILES
        print (v_data_distance.head())
    '''
    
    return()

def f_vehicle_count ():
    v_databasae = 'vzw_root_metrics'
    v_query = q_posgresql_root_state_all()
    v_data_loc_all = c_postgresql_query_table (v_databasae,v_query)             # AFTER INFORMAITON IS EXTRACTED FROM FUZE VIA NDL THIS FUNCITON JOINS BOTH TABLES, AND GENERATES TWO TABLES,        
    v_data_loc_ut = v_data_loc_all[v_data_loc_all['State'] == 'Utah']   # CREATE A SUBSET WITH JUS TTHE ROOT METRICS POINTS
    v_data_loc_MT = v_data_loc_all[v_data_loc_all['State'] == 'Montana']   # CREATE A SUBSET WITH JUS TTHE ROOT METRICS POINTS
    v_data_loc_ID = v_data_loc_all[v_data_loc_all['State'] == 'Idaho']   # CREATE A SUBSET WITH JUS TTHE ROOT METRICS POINTS
    
    #v_data_loc_ss = v_data_loc_ut
    #v_data_loc_ss = v_data_loc_MT
    v_data_loc_ss = v_data_loc_ID

    print (v_data_loc_ss)

    v_databasae = 'vzw_fuze'
    v_query = q_posgresql_state_traffic_all()
    v_data_traffic_all = c_postgresql_query_table (v_databasae,v_query)            # AFTER INFORMAITON IS EXTRACTED FROM FUZE VIA NDL THIS FUNCITON JOINS BOTH TABLES, AND GENERATES TWO TABLES, 
    v_data_traffic_ut = v_data_traffic_all[v_data_traffic_all['state'] == 'Utah']   # CREATE A SUBSET WITH JUS TTHE ROOT METRICS POINTS
    v_data_traffic_MT = v_data_traffic_all[v_data_traffic_all['state'] == 'Montana']   # CREATE A SUBSET WITH JUS TTHE ROOT METRICS POINTS
    v_data_traffic_ID = v_data_traffic_all[v_data_traffic_all['state'] == 'Idaho']   # CREATE A SUBSET WITH JUS TTHE ROOT METRICS POINTS


    #v_data_traffic_ss = v_data_traffic_ut
    #v_data_traffic_ss = v_data_traffic_MT
    v_data_traffic_ss = v_data_traffic_ID
    
    print (v_data_traffic_ss)

    v_matrix = pd.DataFrame(columns=['State','Collection','Network','Call_Result','aadt','Distance','geo'])

    for index, row in v_data_loc_ss.iterrows():
        v_data_loc_ss_geo1 = f_lat_lon_format (v_data_loc_ss)
        p1 = v_data_loc_ss_geo1.loc[index,'lat']+", "+v_data_loc_ss_geo1.loc[index,'lon']
        print (p1)

        f_distance_traffic_geo (p1,v_matrix,v_data_loc_ss.loc[index],v_data_traffic_ss)   
        
    print (v_matrix)
        
    return()

# ///////// BEGIN 

#f_fuze ()

f_vehicle_count()

# ///////// END 

