import geopandas as gp
import pandas as pd
from shapely.geometry import Point
#import matplotlib
#import matplotlib.pyplot as plt


def f_closest (lat,lon,df):
    
    # CONVERT THE LAT AND LON INTO A GEOP POINT
    p1 = gp.GeoDataFrame(
                        geometry=gp.points_from_xy([lon],[lat]),
                        crs = "EPSG:4326")
    p1 = p1.to_crs('EPSG:26912')
    p1 = p1.loc[0]

    # CONVERT THE DATAFRAME INTO GEO DATAFRAME 
    gp_df = gp.GeoDataFrame (df, 
                            geometry = gp.points_from_xy(df['lon'],df['lat']), 
                            crs = "EPSG:4326")
    gp_df = gp_df.to_crs('EPSG:26912')

    # MAKES THE CALCULATIONS OF P1 DISTANCE TO EACH MEMBER ON THE DATAFRAME
    gp_df['Distance'] = gp_df['geometry'].distance(p1['geometry'])/1609
    gp_df = gp_df.sort_values(by='Distance',ignore_index=True)
    
    gp_df = gp_df.drop(columns='geometry')
    
    v_closest = gp_df.loc[0]

    return (v_closest)

def c_main():

    v_file = '/Users/canobhu/Downloads/location_example.csv'
    df = pd.read_csv (v_file)

    lat = 40.522872
    lon = -111.889581


    v_closest = f_closest (lat,lon,df)
    print (v_closest)

    return ()

# BEGIN
# END