'''
PVS_14_v3_aial_<state_FIPS>.shp - AIAL–AmericanIndianAreaLegal 
PVS_14_v3_aias_<state_FIPS>.shp -AIAS-AmericanIndianReservationState 
PVS_14_v3_aitsl_<state_FIPS>.shp - AITSL -AmericanIndianTribal Subdivision Legal 
PVS_14_v3_aitss_<state_FIPS>.shp -AITSS-AmericanIndianTribalStatisticalState 
PVS_14_v3_cbsa_<state_FIPS>.shp - CBSA - Core Based Statistical Area 
PVS_14_v3_cd_<state_FIPS>.shp - CD - Congressional District 
PVS_14_v3_cdp_<state_FIPS>.shp - CDP - Census Designated Place 
PVS_14_v3_county_<state_FIPS>.shp - COUNTY - County Boundary 
PVS_14_v3_elsd_<state_FIPS>.shp - ELSD - Elementary school districts 
PVS_14_v3_mcd_<state_FIPS>.shp - MCD - Minor Civil Division 
PVS_14_v3_necta_<state_FIPS>.shp - NECTA - New England City and Town Area 
PVS_14_v3_place_<state_FIPS>.shp - PLACE – Incorporated Place 
PVS_14_v3_puma_<state_FIPS>.shp - PUMA - Public Use Microdata Area 
PVS_14_v3_scsd_<state_FIPS>.shp - SCSD – Secondary School District 
PVS_14_v3_sldl_<state_FIPS>.shp - SLDL - State Legislative District Lower 
PVS_14_v3_sldu_<state_FIPS>.shp -SLDU–StateLegislativeDistrictUpper 
PVS_14_v3_state_<state_FIPS>.shp - STATE - State Boundaries 
PVS_14_v3_tbg_<state_FIPS>.shp - TBG - Tribal Block Group 
PVS_14_v3_tct_<state_FIPS>.shp - TCT - Tribal Census Tract 
PVS_14_v3_tracts_<state_FIPS>.shp - TRACTS - Census Tract 
PVS_14_v3_uac_<state_FIPS>.shp - UAC - Urban Area Census 
PVS_14_v3_unsd_<state_FIPS>.shp - UNSD - Unified School District
'''

from operator import contains
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import time    

from shapely.geometry import Point
import pyproj
from shapely.ops import transform


def f_aial ():
    '''
    PVS_14_v3_aial_<state_FIPS>.shp - AIAL–AmericanIndianAreaLegal 
    '''
    df = gpd.read_file('/Users/canobhu/Downloads/USA_2020_Census/Uath/pvs_batch_from_49/partnership_shapefiles_21v2_49049/PVS_21_v2_aial_49049.shp')
    
    return()

def f_aias ():
    '''
    PVS_14_v3_aias_<state_FIPS>.shp -AIAS-AmericanIndianReservationState 
    '''
    return()

def f_aitsl():
    '''
    PVS_14_v3_aitsl_<state_FIPS>.shp - AITSL -AmericanIndianTribal Subdivision Legal 
    '''
    return()

def f_aitss ():
    '''
    PVS_14_v3_aitss_<state_FIPS>.shp -AITSS-AmericanIndianTribalStatisticalState 
    '''
    return()

def f_cbsa ():
    '''
    PVS_14_v3_cbsa_<state_FIPS>.shp - CBSA - Core Based Statistical Area 
    '''
    return()

def f_cd ():
    '''
    PVS_14_v3_cd_<state_FIPS>.shp - CD - Congressional District 
    '''
    return()

def f_cdp ():
    '''
    PVS_14_v3_cdp_<state_FIPS>.shp - CDP - Census Designated Place 
    '''
    return()

def f_county ():
    '''
    PVS_14_v3_county_<state_FIPS>.shp - COUNTY - County Boundary 
    '''
    return()

def f_elsd ():
    '''
    PVS_14_v3_elsd_<state_FIPS>.shp - ELSD - Elementary school districts 
    '''
    return()

def f_mcd ():
    '''
    PVS_14_v3_mcd_<state_FIPS>.shp - MCD - Minor Civil Division 
    '''
    return()

def f_necta ():
    '''
    PVS_14_v3_necta_<state_FIPS>.shp - NECTA - New England City and Town Area 
    '''
    return()

def f_place ():
    '''
    PVS_14_v3_place_<state_FIPS>.shp - PLACE – Incorporated Place 
    '''
    return()

def f_puma ():
    '''
    PVS_14_v3_puma_<state_FIPS>.shp - PUMA - Public Use Microdata Area 
    '''
    return()

def f_scsd ():
    '''
    PVS_14_v3_scsd_<state_FIPS>.shp - SCSD – Secondary School District 
    '''
    return()

