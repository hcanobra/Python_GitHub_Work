


# importing sys
import sys
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')


from cmath import asin
import geopandas as gp
import contextily as cx
from shapely.geometry import Point, Polygon, MultiPolygon

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

import PostgreSQL_API as pg

def q_posgresql_sp_polygon (v_table):
    v_sql_commands = ('''
                       select 
                            "SPE_Name",
                            geom
                            
                       from public."%s"
               
                    '''%v_table)
    return (v_sql_commands)

def c_postgresql_polygon ():
    
    v_databasae = 'geo_db'
    v_table = 'SPE_Polygon'
    
    engine = create_engine(f'postgresql://postgres:Tpztlan02VH@localhost:5432/{v_databasae}')
    
    queried_gdf = gp.read_postgis(q_posgresql_sp_polygon(v_table), engine, geom_col='geom',crs=4326)
    queried_gdf = queried_gdf.explode()
    
    return(queried_gdf) 

def f_sites_df (v_url):
        
    df = pd.read_csv(v_url, on_bad_lines='skip')

    gdf = gp.GeoDataFrame(
        df, geometry=gp.points_from_xy(df["Longitude(DecDeg)"], df["Latitude(DecDeg)"]))
    
    gdf = gdf.set_crs('EPSG:4326')
    
    return (gdf)

def f_sites_ver0 ():
    
    v_url = ["http://datapro.eng.vzwcorp.com/download/sites_files/saltlake_cellver_0000.csv.gz",
             "http://datapro.eng.vzwcorp.com/download/sites_files/boise_cellver_0000.csv.gz",
             "http://datapro.eng.vzwcorp.com/download/sites_files/montana_cellver_0000.csv.gz"]
             
    v_gdf_all = gp.GeoDataFrame()
    for element in v_url:
        gdf = f_sites_df (element)
    
        gdf = gdf.loc[
                (gdf['CBSC_ECP_BSC'] == 10) | 
                (gdf['CBSC_ECP_BSC'] == 210) |
                (gdf['CBSC_ECP_BSC'] == 310) |
                (gdf['CBSC_ECP_BSC'] == 11) | 
                (gdf['CBSC_ECP_BSC'] == 211) |
                (gdf['CBSC_ECP_BSC'] == 311) |
                (gdf['CBSC_ECP_BSC'] == 12) | 
                (gdf['CBSC_ECP_BSC'] == 212) |
                (gdf['CBSC_ECP_BSC'] == 312) |
                (gdf['CBSC_ECP_BSC'] == 13) | 
                (gdf['CBSC_ECP_BSC'] == 213) |
                (gdf['CBSC_ECP_BSC'] == 313)
                ]
        
        gdf = gdf [['BTS.','Site','Latitude(DecDeg)','Longitude(DecDeg)','Site Name','geometry']]
        gdf = gdf.drop_duplicates()
        
        v_gdf_all = pd.concat([v_gdf_all,gdf])
    
    print (v_gdf_all)
        
    return (v_gdf_all)

def f_sites_plt (gdf):
    
    
    ax = gdf.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
    cx.add_basemap(ax, crs=gdf.crs)

    return()

def f_sp_assigment (v_plygon,v_points):

    v_gdf_final = gp.GeoDataFrame()

    for element in v_plygon['SPE_Name']:
        
        v_sp_data = v_plygon.loc[v_plygon['SPE_Name'] == element]
        
        poly = v_sp_data.iloc[0,1]
        
        v_sp_sites = v_points.loc[v_points['geometry'].within(poly) == True]
        v_sp_sites['SP_Eng'] = v_sp_data.iloc[0,0]
        print (v_sp_sites)
        
        v_gdf_final = pd.concat([v_gdf_final,v_sp_sites])

    v_gdf_final.to_csv ('/Users/canobhu/Downloads/SP_eng.csv',index=False)

    return (v_gdf_final)
    
# BEGINING
v_plygon = c_postgresql_polygon ()

v_points = f_sites_ver0 ()

v_sites_all = f_sp_assigment (v_plygon,v_points)

f_sites_plt (v_sites_all)

# END


