from numpy import dtype
from sqlalchemy import create_engine
import pandas as pd
import time 


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

def f_dtaframe_clean (v_file):
    print (v_file)
    v_DataFrame =  pd.read_csv (v_file, header=None, delimiter="|")

    v_geo_location = pd.DataFrame(columns=("RecordId","lat","lon"))
    v_geo_record = []


    v_DataFrame.drop(v_DataFrame.columns[[0,1,2,4,5,9,10,14,15,16,17]],axis=1, inplace= True)

    print (v_DataFrame[3])
    v_geo_location['RecordId'] = v_DataFrame[3]
    v_geo_location['lat'] = (v_DataFrame[6] + (v_DataFrame[7]/60) + (v_DataFrame[8]/3600))
    v_geo_location['lon'] = (-abs(v_DataFrame[11] + (v_DataFrame[12]/60) + (v_DataFrame[13]/3600)))
    print (v_geo_location)


    return(v_geo_location)

def r_tower (v_table):
    v_file = '/Users/canobhu/Documents/GitHub/QGIS/KLM_Resources/UT_2020_Census/FCC_Files/locations.txt'
    v_geo_location = f_dtaframe_clean(v_file)
    c_to_sql (v_geo_location,v_table)
    f_fcc_tower_to_csv (v_geo_location)
    return()

def d_tower (v_table):
    v_file = '/Users/canobhu/Documents/GitHub/QGIS/KLM_Resources/UT_2020_Census/FCC_Files/d_tower/CO.dat'
    v_geo_location = f_dtaframe_clean(v_file)
    c_to_sql (v_geo_location,v_table)
    f_fcc_tower_to_csv (v_geo_location)
    return()

def a_tower (v_table):
    v_file = '/Users/canobhu/Documents/GitHub/QGIS/KLM_Resources/UT_2020_Census/FCC_Files/a_tower/CO.dat'
    v_geo_location = f_dtaframe_clean(v_file)
    c_to_sql (v_geo_location,v_table)
    f_fcc_tower_to_csv (v_geo_location)
    return()
    
#// BEGINING

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




#// END


