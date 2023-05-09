'''
This script imports a CSV file into PosgreSQL and create a point using SQL commands

The location of the files is defined on : c_QGIS_add_point()

'''


from numpy import append, int64, nan, integer
from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
import random

def f_PostgreSQL_open ():
  
    engine = create_engine("postgresql+psycopg2://postgres:Tpztlan02VH@localhost/geo_db")
    conn = engine.connect()

    return(conn)

def f_PostgreSQL_close (conn):
    conn.close()
    return ()

def f_PostgreSQL_Point_Query():
    v_query = ("""
                SELECT * FROM point
                """)
    return(v_query)

def f_QGIS_Point_query (v_geo_id,v_redord_id,v_Name,v_Description,v_Latitude,v_Longitude):

    v_query = ("""
    INSERT INTO point (
					geo_id,
					record_id,
					Name, 
					Description, 
					point) 
			VALUES (
					%s,
					'%s',
					'%s',
					'%s',
					ST_SetSRID(ST_MakePoint(%s, %s), 
					4326))
                """%(v_geo_id,v_redord_id,v_Name,v_Description,v_Longitude,v_Latitude))
    return(v_query)

def f_Postgres_Point_DataFrame(v_query,v_conn):

    v_query = v_conn.execute(v_query)

    v_table = v_query.fetchall()

    v_column_names = v_query.keys()

    v_data = pd.DataFrame(data=v_table)

    v_data.columns = v_column_names

    print (v_data)
    return(v_data)

def c_PostgreSQL_insert(v_query,v_conn):

    v_query = v_conn.execute(v_query)

    return(v_query)

def c_PosgreSQL_Point_Query():

    v_conn = f_PostgreSQL_open()  # Initiate server connection
    v_query = f_PostgreSQL_Point_Query()
    v_data= f_Postgres_Point_DataFrame(v_query,v_conn)

    f_PostgreSQL_close(v_conn)  # Close server connetion

    return(v_data)

def c_QGIS_add_point():

    v_geo_id = 0

    v_conn = f_PostgreSQL_open()  # Initiate server connection

    v_file = pd.read_csv('/Users/canobhu/Downloads/SP_PROJECT_NOTES_SP_Location_LIST.csv')

    for records in v_file.index:
        v_record = v_file.iloc[records]
        v_geo_id = v_geo_id + 1
        v_redord_id = v_record[0]
        v_Name = v_record[1]
        v_Description = v_record[2] 
        v_Latitude = v_record[3]
        v_Longitude = v_record[4]
        v_query = f_QGIS_Point_query (v_geo_id,v_redord_id,v_Name,v_Description,v_Latitude,v_Longitude)
        c_PostgreSQL_insert(v_query,v_conn)

    
    
    (v_conn)  # Close server connetion

    #print (v_file)


    return()

# Begining

c_QGIS_add_point ()
v_query = c_PosgreSQL_Point_Query()
print (v_query)

# End





