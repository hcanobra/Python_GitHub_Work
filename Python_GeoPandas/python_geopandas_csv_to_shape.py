
import os

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, GeometryCollection



def f_shape_file (df,v_lat_field,v_long_field,v_file):

    df = gpd.GeoDataFrame (df,
                        geometry=gpd.points_from_xy(df[v_long_field],df[v_lat_field]),
                        crs = "EPSG:4326")
    
    
    f_file = ('/Users/canobhu/Documents/GitHub/QGIS/KLM_Resources/Kyles_list/ShapeFiles/%s.shp'%v_file)


    #df = df.to_crs('epsg:4326')

    print (df)
        
    df.to_file(f_file)
    
   


# Get the list of all files and directories
v_directory = '/Users/canobhu/Documents/GitHub/QGIS/KLM_Resources/Root_State_Clusters_Mar2022_Original/Root_State_Clusters_Mar2022_v4/'
v_file = 'Root_State_Clusters_Mar2022_v4'
v_lat_field = 'cluster_la'
v_long_field = 'cluster_lo'

v_directory_file = v_directory+v_file+'.csv'


v_df = pd.read_csv (v_directory_file)

f_shape_file (v_df,v_lat_field,v_long_field,v_file)
