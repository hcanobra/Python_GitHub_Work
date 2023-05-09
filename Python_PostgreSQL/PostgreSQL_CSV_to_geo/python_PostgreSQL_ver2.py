
def c_using_psycop2 ():

    import psycopg2

    # Connect to an existing database
    conn = psycopg2.connect("dbname=postgres user=postgres password=Tpztlan02VH")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")


    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no more SQL injections!)
    cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))

    # Query the database and obtain data as Python objects
    cur.execute("SELECT * FROM test;")
    cur.fetchone()
    (1, 100, "abc'def")

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()


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

def f_QGIS_Point_query (v_geo_id,v_redord_id,v_Name,v_Description,v_SP_Eng,v_Status,v_Latitude,v_Longitude):

    v_query = ("""
    INSERT INTO point (
					geo_id,
					record_id,
					Name, 
					Description, 
                    sp_eng,
                    status,
					point) 
			VALUES (
					%s,
					'%s',
					'%s',
					'%s',
					'%s',
					'%s',
					ST_SetSRID(ST_MakePoint(%s, %s), 
					4326))
                """%(v_geo_id,v_redord_id,v_Name,v_Description,v_SP_Eng,v_Status,v_Longitude,v_Latitude))
    return(v_query)

def f_Postgres_Point_DataFrame(v_query,v_conn):

    v_query = v_conn.execute(v_query)

    v_table = v_query.fetchall()

    v_column_names = v_query.keys()

    v_data = pd.DataFrame(data=v_table)

    v_data.columns = v_column_names

    return(v_data)

def c_PostgreSQL_Query(v_query):
    v_conn = f_PostgreSQL_open ()

    v_query = v_conn.execute(v_query)

    v_table = v_query.fetchall()

    v_column_names = v_query.keys()

    v_data = pd.DataFrame(data=v_table)

    v_data.columns = v_column_names

    print (v_data)
    f_PostgreSQL_close (v_conn)
    return ()

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
        v_SP_Eng = v_record[3]
        v_Status = v_record[4]

        v_Latitude = v_record[5]
        v_Longitude = v_record[6]
        v_query = f_QGIS_Point_query (v_geo_id,v_redord_id,v_Name,v_Description,v_SP_Eng,v_Status,v_Latitude,v_Longitude)
        c_PostgreSQL_insert(v_query,v_conn)

    f_PostgreSQL_close(v_conn)  # Close server connetion

    #print (v_file)


    return()

# Begining

### Query Table Points
'''
v_query = f_PostgreSQL_Point_Query()
c_PostgreSQL_Query(v_query)
'''


c_QGIS_add_point ()
#v_query = c_PosgreSQL_Point_Query()
#print (v_query)

# End





'''
Construction completed that are not construction completed. 
- Projects they get push so hard, GC is not double checking / they need to validate that it Construction needs to validate 
that GC is delivering acordance to the design.

DT Tooele is a hob site, they are two sites probably 3 on a 1G link.

Construction complete actual
Ready for integration

- Integration hand off, eSNAP, what will be the deliverable timepline from the IB perspective.


'''