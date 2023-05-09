#!/usr/bin/env python3.7

# importing sys
import sys
  
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')

import sys
import mysql.connector
import time
from numpy import NaN
import pandas as pd
import datetime
import PostgreSQL_API as pg


def f_postgressql_table (v_database,v_table,v_data):
    
    cn = pg.Connection(v_database)
    cn.PostgreSQL_load_append_df (v_table,v_data)

def f_files(v_url):
    
    url = v_url

    v_page = pd.read_html(url)
     
    v_page =  v_page[0]                                                             # Breacks down the DF and selects the fields needed
    v_page = v_page[~v_page['Last modified'].isnull()]                              # Remove Nan
    v_page = v_page[v_page['Name'].str.contains('RadioConfigs')]                    # Subfilter the DF just for the filenes which match 'RadioConfig'
    v_page[['Date','Time']] = v_page['Last modified'].str.split(' ', expand=True)   # Splits the column 'Last modified' by space
    v_page = v_page[['Name','Date']]                                                # Selects just colums needed
    #print (v_page)
    
    return (v_page)

def f_import_csv_to_postgresql (v_database,v_table,v_files,v_url): # This funciton imports a CSV File to MySQL

    for  index, row in v_files.iterrows():
        url = v_url+row['Name']
        v_date = row['Date']
        
        data = pd.read_csv(url) 
        data.insert(0, 'Date',v_date)
    
        #print (data.head())

        v_data = data[[
                        'Date',
                        'MKT',
                        'ENB',
                        'NAME',
                        'EUtranCell',
                        'administrativeState',
                        'operationalState'
                    ]]
        v_data['Date'] = pd.to_datetime(v_data["Date"]).dt.date     # Fromanting field Date as date in Pandas
 
        
        #v_data =  v_data[(v_data['administrativeState'] == 'UNLOCKED') & (v_data['operationalState'] == 'DISABLED')]       # Subfilter the DF just for the filenes which match 'RadioConfig'
        v_data =  v_data[(v_data['operationalState'] == 'DISABLED')]                                                        # Subfilter the DF just for the filenes which match 'RadioConfig'
        
        v_data.set_index('MKT')
        v_data.columns = v_data.columns.str.rstrip()    # This commnad removes white space at the end of string: https://stackoverflow.com/questions/41476150/removing-space-from-dataframe-columns-in-pandas/41476181
    
        f_postgressql_table (v_database,v_table,v_data)

        
    print ('Tables completed....!!!!')

    return ()

def f_PostgreSQL_Query():
    v_query = ("""
                    SELECT 
                        "MKT",
                        "NAME",
                        "ENB",
                        "EUtranCell",
                        "administrativeState",
                        "operationalState",
                        count("EUtranCell") as "Appearance",
                        CURRENT_DATE AS DAY_PULLED
                        
                    FROM public."WJ_EricssonRadioConfigs"

                    WHERE "EUtranCell" IN
                        (
                            SELECT 
                                "EUtranCell"
                            FROM public."WJ_EricssonRadioConfigs"
                            WHERE "Date" = '"2022-04-05"'
                                AND
                                "administrativeState" in ('UNLOCKED','LOCKED')
                                AND
                                "operationalState" = 'DISABLED'
                            GROUP BY "EUtranCell"
                        )
                        AND
                        "administrativeState" in ('UNLOCKED','LOCKED')
                        AND
                        "operationalState" = 'DISABLED'
                        AND
                        "MKT" IN (10,11,12,13)
                        AND
                        "Date" BETWEEN (CURRENT_DATE - INTERVAL '30 day') AND CURRENT_DATE

                    GROUP BY 
                        "EUtranCell",
                        "MKT",
                        "NAME",
                        "ENB",
                        "administrativeState",
                        "operationalState"

                    ORDER BY count("EUtranCell") DESC
                """)
    return(v_query)    

def f_Postgres_Point_DataFrame(v_database):
    cn = pg.Connection(v_database)
    
    v_data =cn.PostgreSQL_query_df (f_PostgreSQL_Query())
            
    print (v_data)    
    

    return(v_data)


# // BEGIN

v_database = "vzw_db"
v_table  = "WJ_EricssonRadioConfigs"
v_url = 'http://txslmdatapa1v/TrendingFiles/Top10reports/VSONstuff/archive/'



#v_files = f_files (v_url)
#f_import_csv_to_postgresql (v_database,v_table,v_files,v_url)

v_data= f_Postgres_Point_DataFrame(v_database)


#// END

