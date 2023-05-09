

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, GeometryCollection


def f_line_sample ():
    
    df = pd.read_csv('/Users/canobhu/Downloads/points.csv')
    
    #zip the coordinates into a point object and convert to a GeoData Frame
    geometry = [Point(xy) for xy in zip(df.X, df.Y)]
    geo_df = gpd.GeoDataFrame(df, geometry=geometry)
    print (geo_df)

    geo_df2 = geo_df.groupby(['ID', 'Hour'])['geometry'].apply(lambda x: LineString(x.tolist()))
    geo_df2 = gpd.GeoDataFrame(geo_df2, geometry='geometry')

    print (geo_df2)

    return ()

def f_line_sample2 ():
        
    o = [Point (-116.2847753565571, 43.61722615312507),
        Point(-116.2847753565571, 43.61722615312507),
        Point (-116.2847753565571,43.61722615312507)]

    d = [Point (-116.3042144501943, 43.60844476082184),
        Point(-116.3042144501943,43.60844476082184),
        Point(-116.3042144501943,43.60844476082184)]

    df = pd.DataFrame({'orig_coord' : o, 'dest_coord': d})
    df['line']=df.apply(lambda x: LineString([x['orig_coord'], x['dest_coord']]),axis=1)

    print(df['line'])

    return()

def f_line (df):
        
    #zip the coordinates into a point object and convert to a GeoData Frame
    #geometry = [Point(xy) for xy in zip(df['point_start'], df['point_end'])]
    geo_df = gpd.GeoDataFrame(df)
    print (geo_df)

    geo_df2 = geo_df.groupby(['Test_Cycle_ID','Driver-Kit', 'Network'])['geometry'].apply(lambda x: LineString(x.tolist()))
    geo_df2 = gpd.GeoDataFrame(geo_df2)

    print (geo_df2)

    return ()

def main():
    df = pd.read_csv('/Users/canobhu/Documents/File_Resources/RootMetrics/SLC/SaltLakeCity_UT2022_1H/SaltLakeCity_UT_2022_1H_All_Mobile_to_Mobile_Tests.csv')

    #print (df.info())

    df['point_start'] = gpd.GeoDataFrame(
                        geometry=gpd.points_from_xy(df['Start_Test_Longitude'],df['Start_Test_Latitude']),
                        crs = "EPSG:4326")

    df['point_end'] = gpd.GeoDataFrame(
                        geometry=gpd.points_from_xy(df['End_Test_Longitude'],df['End_Test_Latitude']),
                        crs = "EPSG:4326")

    df['line']=df.apply(lambda x: LineString([x['point_start'], x['point_end']]),axis=1)

    #df['geo']=df.apply(lambda x: GeometryCollection([x['line'], x['point_start'], x['point_end']]),axis=1)


    print(df.head())

    print(df)

    df = gpd.GeoDataFrame (df,
                        geometry=df['line'],
                        crs = "EPSG:4326")
                        
    df = df.drop(['point_start','point_end','line'],1)

    df = df.to_crs('epsg:4326')

    df.to_file('/Users/canobhu/Documents/File_Resources/RootMetrics/SLC/SaltLakeCity_UT2022_1H/SaltLakeCity_UT_2022_1H_All_Mobile_to_Mobile_Tests.shp')

    
    #fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    #df.plot(ax=ax)
    #plt.show()
    
    print(df.head())

main()

