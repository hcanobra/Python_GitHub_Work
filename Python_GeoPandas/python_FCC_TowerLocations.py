from numpy import dtype
from sqlalchemy import create_engine
import pandas as pd
import time 
import sys

sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_GeoPandas')

import PostgreSQL_API as pg

def c_to_sql(v_data,v_table):
    v_databasae = 'vzw_sandbox'
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                        .format(user="hcanobra",
                                pw="Tpztlan02VH",
                                db=v_databasae))
    v_data.to_sql(v_table, con = engine, if_exists = 'replace', index=False)

    return ()

def f_utah_fcc_tower_to_csv (v_data):
    v_table = 'FCC_Towers_table'
    v_file = '/Users/canobhu/Documents/GitHub/QGIS/KLM_Resources/UT_2020_Census/FCC_Files/UT_FCC_Towers.txt'

    v_DataFrame = pd.read_csv(v_file, header=None, delimiter="|")

    f_colums = v_DataFrame[0]=='CO'
    v_DataFrame = (v_DataFrame[f_colums])
    v_DataFrame =  v_DataFrame[v_DataFrame.columns[[3,6,7,8,11,12,13]]]
    v_DataFrame = v_DataFrame.astype('float64')
    v_DataFrame[3] = v_DataFrame[3].astype('int64')
    print (v_DataFrame)

    v_geo_location = pd.DataFrame(columns=("RecordId","lat","lon"))
    v_geo_location['RecordId'] = v_DataFrame[3]
    v_geo_location['lat'] = (v_DataFrame[6] + (v_DataFrame[7]/60) + (v_DataFrame[8]/3600))
    v_geo_location['lon'] = (-abs(v_DataFrame[11] + (v_DataFrame[12]/60) + (v_DataFrame[13]/3600)))

    print (v_geo_location)
    return ()

def f_fcc_location (df):
    
    f_colums_loc = df[0]=='CO'
    v_DataFrame_loc = (v_DataFrame[f_colums_loc])
    print (v_DataFrame_loc.head())

    v_DataFrame_loc =  v_DataFrame_loc[v_DataFrame_loc.columns[[3,6,7,8,11,12,13]]]
    v_DataFrame_loc = v_DataFrame_loc.astype('float64')
    v_DataFrame_loc[3] = v_DataFrame_loc[3].astype('int64')
    print (v_DataFrame_loc)

    v_geo_location = pd.DataFrame(columns=("RecordId","lat","lon"))
    v_geo_location['RecordId'] = v_DataFrame_loc[3]
    v_geo_location['lat'] = (v_DataFrame_loc[6] + (v_DataFrame_loc[7]/60) + (v_DataFrame_loc[8]/3600))
    v_geo_location['lon'] = (-abs(v_DataFrame_loc[11] + (v_DataFrame_loc[12]/60) + (v_DataFrame_loc[13]/3600)))

    return (v_geo_location)
    
def f_fcc_contact (df):
    
    f_colums_con = df[0]=='EN'
    v_DataFrame_con = (df[f_colums_con])

    v_DataFrame_con =  v_DataFrame_con[v_DataFrame_con.columns[[3,9,16]]]
    v_DataFrame_con.columns = ["RecordId","Owner","Contact"]
    
    return (v_DataFrame_con)
 
def f_fcc_detail (df):
    
    f_colums_det = df[0]=='RA'
    v_DataFrame_det = (df[f_colums_det])
    
    v_DataFrame_det =  v_DataFrame_det[v_DataFrame_det.columns[[3,23,24,25,26,27,28,29,30,31,32]]]

    v_DataFrame_det.columns = ["RecordId","Reference","City",
                               "State",
                               "County",
                               "Zip",
                               "Overall Height Above Ground w/o Appurtenances",
                               "Elevation of Site Above Mean Sea Level",
                               "Overall Height Above Ground (AGL)",
                               "Overall Height Above Mean Sea Level",
                               "Structure Type"]
    
    return (v_DataFrame_det)

def f_postgresql_locations (df, v_database, v_table):
    
    cn = pg.Connection(v_databasae)
    
    v_data =df
    cn.PostgreSQL_load_geo(('%s_geo'%v_table), v_data,"lon","lat")
    
    return()    

#// BEGINING

v_databasae = 'vzw_fuze'
v_table = 'FCC_MT_Towers_table'
v_file = '/Users/canobhu/Downloads/FCC_MT_07212022.txt'

v_DataFrame = pd.read_csv(v_file, header=None, delimiter="|")

pd1 = f_fcc_location (v_DataFrame)
pd2 = f_fcc_contact (v_DataFrame)
pd3 = f_fcc_detail (v_DataFrame)

v_DataFrame_fcc = pd1.merge(pd2, on="RecordId", how = 'inner')
v_DataFrame_fcc = v_DataFrame_fcc.merge(pd3, on="RecordId", how = 'inner')
v_DataFrame_fcc = v_DataFrame_fcc.drop_duplicates()

v_DataFrame_fcc.to_csv('/Users/canobhu/Downloads/%s.csv'%v_table, index=False)

print (v_DataFrame_fcc)

f_postgresql_locations (v_DataFrame_fcc,v_databasae,v_table)



#// END


