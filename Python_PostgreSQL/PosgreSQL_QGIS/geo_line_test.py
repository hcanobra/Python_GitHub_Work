import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, shape

df = pd.read_csv('/Users/canobhu/Downloads/Geo_lines.csv', sep='\s*,\s*')
print (df)

#zip the coordinates into a point object and convert to a GeoData Frame
geometry = [Point(xy) for xy in zip(df.X, df.Y)]
geo_df = gpd.GeoDataFrame(df, geometry=geometry)

geo_df2 = geo_df.groupby(['ID', 'Hour'])['geometry'].apply(lambda x:LineString(x.tolist()))
geo_df2 = gpd.GeoDataFrame(geo_df2, geometry='geometry')

print (geo_df2)