def f_sldl ():
    '''
    PVS_14_v3_sldl_<state_FIPS>.shp - SLDL - State Legislative District Lower 
    '''
    return()

def f_sldu ():
    '''
    PVS_14_v3_sldu_<state_FIPS>.shp -SLDU–StateLegislativeDistrictUpper 
    '''
    return()

def f_state ():
    '''
    PVS_14_v3_state_<state_FIPS>.shp - STATE - State Boundaries 
    '''
    return()

def f_tbg ():
    '''
    PVS_14_v3_tbg_<state_FIPS>.shp - TBG - Tribal Block Group 
    '''
    return()

def f_tct ():
    '''
    PVS_14_v3_tct_<state_FIPS>.shp - TCT - Tribal Census Tract 
    '''
    return()

def f_tracts ():
    '''
    PVS_14_v3_tracts_<state_FIPS>.shp - TRACTS - Census Tract 
    '''
    return()

def f_uac ():
    '''
    PVS_14_v3_uac_<state_FIPS>.shp - UAC - Urban Area Census 
    '''
    return()

def f_unsd ():
    '''
    PVS_14_v3_unsd_<state_FIPS>.shp - UNSD - Unified School District
    '''
    return()

def f_tabblock2020 (v_counties_files,v_directories,v_market):
    '''
    PVS_21_v2_tabblock2020_<state_FIPS>.shp - 
    '''
    
    county_files = v_counties_files[0]
    v_county_file = county_files
    df = pd.read_csv (v_county_file)


    shapefiles = []
    for i in df['ID']:   
        v_shape_files = ('%s/partnership_shapefiles_21v2_%s/PVS_21_v2_tabblock2020_%s.shp'%(v_directories[0],i,i))
        shapefiles.append (v_shape_files)

    gdf = pd.concat([
                    gpd.read_file(shp)
                    for shp in shapefiles
                    ]).pipe(gpd.GeoDataFrame)

    
    gdf['Conty'] = gdf['STATEFP20']+gdf['COUNTYFP20']
    gdf['Conty'] =  gdf['Conty'].astype(int)


    x=0
    for i in df['ID']:
        gdf.loc[gdf['Conty'] == i, 'Conty'] = df.iloc[x,0]
        x=x+1
        
    gdf = gdf.to_crs('epsg:26912')
    v_geom = gdf['geometry']
    gdf['area'] = ((v_geom.area/1000)/1.609)  
    gdf['pop_mile'] = gdf['POP20']/((v_geom.area/1000)/1.609)  
    #gdf.loc[gdf['pop_per_mile'] == np.inf, 'pop_per_mile'] = 0          # look for infimity values and replace them by 0
    
    print (gdf)
    
    gdf = gdf.to_crs('epsg:4326')

    gdf.to_file('/Users/canobhu/Documents/GitHub/QGIS/USA_2020_Census/USA_2020_Census_Compile_Shape_Files/%s_tabblock2020_Pop.shp'%v_market)

    
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    gdf.plot(ax=ax)
    plt.show()
    
    return()

def f_gis_distance_area_test (v_counties_files,v_directories,v_market):
    
    county_files = v_counties_files[0]
    v_county_file = county_files
    df = pd.read_csv (v_county_file)

    v_shape_files = ('/Users/canobhu/Documents/GitHub/QGIS/USA_2020_Census/Utah/pvs_batch_from_49/partnership_shapefiles_21v2_49001/PVS_21_v2_tabblock2020_49001.shp')
    gdf = gpd.read_file (v_shape_files)
    print (gdf.head())
    
    gdf = gdf.to_crs('epsg:26912')
    s = gdf['geometry']
    print ((s.area/1000)/1.609)  
    

    v_shape_files1 = ('/Users/canobhu/Documents/GitHub/QGIS/USA_2020_Census/test_shape_file.shp')
    gdf1 = gpd.read_file (v_shape_files1)
    print (gdf1.head())
    
    gdf1 = gdf1.to_crs('epsg:26912')

    v_distance = gdf1.distance(gdf1.iloc[0,39])
    print ((v_distance/1000)/1.609)
    
    return()

######### 
# Begin

market = 'Idaho'

market_id = '16'

files = [
            '/Users/canobhu/Documents/GitHub/QGIS/USA_2020_Census/%s/%s_County.csv'%(market,market)
        ]
directories = [
                '/Users/canobhu/Documents/GitHub/QGIS/USA_2020_Census/%s/pvs_batch_from_%s'%(market,market_id)
                ]

#f_gis_distance_area_test (files,directories,market)

f_tabblock2020 (files,directories,market)

# End
######### 
