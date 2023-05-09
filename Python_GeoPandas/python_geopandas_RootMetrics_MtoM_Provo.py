
import os

import matplotlib.pyplot as plt
from numpy import int64
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, GeometryCollection
from sqlalchemy import null




def f_drive (df,cycle):

    df['point_start'] = gpd.GeoDataFrame(
                        geometry=gpd.points_from_xy(df['Start_Test_Longitude'],df['Start_Test_Latitude']),
                        crs = "EPSG:4326")

    df['point_end'] = gpd.GeoDataFrame(
                        geometry=gpd.points_from_xy(df['End_Test_Longitude'],df['End_Test_Latitude']),
                        crs = "EPSG:4326")

    df['line']=df.apply(lambda x: LineString([x['point_start'], x['point_end']]),axis=1)

    df['geo']=df.apply(lambda x: GeometryCollection([x['line'], x['point_start'], x['point_end']]),axis=1)


    #print(df)

    df = gpd.GeoDataFrame (df,
                        geometry=df['line'],
                        crs = "EPSG:4326")
                        
    df = df.drop(['point_start','point_end','line','geo'],1)

    df = df.to_crs('epsg:4326')

    v_cycle = (cycle.split('.'))
    
    f_file = ('/Users/canobhu/Documents/File_Resources/RootMetrics/Ogden/Ogden_RootMetrics_ShapeFiles/%s_drive_route.shp'%v_cycle[0])
    print (f_file)
    
    df.to_file(f_file)
    
def f_start_points (df,cycle):


    df['point_start'] = gpd.GeoDataFrame(
                        geometry=gpd.points_from_xy(df['Start_Test_Longitude'],df['Start_Test_Latitude']),
                        crs = "EPSG:4326")

    df['point_end'] = gpd.GeoDataFrame(
                        geometry=gpd.points_from_xy(df['End_Test_Longitude'],df['End_Test_Latitude']),
                        crs = "EPSG:4326")

    df['line']=df.apply(lambda x: LineString([x['point_start'], x['point_end']]),axis=1)

    df['geo']=df.apply(lambda x: GeometryCollection([x['line'], x['point_start'], x['point_end']]),axis=1)

    df = gpd.GeoDataFrame (df,
                        geometry=df['point_start'],
                        crs = "EPSG:4326")
                        
    df = df.drop(['point_start','point_end','line','geo'],1)

    df = df.to_crs('epsg:4326')

    v_cycle = (cycle.split('.'))
    
    f_file = ('/Users/canobhu/Documents/File_Resources/RootMetrics/Ogden/Ogden_RootMetrics_ShapeFiles/%s_start_points.shp'%v_cycle[0])
    print (f_file)
    
    df.to_file(f_file)

def f_end_points (df,cycle):

    df['point_start'] = gpd.GeoDataFrame(
                        geometry=gpd.points_from_xy(df['Start_Test_Longitude'],df['Start_Test_Latitude']),
                        crs = "EPSG:4326")

    df['point_end'] = gpd.GeoDataFrame(
                        geometry=gpd.points_from_xy(df['End_Test_Longitude'],df['End_Test_Latitude']),
                        crs = "EPSG:4326")

    df['line']=df.apply(lambda x: LineString([x['point_start'], x['point_end']]),axis=1)

    df['geo']=df.apply(lambda x: GeometryCollection([x['line'], x['point_start'], x['point_end']]),axis=1)

    df = gpd.GeoDataFrame (df,
                        geometry=df['point_end'],
                        crs = "EPSG:4326")
                        
    df = df.drop(['point_start','point_end','line','geo'],1)

    df = df.to_crs('epsg:4326')

    v_cycle = (cycle.split('.'))
    
    f_file = ('/Users/canobhu/Documents/File_Resources/RootMetrics/Ogden/Ogden_RootMetrics_ShapeFiles/%s_end_points.shp'%v_cycle[0])
    print (f_file)
    
    df.to_file(f_file)


def f_lines (df_m2m,cycle):

    df_m2m = gpd.GeoDataFrame(
                        df_m2m,
                        geometry=gpd.points_from_xy(df_m2m['Longitude'],df_m2m['Latitude']),
                        crs = "EPSG:4326")

    
    v_cycle = (cycle.split('.'))
    print (df_m2m.head())
    
    f_file = ('/Users/canobhu/Documents/File_Resources/RootMetrics/Drive_Results_Shape_Files/M2M/%s_drive_route.shp'%v_cycle[0])

    df_m2m.to_file(f_file)
    return ()


# Get the list of all files and directories
path = '/Users/canobhu/Documents/File_Resources/RootMetrics/Drive_Results_Shape_Files/Files_Detail/'
dir_list = [f for f in os.listdir(path) if f.endswith('.csv')]
 
 
for i in dir_list:   
    v_shape_files = (path+i)
    #print (v_shape_files)
    df = pd.read_csv (v_shape_files, low_memory=False)
    #print (df.head())
    
    #df['Test_Cycle_ID'] = df['Test_Cycle_ID'].astype(str)
    df['Test_Cycle_ID'] = df['Test_Cycle_ID'].astype('Int64').astype('str')
    df['idx'] =  df [['Driver-Kit','Test_Cycle_ID']].apply(lambda x : ''.join(x), axis=1)

    options = ['Mobile-to-mobile Call Originating Test Start', 'Mobile-to-mobile Call Originating Test','Mobile-to-mobile Call Originating Test End']
    #values = df[df['Task_Summary'] == 'Failure']['idx'].tolist()


    values = df[(
                (df['Test'] != null) &
                (df['Network'] == 'Verizon') &
                (
                    (df['Task_Summary'] == 'Failure') |
                    (df['Access_Summary'] == 'Failure')
                ) &
                (df['Test'].isin(options)) 
                )]['idx'].tolist()

    print ("Those are the call records with DC: ")
    print("the unique values from 1st list is",np.unique(values))
    
    df_m_to_m = df.loc[
                        (df['Network'] == 'Verizon') &
                        (df['Test'].isin(options)) &
                        (df['idx'].isin(values)) 
                        ]
    
    
    df_m_to_m['Result'] = df_m_to_m['Test_Cycle_ID']
    
    
    df_m_to_m.loc[(df_m_to_m['Access_Summary']) == 'Failure', 'Result'] = 'M2M_IA'
    df_m_to_m.loc[(df_m_to_m['Task_Summary']) == 'Failure', 'Result'] = 'M2M_DC'
    
    f_lines (df_m_to_m,i)
    

