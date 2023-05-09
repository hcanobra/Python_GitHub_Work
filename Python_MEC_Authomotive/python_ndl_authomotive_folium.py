
'''

https://python-visualization.github.io/folium/modules.html


# folium icon
You can find a full list here:
https://fontawesome.com/icons?d=gallery
use with: prefix='fa'

or the glyphicon icons of Bootstrap that are built-in and standard, thus without prefix needed. https://getbootstrap.com/docs/3.3/components/



https://medium.com/datasciencearth/map-visualization-with-folium-d1403771717

#
HOW TO CREATE MULTIPLE LAYERS IN FOLIUM

https://www.analyticsvidhya.com/blog/2020/06/guide-geospatial-analysis-folium-python/

#
Best Libraries for Geospatial Data Visualisation in Python
https://towardsdatascience.com/best-libraries-for-geospatial-data-visualisation-in-python-d23834173b35

#
Interactive Geospatial Data Visualization with Geoviews in Python
https://towardsdatascience.com/interactive-geospatial-data-visualization-with-geoviews-in-python-7d5335c8efd1


#
Interactive Map visualization with Folium in Python
https://medium.com/@saidakbarp/interactive-map-visualization-with-folium-in-python-2e95544d8d9b

#
Hexbin map from geoJson file with Python
https://www.python-graph-gallery.com/hexbin-map-from-geojson-python


#
Add 3D terrain to a map
https://docs.mapbox.com/mapbox-gl-js/example/add-terrain/

#
Folium Quickstart
https://python-visualization.github.io/folium/quickstart.html


#
Hexbin Mapbox in Python
https://plotly.com/python/hexbin-mapbox/

#
Playing With Uber’s Hexagonal Hierarchical Spatial Index, H3
https://betterprogramming.pub/playing-with-ubers-hexagonal-hierarchical-spatial-index-h3-ed8d5cd7739d


#
How to change circle opacity in Folium?
https://gis.stackexchange.com/questions/381356/how-to-change-circle-opacity-in-folium

#
Plotting with GeoPandas and Folium
https://geopandas.org/en/stable/gallery/plotting_with_folium.html
'''


# importing sys
import sys
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')

import PostgreSQL_API as pg
import pandas as pd
import geopandas as gp


import folium
from folium import plugins

def temp_folium_sample ():
    '''
    map = folium.Map(location=[40.4939349,-111.8680188], tiles="OpenStreetMap",  zoom_start=20)
    map.save('/Users/canobhu/Downloads/py_folium_map.html')
    '''


    map = folium.Map(location=[45.372, -121.6972], zoom_start=12, tiles="Stamen Terrain")

    tooltip = "Click me!"

    folium.Marker(
        location=[45.3288, -121.6625],
        popup="Mt. Hood Meadows",
        icon=folium.Icon(icon="cloud"),
        ).add_to(map)

    folium.CircleMarker(
        location=[45.3311, -121.7113],
        popup="The Waterfront",
        radius=6,
        fill=True,
        color="crimson",
        opacity=0.5,
        fill_opacity=0.5,
        ).add_to(map)

    folium.CircleMarker(
        location=[45.3300, -121.6823],
        radius=3,
        popup="Laurelhurst Park",
        color="#3186cc",
        fill=True,
        fill_color="#3186cc"
        ).add_to(map)


    minimap = plugins.MiniMap()
    map.add_child(minimap)

    map.save('/Users/canobhu/Downloads/py_folium_map.html')

def q_posgresql_query ():
    v_sql_commands = ('''
                    SELECT * FROM public.truecall_presto_views_f_truecall_lsr_raw_v0_mk12_20221015

                    ''')
    return (v_sql_commands)

def c_postgresql_query_table (v_databasae):
    
    cn = pg.Connection(v_databasae)
    
    v_data =cn.PostgreSQL_query_df (q_posgresql_query())
            
    print (v_data)    
    
    return(v_data)    

