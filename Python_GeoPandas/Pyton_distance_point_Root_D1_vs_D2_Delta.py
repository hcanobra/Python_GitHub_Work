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

def f_postgresql_table_creation_locations (v_databasae,v_table,v_sub_data):
    
    cn = pg.Connection(v_databasae)
    
    v_data =v_sub_data

    cn.PostgreSQL_load_geo(('%s_geo'%v_table), v_data,"lon","lat")
    return()    

def q_posgresql_target_query ():
    v_sql_commands = ('''
                        select 
                            "Collection" as "Collection_target",
                            "Network" as "Network_target",
                            "Driver-Kit" as "Driver-Kit_target",
                            "Activity" as "Activity_target",
                            "UTC_Time" as "UTC_Time_target",
                            "Test_Cycle_ID" as "Test_Cycle_ID_target",
                            "Device_ID" as "Device_ID_target",
                            "Data_Direction" as "Data_Direction_target",
                            "Task_Summary" as "Task_Summary_target",
                            "Task_Speed_Median" as "Task_Speed_Median_target",
                            "Start_Test_Latitude" as "Start_Test_Latitude_target",
                            "Start_Test_Longitude" as "Start_Test_Longitude_target",
                            "End_Test_Latitude" as lat,
                            "End_Test_Longitude" as lon,
                            "Average_LTE_RSRP" as "Average_LTE_RSRP_target",
                            "Min_LTE_RSRP" as "Min_LTE_RSRP_target",
                            "Max_LTE_RSRP" as "Max_LTE_RSRP_target",
                            "Average_LTE_RSRQ" as "Average_LTE_RSRQ_target",
                            "Average_LTE_RSSNR" as "Average_LTE_RSSNR_target",
                            "Average_5G_SS_RSRP" as "Average_5G_SS_RSRP_target",
                            "Average_5G_SS_RSRQ" as "Average_5G_SS_RSRQ_target",
                            "Average_5G_SS_RSSNR" as "Average_5G_SS_RSSNR_target",
                            "Average_LTE_Bandwidth" as "Average_LTE_Bandwidth_target",
                            "Average_NR_BW" as "Average_NR_BW_target",
                            "Data_Delivery_Successes_%%" as "Data_Delivery_Successes_%%_target",
                            "Final_Test_Speed" as "Final_Test_Speed_target",
                            "Network_Types" as "Network_Types_target",
                            "Network_Category" as "Network_Category_target",
                            "geometry" as "geometry_target"
                        from public."Provo_UT_2022_2H_All_Data_Throughput_Tests_geo"
                        where "Data_Direction" = 'Download' 
                        and "Network" = 'Verizon'
                        and "Activity" = 'Drive'                        
                    ''')
    return (v_sql_commands)

def q_posgresql_source_query ():
    v_sql_commands = ('''        
                    
                        select 
                            "Collection" as "Collection_source",
                            "Network" as "Network_source",
                            "Driver-Kit" as "Driver-Kit_source",
                            "Activity" as "Activity_source",
                            "UTC_Time" as "UTC_Time_source",
                            "Test_Cycle_ID" as "Test_Cycle_ID_source",
                            "Device_ID" as "Device_ID_source",
                            "Data_Direction" as "Data_Direction_source",
                            "Task_Summary" as "Task_Summary_source",
                            "Task_Speed_Median" as "Task_Speed_Median_source",
                            "Start_Test_Latitude" as "Start_Test_Latitude_source",
                            "Start_Test_Longitude" as "Start_Test_Longitude_source",
                            "End_Test_Latitude" as lat,
                            "End_Test_Longitude" as lon,
                            "Average_LTE_RSRP" as "Average_LTE_RSRP_source",
                            "Min_LTE_RSRP" as "Min_LTE_RSRP_source",
                            "Max_LTE_RSRP" as "Max_LTE_RSRP_source",
                            "Average_LTE_RSRQ" as "Average_LTE_RSRQ_source",
                            "Average_LTE_RSSNR" as "Average_LTE_RSSNR_source",
                            "Average_5G_SS_RSRP" as "Average_5G_SS_RSRP_source",
                            "Average_5G_SS_RSRQ" as "Average_5G_SS_RSRQ_source",
                            "Average_5G_SS_RSSNR" as "Average_5G_SS_RSSNR_source",
                            "Average_LTE_Bandwidth" as "Average_LTE_Bandwidth_source",
                            "Average_NR_BW" as "Average_NR_BW_source",
                            "Data_Delivery_Successes_%%" as "Data_Delivery_Successes_%%_source",
                            "Final_Test_Speed" as "Final_Test_Speed_source",
                            "Network_Types" as "Network_Types_source",
                            "Network_Category" as "Network_Category_source",
                            "geometry" as "geometry_source"
                        from public."Provo_UT_2022_1H_All_Data_Throughput_Tests_geo"
                        where "Data_Direction" = 'Download' 
                        and "Network" = 'Verizon'                        
                        and "Activity" = 'Drive'
                    ''')
    return (v_sql_commands)

def f_main (v_databasae,v_query):
    
    query = v_query
    databasae = v_databasae
    
    v_records = c_postgresql_query_table (databasae,query)
    
    #print (v_records)
    
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

    
    v_final['Delta_Thrp'] = v_final['Final_Test_Speed_source'] - v_final['Final_Test_Speed_target']

    return (v_final)
# ///////// BEGIN 

'''
1) Definition of parameters
'''

v_target_query = ['vzw_root_metrics',q_posgresql_target_query()]
v_source_query = ['vzw_root_metrics',q_posgresql_source_query()]

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



# Calculations ...
v_final = f_closest_df (v_target,v_source)

# Build table with calculation data
v_databasae = 'vzw_root_metrics'
v_table = 'postgresql_Provo_H1_to_Provo_H2'

print (v_final)
f_postgresql_table_creation_locations (v_databasae,v_table,v_final)


# ///////// END 

