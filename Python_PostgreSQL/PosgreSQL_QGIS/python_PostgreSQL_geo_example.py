
from shapely import geometry
import PostgreSQL_API as pg
import pandas as pd
import geopandas as gp
from geoalchemy2 import Geometry, WKTElement
from shapely.geometry import Point


from sqlalchemy import create_engine, engine



def f_PostgreSQL_open ():
  
    engine = create_engine("postgresql+psycopg2://postgres:Tpztlan02VH@localhost/vzw_Fuze")
    conn = engine.connect()

    return(conn)

def f_PostgreSQL_close (conn):
    conn.close()
    return ()

def q_posgresql_query ():
    v_sql_commands = ('''
    
                        SELECT * 
                        FROM public."vzw_Fuze_Proj"

                    ''')
    return (v_sql_commands)

def c_Query ():
        
    v_conn = f_PostgreSQL_open()
    
    print (q_posgresql_query())
    v_data = v_conn.execute(q_posgresql_query)
    
    print (v_data)
    
    f_PostgreSQL_close (v_conn)
    
    return ()

# ///////// BEGIN 

v_databasae = 'vzw_Fuze'
conn = pg.Connection('vzw_Fuze')

v_data = conn.PostgreSQL_query_df(q_posgresql_query())

conn.PostgreSQL_load_geo('vzw_fuze_loc', v_data,'Projects_atoll_site_longitude','Projects_atoll_site_latitude')



conn.close()
'''
v_databasae = 'vzw_Fuze'
conn = engine.create_engine("postgresql+psycopg2://postgres:Tpztlan02VH@localhost/%s"%v_databasae)
v_data = conn.execute(q_posgresql_query())
df = pd.DataFrame(v_data)
df.columns = v_data.keys()

df['geometry'] = gp.GeoDataFrame(v_data, geometry=gp.points_from_xy(df.Projects_atoll_site_longitude,df.Projects_atoll_site_latitude))


df = gp.GeoDataFrame(df)

print (df)

df.to_postgis('vzw_fuze_loc', con = conn, if_exists = 'replace', index=False, dtype={'geometry': Geometry(geometry_type='POINT', srid= 4326)})

'''