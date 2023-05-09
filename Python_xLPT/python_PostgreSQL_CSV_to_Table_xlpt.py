'''
Thhis script imports a .csv file into PostgreSQL
on a table named UT2_2021, this table will be used 
later in Excell to plot some data.

'''


# importing sys
import sys
  
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')

from numpy import isnan
import numpy as np
import ndl_API as ndl
import PostgreSQL_API as pg
import pandas as pd
import geopandas as gp

from sqlalchemy import create_engine, engine


def f_read_csv_fromfile (v_directory,v_table):
    
    v_file =  ("%s%s.csv" %(v_directory,v_table))
    v_sheet = pd.read_csv (v_file)
    print (v_sheet)
    return (v_sheet)


# ///////// BEGIN 

v_database = 'vzw_xlpt'
v_directory = '/Users/canobhu/Downloads/xLPT_tmp/'
v_table = 'DMPL_4G_XLPT_KPI_WEBSERVICES'


v_data = f_read_csv_fromfile(v_directory,v_table)

cn = pg.Connection(v_database)
cn.PostgreSQL_load_df (v_table,v_data)

# ///////// END 


# // From PostgreSQL
