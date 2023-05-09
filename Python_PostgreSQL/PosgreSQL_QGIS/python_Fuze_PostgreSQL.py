"""


c_to_sql
    v_data
    v_table

c_sql_to_csv
    v_query

c_postgresql_locations
    v_data

q_NDL_Fuze_Dash_Query

q_NDL_Fuze_PROJ_Query

q_NDL_Query_Sample

q_sql_SGFI_Query

c_Fuzee_Table_updates

c_Cband_sql_to_csv


"""

# importing sys
import sys
  
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')

import ndl_API as ndl
import PostgreSQL_API as pg
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text


def c_to_sql(v_data,v_table):
    v_databasae = 'vzw_sandbox'
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                        .format(user="hcanobra",
                                pw="Tpztlan02VH",
                                db=v_databasae))
    v_data.to_sql(v_table, con = engine, if_exists = 'replace', index=False)

    return ()

def c_sql_to_csv (v_query):
    v_databasae = 'vzw_sandbox'
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                        .format(user="hcanobra",
                                pw="Tpztlan02VH",
                                db=v_databasae))
    
    v_columns = engine.execute(v_query).keys() # Obtains the column names from the DB
    v_data = engine.execute (v_query) # Execure the Query on the DB
    
    v_data = pd.DataFrame(data=v_data) # Transform the result of the query into Pandas DataFrame 

    v_data.columns = v_columns # Add colum names to DataFrame

    return (v_data)

def c_postgresql_locations (v_data):
    v_databasae = 'vzw_fuze'

    conn = pg.Connection('vzw_fuze')
    
    #v_data = conn.PostgreSQL_query_df(q_posgresql_Fuze_query())
    conn.PostgreSQL_load_geo('vzw_fuze_loc', v_data,'Projects_atoll_site_longitude','Projects_atoll_site_latitude')

    return()

def q_NDL_Fuze_Dash_Query ():
    v_sql_commands = ('''
    
    SELECT *
    FROM  fuze_presto_views.dmp_rfds_sp_fuze_dash_view 

                    ''')
    return (v_sql_commands)

def q_NDL_Fuze_PROJ_Query ():
    v_sql_commands = ('''

    SELECT *
    FROM  fuze_presto_views.dmp_rfds_sp_fuze_projects_view

                    ''')
    return (v_sql_commands)

def q_NDL_Query_Sample ():
    v_sql_commands = ('''


        SELECT 
            *
            FROM fuze_presto_views.dmp_rfds_sp_cband_ready
            
        UNION


        SELECT 
            *
            FROM fuze_presto_views.dmp_rfds_sp_cband_forecast
            
                    ''')
    return (v_sql_commands)

def c_NDL_Query_Sample ():
    cn = ndl.Connection()
    
    v_data = cn.commands(q_NDL_Query_Sample)
    print (v_data.head())

    return ()

def q_sql_SGFI_Query ():
    v_sql_commands = ('''

    select *
    from vzw_sandbox.Fuze_Proj pr
    join vzw_sandbox.Fuze_dash ds on pr.Projects_Fuze_project_id = ds.Dashboar_Fuze_project_id
    where Projects_pl_rationale like ("%Ga
                    ''')
    return (v_sql_commands)

def c_Fuzee_Table_updates ():
    cn = ndl.Connection()

    v_table = 'Fuze_Proj'
    v_data = cn.commands(q_NDL_Fuze_PROJ_Query())
    
    #c_to_sql(v_data,v_table)


    v_table = 'Fuze_Dash'
    v_data = cn.commands(q_NDL_Fuze_Dash_Query())
    
    #c_to_sql(v_data,v_table)

    cn.close

    return()

def c_Cband_sql_to_csv ():
    v_data = c_sql_to_csv(q_sql_CbandActivation_Query())  # Generates csv file from a query defined on a sub function
    f_CbandActivation_to_csv (v_data)
    v_data = c_sql_to_csv(q_sql_CbandReady_Query())  # Generates csv file from a query defined on a sub function
    f_CbandReady_to_csv (v_data)
    v_data = c_sql_to_csv(q_sql_CbandForecast_Query())  # Generates csv file from a query defined on a sub function
    f_CbandForecast_to_csv (v_data)
    v_data = c_sql_to_csv(q_sql_Cband2021_Query())  # Generates csv file from a query defined on a sub function
    f_Cband2021_to_csv (v_data)

    return()

# // Begining

c_Fuzee_Table_updates()

#c_NDL_Query_Sample ()

# // End