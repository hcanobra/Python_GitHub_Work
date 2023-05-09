"""

This Script executes a query on NDL, pulling the informaotin from ATOLL and eLPT
related to all the sites part of UT2.

Then the result is loaded in PostgreSQL locally on a table/database

Functions:

    q_NDL_Query_Sample : Contain the Query commands to execute

    f_PostgreSQL_open : This Funtion open the connection to PostgreSQL server

    f_PostgreSQL_close : This function closes the connection to PostgreSQL server 
        conn : Import the connection already opened

    f_postgreSQL_inport : This funciton import the data to PostgresSQL, the following infromation has to be given
        v_data : The dataframe that will be loaded in PostgreSQL
        v_table : The target table on PostgreSQL.
        v_conn : The oppen connetion to the PostgreSQL server.

    c_NDL_Query_Sample : Main class which funtion is to call all classes functions and queries.

"""

# importing sys
import sys
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')

import ndl_API as ndl
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text


def f_PostgreSQL_open ():
  
    engine = create_engine("postgresql+psycopg2://postgres:Tpztlan02VH@localhost/vzw_atoll")
    conn = engine.connect()

    return(conn)

def f_PostgreSQL_close (conn):
    conn.close()
    return ()

def f_postgreSQL_inport (v_data, v_table, v_conn):
    
    v_data.to_sql(v_table, con = v_conn, if_exists = 'replace', index=False)
    return()

def q_NDL_Query_Sample ():
    v_sql_commands = ('''
                    SELECT 
                        DISTINCT(lpt.enodeb) AS elpt_enodeb,
                        lpt.site AS elpt_site_name,
                        lpt.latitude_degrees_nad83 AS elpt_latitude_degrees_nad83,
                        lpt.longitude_degrees_nad83 AS elpt_longitude_degrees_nad83,
                        
                        atoll.state AS atoll_state,
                        atoll.county AS atoll_county,
                        atoll.site_custom_field_03 AS atoll_rsa,
                        atoll.site_on_air_date AS atoll_site_on_air_date,
                        atoll.peoplesoft_location_code AS atoll_peoplesoft_location_code,
                        atoll.fuze_site_id AS atoll_fuze_site_id

                        
                    FROM vzatoll.f_vzatoll_lte_v4 atoll
                    JOIN elpt.ericssonenbgeographicinfo lpt on atoll.peoplesoft_location_code = lpt.peoplesoft_location_code

                    WHERE 
                        atoll.site_custom_field_03 = 'UT2'
                        AND
                        atoll.gnb_enb_cell_name != ''
                        AND
                        atoll.gnb_enb_site_name != ''
            
                    ''')
    return (v_sql_commands)

def c_NDL_Query_Sample ():
    cn = ndl.Connection()
    
    v_data = cn.commands(q_NDL_Query_Sample)
    
    v_conn = f_PostgreSQL_open()
    
    f_postgreSQL_inport (v_data, 'vzw_atoll_ut2', v_conn)
    
    f_PostgreSQL_close (v_conn)
    
    print (v_data.head())

    cn.close
    
    return ()

# // Begining

c_NDL_Query_Sample ()

# // End
