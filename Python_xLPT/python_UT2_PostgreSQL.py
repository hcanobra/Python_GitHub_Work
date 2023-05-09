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


def f_read_csv_fromfile ():
    
    #v_sheet = pd.read_csv ('/Users/canobhu/Documents/UT2_EVDO_Day.csv' )
    v_sheet = pd.read_csv ('/Users/canobhu/Downloads/data-1640627680430.csv')
    print (v_sheet)
    return (v_sheet)



# ///////// BEGIN 

v_data = f_read_csv_fromfile()
v_table = 'UT2_LTE_2021'
cn = pg.Connection('vzw_xlpt')
cn.PostgreSQL_load_df (v_table,v_data)


# ///////// END 


# // From PostgreSQL
'''
SELECT 
	TO_DATE ("MONTH", 'MM/D/YY') AS "Date",
	"RRC_Setup_Failure%" AS "RRC_Setup_Pct",
	"Bearer_Drop%" AS "Bearer_Drop_Pct",
	"Downlink_Throughput_in_Mbps" AS "Downlink_Throughput_Mbps",
	"Downlink_Data_Volume_MB_Test" AS "Downlink_Data_Volume_MB",
	"Downlink_Data_Volume_MB_Test"/30 AS "AVG_Downlink_Data_Volume_MB"
FROM public."UT2_2021"
ORDER BY TO_DATE ("MONTH", 'MM/D/YY')


SELECT 
	TO_DATE ("MONTH", 'MM/D/YY') AS "Date",
	"VoLTE_SC_IA%" AS "VoLTE_SC_IA_Pct",
	"VoLTE_IA%" AS "VoLTE_IA_Pct",
	"Adjusted_SIP_SC_DC%" AS "Adjusted_SIP_SC_DC_Pct",
	"SIP_Total_MOU" AS "VoLTE_MOU",
	"SIP_Total_MOU"/30 AS "Avg_VoLTE_MOU"
	
FROM public."UT2_2021"
ORDER BY TO_DATE ("MONTH", 'MM/D/YY')

'''
