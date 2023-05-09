"""


f_PostgreSQL_open

f_PostgreSQL_close
    conn

f_postgreSQL_inport 
    v_data
    v_table
    v_conn

c_sql_to_csv
    v_query

q_NDL_Fuze_PROJ_Query

q_NDL_Fuze_Dash_Query

c_NDL_Query
    v_query
    v_table

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
  
    engine = create_engine("postgresql+psycopg2://postgres:Tpztlan02VH@localhost/vzw_fuze")
    conn = engine.connect()

    return(conn)

def f_PostgreSQL_close (conn):
    conn.close()
    return ()

def f_postgreSQL_inport (v_data, v_table, v_conn):
    
    v_data.to_sql(v_table, con = v_conn, if_exists = 'replace', index=False)
    return()

def q_NDL_Fuze_PROJ_Query ():
    v_sql_commands = ('''
                        SELECT
                        *
                        FROM  fuze_presto_views.dmp_rfds_sp_fuze_projects_view

                    ''')
    return (v_sql_commands)

def q_NDL_Fuze_Dash_Query ():
    v_sql_commands = ('''
    
                        SELECT *
                        FROM  fuze_presto_views.dmp_rfds_sp_fuze_dash_view 

                    ''')
    return (v_sql_commands)


def q_NDL_Fuze_Dates_Query ():
    v_sql_commands = ('''
    
                        SELECT *
                        FROM  fuze_presto_views.dmp_rfds_sp_fuze_dates_view

                    ''')
    return (v_sql_commands)
    
def c_NDL_Query (v_query,v_table):
    cn = ndl.Connection()
    
    v_data = cn.commands(v_query)
    print (v_data.head())

    
    v_conn = f_PostgreSQL_open()
    
    f_postgreSQL_inport (v_data, v_table, v_conn)
    
    f_PostgreSQL_close (v_conn)
    

    cn.close
    
    return ()


def c_main ():
    c_NDL_Query (q_NDL_Fuze_PROJ_Query(),'vzw_fuze_proj')

    c_NDL_Query (q_NDL_Fuze_Dash_Query(),'vzw_fuze_dash')

    c_NDL_Query (q_NDL_Fuze_Dates_Query(),'vzw_fuze_dates')  
    return()
# // Begining




# // End
