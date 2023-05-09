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


def c_postgresql_query_table (v_databasae,v_query):

    
    cn = pg.Connection(v_databasae)
    
    v_data =cn.PostgreSQL_query_df (v_query)
            
    
    return(v_data)    

def f_postgresql_locations (v_sub_data):
    
    v_databasae = 'vzw_fuze'
    v_table = 'escalation_location_fuze_pid'
    
    cn = pg.Connection(v_databasae)
    
    v_data =v_sub_data
        
    cn.PostgreSQL_load_append_geo(('%s_geo'%v_table), v_data,"lon","lat")
    return()    

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

def q_posgresql_location_query ():
    v_sql_commands = ('''
                    SELECT
                        ESC.idx_id,
                        ESC.pdx_id,
                        ESC."priority",
                        ESC."SP_Eng",
                        ESC. "priority",
                        ESC."Comments",
                        ST_AsX3D (point) AS geo,
                        point
                    FROM escalations_locations LOC
                    JOIN postgresql_locations_list ESC ON LOC.pdx_id = ESC.pdx_id
                    WHERE ESC.priority IN ('ROOT_STATE_P1','L3_P1')

                    ''')
    return (v_sql_commands)

def q_posgresql_fuze_query ():
    v_sql_commands = ('''
                    SELECT 
                        "Projects_Fuze_project_id",
                        "Projects_parent_solution_id",
                        "Projects_local_market",
                        "Projects_Site_name",
                        "Projects_Status",
                        ST_AsX3D (geometry) AS geo,
                        geometry
                    FROM public.vzw_fuze_qgis
                    WHERE 
                        "Projects_Status" != 'Completed'
                        AND
                        "Projects_Status" != 'Fuze_Reject'
                    ''')
    return (v_sql_commands)

def f_fuze_distance_geo (p1,v_matrix,v_data_loc_ss,v_data_fize_ss):
    
    v_data_fize_sss = v_data_fize_ss[[
                                    'Projects_Fuze_project_id',
                                    'Projects_parent_solution_id'
                                    ]]
    
    v_sub_data = v_data_fize_ss['geo'].str.split(" ", expand=True)
    v_sub_data = pd.concat([v_data_fize_sss,v_sub_data], axis=1)
    v_sub_data.columns = [
                            'Projects_Fuze_project_id',
                            'Projects_parent_solution_id',
                            'lon','lat'
                            ]

    for index, row in v_sub_data.iterrows():  
        p2 = v_sub_data.loc[index,'lat']+", "+v_sub_data.loc[index,'lon']
        v_dist = geopy.distance.geodesic(p1,p2)

        
        if v_dist.miles < 2:
            v_matrix = v_matrix.append({
                                    'idx_id': v_data_loc_ss["idx_id"],
                                    'pdx_id': v_data_loc_ss["pdx_id"],
                                    'Projects_Fuze_project_id': f"{row['Projects_Fuze_project_id']}",
                                    'Projects_parent_solution_id': f"{row['Projects_parent_solution_id']}",
                                    'Distance': v_dist.miles,
                                    'lat': f"{row['lat']}",
                                    'lon' : f"{row['lon']}",
                                    'geo': v_data_loc_ss["geo"]
                                    }, ignore_index=True)

    if v_matrix.empty:
        pass
    else:
        v_matrix = pd.DataFrame(v_matrix)
        
        v_colums = v_matrix.columns
        v_sub_geo = v_matrix['geo'].str.split(" ", expand=True)
        

        v_sub_geo.columns = ["lon","lat"]
        

        v_aadt = v_matrix[[
                            "idx_id","pdx_id","Projects_Fuze_project_id","Projects_parent_solution_id","Distance"
                            ]]
        v_sub_geo = v_matrix['geo'].str.split(" ", expand=True)
        v_sub_geo.columns = ["lon","lat"]
        v_sub_data = pd.concat([v_aadt,v_sub_geo], axis=1)

        f_postgresql_locations(v_sub_data)

    return()

def f_target_loations_geo ()

def f_fuze ():
    v_databasae = 'vzw_fuze'
    
    v_query = q_posgresql_fuze_query()
    v_data_fuze_all = c_postgresql_query_table (v_databasae,v_query)
    
    v_data_fuze_ss = v_data_fuze_all
    print (v_data_fuze_ss)



    '''
    v_query = q_posgresql_location_query()
    v_data_loc_all = c_postgresql_query_table (v_databasae,v_query)
    
    v_data_loc_ss = v_data_loc_all
    print (v_data_loc_ss)

    v_matrix = pd.DataFrame(columns=['idx_id' ,
                                    'pdx_id',
                                    'priority' ,
                                    'Projects_Fuze_project_id',
                                    'Projects_parent_solution_id',
                                    'Distance', 
                                    'lat',
                                    'lon',
                                    'geo',
                                    ])

    for index, row in v_data_loc_ss.iterrows():
        v_data_loc_ss_geo1 = f_lat_lon_format (v_data_loc_ss)
        p1 = v_data_loc_ss_geo1.loc[index,'lat']+", "+v_data_loc_ss_geo1.loc[index,'lon']


        f_fuze_distance_geo (p1,v_matrix,v_data_loc_ss.loc[index],v_data_fuze_ss)   
        
    print (v_matrix)
    '''

    
    return(v_data_fuze_ss)

# ///////// BEGIN 

v_fuze_df = f_fuze()
v_target_locations = 

# ///////// END 

