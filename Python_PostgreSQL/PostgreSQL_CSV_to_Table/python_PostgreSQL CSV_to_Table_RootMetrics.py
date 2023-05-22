'''
Thhis script imports a .csv file into PostgreSQL
on a table named UT2_2021, this table will be used 
later in Excell to plot some data.
pwd
'''


# importing sys
import sys
  
# adding Folder_2 to the system path
sys.path.append('/storage/emulated/0/Documents/Pydroid3/site-packages')

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

v_database = 'vzw_root_metrics'
v_directory = '/Users/canobhu/Documents/File_Resources/RootMetrics/SLC/SaltLakeCity_UT2022_2H/'
v_table = 'SaltLakeCity_UT_2022_2H_All_Mobile_to_Mobile_Tests'


v_data = f_read_csv_fromfile(v_directory,v_table)

cn = pg.Connection(v_database)
cn.PostgreSQL_load_df (v_table,v_data)


# ///////// END 


# // From PostgreSQL

