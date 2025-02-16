'''
This version of the script uses the report on xLPT named DMPL_4G_XLPT_KPI_WEBSERVICES

'''
#!/usr/bin/env python3

import sys
from npe import ws
import pandas as pd
from datetime import date
import datetime


import pandas as pd

# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')
sys.path.append('/Users/canobhu/Library/Python/3.8/lib/python/site-packages')


import PostgreSQL_API as pg


def c_xlpt ():
    print ("################################################################################")
    print ("################################################################################")
    print ('###',pd.Timestamp.now())
    print ("### 1) Extracting data from xLPT ....")
    
    # Month abbreviation, day and year	
    today = date.today()
    d4 = today.strftime("%b_%d_%Y")
    
    df = ws.xlpt('ericsson', 'canobhu', 'DMPL_4G_XLPT_KPI_WEBSERVICES')
    
    print ('### %s : Importing xLPT Report'%d4)
    print (df.head())
    
    Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
    d1 = Previous_Date.strftime("%m/%d/%Y")   
    df['DAY'] = d1
    
    df = df[df.HR != '*']
    df.columns= df.columns.str.replace('%','_pct',regex=True)
    
    df = pd.DataFrame(df)
    df.to_csv('/Users/canobhu/Downloads/xLPT_tmp/DMPL_4G_XLPT_KPI_WEBSERVICES_%s.csv'%d4, index=False)
    
    print ('###',pd.Timestamp.now())
    print ("################################################################################")
    print ("################################################################################")
    
    return (df)

def c_csv():
    v_file = '/Users/canobhu/Downloads/xLPT_tmp/DMPL_4G_XLPT_KPI_WEBSERVICES.csv'
    df = pd.read_csv (v_file)

    df = df[df.HR != '*']
    df.columns= df.columns.str.replace('%','_pct',regex=True)
    print (df)
    
    return (df)

def c_postgresql_bulk(df):
    import psycopg2
    from psycopg2.extras import execute_values
    from psycopg2 import sql

    con = psycopg2.connect(
                        database="vzw_xlpt",
                        user='postgres',
                        password='Tpztlan02VH',
                        host='127.0.0.1',
                        port='5432'
                        )
    
    
    cur = con.cursor()

    print ("################################################################################")
    print ("################################################################################")
    print ('###',pd.Timestamp.now())
    print ("### Inserting values in PostgreSQL table: ")

    
    #df = df.head()
    
    v_colums = df.columns.tolist()
    columns = sql.SQL(',').join(map(sql.Identifier, v_colums))
    #print (columns)
    
    
    data_dict = df.to_dict('records')
    #print (data_dict)

    v_values = v_colums
    values = sql.SQL(',').join(map(sql.Placeholder, v_values))
    
    # Since you are using a dict you need to provide a template for 
    # execute_values
    values_template = sql.SQL('(') + values + sql.SQL(')')

    #print(values_template.as_string(con))


    insert_sql = sql.SQL("INSERT INTO {} ({}) VALUES %s").format(sql.Identifier("DMPL_4G_XLPT_KPI_WEBSERVICES"), columns)

    #print(insert_sql.as_string(con))
    
    execute_values(cur, insert_sql, data_dict, template=values_template)
    
    con.commit()
    con.close()
    
    
    print ('###',pd.Timestamp.now())
    print ("################################################################################")
    print ("################################################################################")
    
    return()

    #print (columns)
#/Begin


v_df = c_xlpt ()
#v_df = c_csv ()

c_postgresql_bulk(v_df)


#/End