def f_folium_map (df):
    
    # Create a GeoDataFrame from Pandas DataFrme
    gdf = gp.GeoDataFrame(df, geometry=gp.points_from_xy(df.end_location_lon, df.end_location_lat))
    
    # Create a geometry list from the GeoDataFrame
    geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in gdf.geometry ]

    print (gdf)
    
    map = folium.Map(location=[40.4939349,-111.8680188], tiles="OpenStreetMap",  zoom_start=10)
    
    tooltip = "Click me!"
    
    # Iterate through list and add a marker for each volcano, color-coded by its type.
    i = 0
    for coordinates in geo_df_list:
        # Place the markers with the popup labels and data
        map.add_child(
                        folium.CircleMarker
                                (location = coordinates,
                                    radius=3,
                                    fill=True,
                                    color="crimson",
                                    opacity=0.5,
                                    fill_opacity=0.5,
                                    popup =
                                           'start_time: ' + str(gdf.start_time[i]) + '<br>' +
                                            'end_time: ' + str(gdf.end_time[i]) + '<br>' +

                                            'end_location_lat: ' + str(gdf.end_location_lat[i]) + '<br>' +
                                            'end_location_lon: ' + str(gdf.end_location_lon[i]) + '<br>' +

                                            'environment: ' + str(gdf.environment[i]) + '<br>' +
                                            'service_type: ' + str(gdf.service_type[i]) + '<br>' +
                                            'final_disposition: ' + str(gdf.final_disposition[i]) + '<br>' +
                                            's1_release_cause: ' + str(gdf.s1_release_cause[i]) + '<br>' +
                                            'start_enb: ' + str(gdf.start_enb[i]) + '<br>' +
                                            'end_enb: ' + str(gdf.end_enb[i]) + '<br>' +

                                            'rsrp_dbm: ' + str(gdf.rsrp_dbm[i]) + '<br>' +
                                            'rsrq_db: ' + str(gdf.rsrq_db[i]) + '<br>' +

                                            'mac_volume_dl_bytes: ' + str(gdf.mac_volume_dl_bytes[i]) + '<br>' +
                                            'mac_volume_ul_bytes: ' + str(gdf.mac_volume_ul_bytes[i]) + '<br>' +

                                            'qci_list: ' + str(gdf.qci_list[i]) + '<br>' +

                                            'pusch_sinr_db: ' + str(gdf.pusch_sinr_db[i]) + '<br>' +

                                            'ta_distance_meters: ' + str(gdf.ta_distance_meters[i]) + '<br>' +
                                            'intersite_distance_meters: ' + str(gdf.intersite_distance_meters[i]) + '<br>' +
                                            'nr_rsrp_dbm: ' + str(gdf.nr_rsrp_dbm[i]) + '<br>' +
                                            'nr_rsrq_db: ' + str(gdf.nr_rsrq_db[i]) + '<br>' +
                                            'nr_dl_sinr_db: ' + str(gdf.nr_dl_sinr_db[i]) + '<br>',
                                )
                    )
        i = i + 1

    minimap = plugins.MiniMap()
    map.add_child(minimap)
    
    map.save('/Users/canobhu/Downloads/py_folium_map.html')
    
    return ()



# ///////// BEGIN 

v_databasae = 'vzw_truecall'

df = c_postgresql_query_table (v_databasae)                     # AFTER INFORMAITON IS EXTRACTED FROM FUZE VIA NDL THIS FUNCITON JOINS BOTH TABLES, AND GENERATES TWO TABLES, 
                                                                # 1ST TABLE) CONTAINING FUZE PROJECTS SOME BASIC INFORMAIOTN ABOUT THE PROJECT AND THE LAT LONG INFORMATION --- NAMED: vzw_fuze_loc
                                                                # 2ND TABLE) CONTAINING PROJECT INFORMATION AND DASHBOARD INFORMATION - NAMED: vzw_fuze_qgis

f_folium_map (df)

# ///////// END 
