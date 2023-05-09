# Python 3.8.2
# Date: 10.27.2021
# Author: Hugo Cano

'''
T
'''

# IMPORT LIBRARIES 
from sqlalchemy import create_engine
#from sqlalchemy import text
from getpass import getpass
import pandas as pd

import geopandas as gp
from shapely.geometry import Point, LineString, shape


from geoalchemy2 import Geometry, WKTElement
from shapely.geometry import Point


# static helper methods
class Connection:

    # Setup the connection. Username and password optional. If not supplied, will be asked for later on
    def __init__(self,v_databasae):

        self.engine = create_engine("postgresql+psycopg2://canobhu:Tpztlan02VH@10.136.233.31/%s"%v_databasae)


    # Execute query
    def PostgreSQL_Create_Table(self, query):
        print('Processing MySQL Query Creating Table... ', query)

        v_result = self.engine.execute(query)   # Execute the query, calls itself to open the Engine
        
        return ()
    
    # Execute query
    def PostgreSQL_query_df(self, query):
        print('Processing MySQL Query... yes ', query)

        v_result = self.engine.execute(query)   # Execute the query, calls itself to open the Engine
        df = pd.DataFrame(v_result)             # Convert the result into DataFrame

        df.columns = v_result.keys()            # Add column names to the DataFrame
        return (df)

    def PostgreSQL_load_df(self,v_table,v_data):
        #v_data = pd.DataFrame(v_data)
        v_data.to_sql(v_table, con = self.engine, if_exists = 'replace', index=False)

    def PostgreSQL_load_append_df(self,v_table,v_data):
        #v_data = pd.DataFrame(v_data)
        v_data.to_sql(v_table, con = self.engine, if_exists = 'append', index=False)
        
    def PostgreSQL_load_geo(self,v_table,v_data,v_long,v_lat):
        print('Creating geo locations... ')

        df = pd.DataFrame(v_data)
        gdf = gp.GeoDataFrame(v_data, geometry=gp.points_from_xy(df[v_long],df[v_lat]))
        gdf.crs = "EPSG:4326"
        gdf = gp.GeoDataFrame(gdf)
    
        gdf.to_postgis(v_table, con = self.engine, if_exists = 'replace', index=False, dtype={'geometry': Geometry(geometry_type='POINT', srid= 4326)})

    def PostgreSQL_load_append_geo(self,v_table,v_data,v_long,v_lat):
        print('Creating geo locations... ')

        df = pd.DataFrame(v_data)
        gdf = gp.GeoDataFrame(v_data, geometry=gp.points_from_xy(df[v_long],df[v_lat]))
        gdf.crs = "EPSG:4326"
        gdf = gp.GeoDataFrame(gdf)
            
        gdf.to_postgis(v_table, con = self.engine, if_exists = 'append', index=False, dtype={'geometry': Geometry(geometry_type='POINT', srid= 4326)})

    def PostgreSQL_load_line_geo(self,v_table,v_data,v_long,v_lat):
        print('Creating geo locations... ')

        df = pd.DataFrame(v_data)
        
        #print (df)

        #gdf = gp.GeoDataFrame(v_data, geometry=gp.points_from_xy(df[v_long],df[v_lat]))
        #gdf.crs = "EPSG:4326"
    
        #zip the coordinates into a point object and convert to a GeoData Frame
        geometry = [Point(xy) for xy in zip(df.Longitude, df.Latitude)]
        geo_df = gp.GeoDataFrame(df, geometry=geometry)

        geo_df2 = geo_df.groupby(['Test_Cycle_ID', 'Device_ID'])['geometry'].apply(lambda x:LineString(x.tolist()))
        #geo_df2 = gp.GeoDataFrame(geo_df2, geometry='geometry')

        #print (df)
        print (geo_df2)

        geo_df2 = gp.GeoDataFrame(geo_df2)
        geo_df2.crs = "EPSG:4326"
        geo_df2.to_postgis(v_table, con = self.engine, if_exists = 'replace', index=False, dtype={'geometry': Geometry(geometry_type='LINESTRING', srid= 4326)})
      
    def  PostgreSQL_close(self):
        self.engine.close()                     # Close the connection to the Engine