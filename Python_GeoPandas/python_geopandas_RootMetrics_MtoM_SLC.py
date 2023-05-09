
import os

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, GeometryCollection



def f_drive (df,cycle):
    #df = pd.read_csv('/Users/canobhu/Documents/File_Resources/RootMetrics/SLC/SaltLakeCity_MtoM/SaltLakeCity_UT_2022_1H_All_Mobile_to_Mobile_Tests.csv')

    #print (df.info())

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
    
    f_file = ('/Users/canobhu/Documents/File_Resources/RootMetrics/SLC/SaltLakeCity_RootMetrics_ShapeFiles/%s_drive_route.shp'%v_cycle[0])
    print (f_file)
    
    df.to_file(f_file)
    
def f_start_points (df,cycle):
    #df = pd.read_csv('/Users/canobhu/Documents/File_Resources/RootMetrics/SLC/SaltLakeCity_MtoM/SaltLakeCity_UT_2022_1H_All_Mobile_to_Mobile_Tests.csv')

    #print (df.info())

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
    
    f_file = ('/Users/canobhu/Documents/File_Resources/RootMetrics/SLC/SaltLakeCity_RootMetrics_ShapeFiles/%s_start_points.shp'%v_cycle[0])
    print (f_file)
    
    df.to_file(f_file)

def f_end_points (df,cycle):
    #df = pd.read_csv('/Users/canobhu/Documents/File_Resources/RootMetrics/SLC/SaltLakeCity_MtoM/SaltLakeCity_UT_2022_1H_All_Mobile_to_Mobile_Tests.csv')

    #print (df.info())

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
    
    f_file = ('/Users/canobhu/Documents/File_Resources/RootMetrics/SLC/SaltLakeCity_RootMetrics_ShapeFiles/%s_end_points.shp'%v_cycle[0])
    print (f_file)
    
    df.to_file(f_file)

# Get the list of all files and directories
path = '/Users/canobhu/Documents/File_Resources/RootMetrics/SLC/SaltLakeCity_MtoM/'
dir_list = [f for f in os.listdir(path) if f.endswith('.csv')]
 
#GENERATE THE DRIVE DATA
v_files = []
for i in dir_list:   
    v_shape_files = ('/Users/canobhu/Documents/File_Resources/RootMetrics/SLC/SaltLakeCity_MtoM/%s'%i)
    df = pd.read_csv (v_shape_files)
    f_drive(df,i)
    

#GENERATE THE START POINT DATA
v_files = []
for i in dir_list:   
    v_shape_files = ('/Users/canobhu/Documents/File_Resources/RootMetrics/SLC/SaltLakeCity_MtoM/%s'%i)
    df = pd.read_csv (v_shape_files)
    f_start_points (df,i)
    
#GENERATE THE END POINT DATA
v_files = []
for i in dir_list:   
    v_shape_files = ('/Users/canobhu/Documents/File_Resources/RootMetrics/SLC/SaltLakeCity_MtoM/%s'%i)
    df = pd.read_csv (v_shape_files)
    f_end_points (df,i)