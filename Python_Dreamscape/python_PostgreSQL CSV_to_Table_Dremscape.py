'''
Thhis script imports a .csv file into PostgreSQL
on a table named UT2_2021, this table will be used 
later in Excell to plot some data.
pwd
'''



from operator import contains
import pandas as pd
import geopandas as gp
import folium
from folium import plugins
import numpy as np


def f_root_data ():
    v_directory = '/Users/canobhu/Documents/File_Resources/RootMetrics/LosAngeles/'
    v_file = [
                'LosAngeles_CA_2022_1H_All_Data_Throughput_Tests',
                'LosAngeles_CA_2022_2H_All_Data_Throughput_Tests'
            ]


    df = pd.DataFrame()
    for file in v_file:
        v_location= v_directory+file+'.csv'
        v_df = pd.read_csv (v_location)
        df = pd.concat ([v_df,df])
    
    
    df = df[df['Network'].str.contains ('Verizon', na = False)]
    df = df[df['Data_Direction'].str.contains ('Download', na = False)]
    df = df[df['Network_Types'].str.contains ('NR', na = False)]

    df = df[[
            'Collection',
            'Network',
            'Activity',
            'Activity_Route',
            'UTC_Time',
            'Test_Cycle_ID',
            'Device_ID',
            'Device_Model_Number',
            'Data_Direction',
            'Access_Summary',
            'Access_Speed_Mean',
            'Access_Speed_Median',
            'Access_Speed_5th_Percentile',
            'Access_Speed_95th_Percentile',
            'Task_Summary',
            'Task_Speed_Median',
            'Start_Test_Latitude',
            'Start_Test_Longitude',
            'End_Test_Latitude',
            'End_Test_Longitude',
            'Average_GPS_Speed',
            'Average_LTE_RSRP',
            'Min_LTE_RSRP',
            'Max_LTE_RSRP',
            'Average_LTE_RSRQ',
            'Average_LTE_RSSNR',
            'Average_LTE_UE_PUSCH_Tx_Power',
            'Average_5G_SS_RSRP',
            'Average_5G_SS_RSRQ',
            'Average_5G_SS_RSSNR',
            'LTE_TAC',
            'LTE_eCI',
            'LTE_eNB_ID',
            'LTE_Band_Pcell',
            'LTE_Band_Scell1',
            'LTE_Band_Scell2',
            'LTE_Band_Scell3',
            '5G_Band_CC1',
            '5G_Band_CC2',
            '5G_Band_CC3',
            '5G_Band_CC4',
            '5G_Band_CC5',
            '5G_Band_CC6',
            '5G_Band_CC7',
            '5G_Band_CC8',
            'Average_LTE_Bandwidth',
            'Average_LTE_DL_RBs',
            'Average_LTE_UL_RBs',
            'LTE_Bandwidth_Pcell',
            'LTE_Bandwidth_Scell1',
            'LTE_Bandwidth_Scell2',
            'LTE_Bandwidth_Scell3',
            'Average_NR_BW',
            'Average_NR_DL_RBs',
            'Average_NR_UL_RBs',
            '5G_Bandwidth_CC1',
            'Average_LTE_DL_MCS',
            'Average_LTE_UL_MCS',
            'NR_RI_Mode',
            'Average_NR_DL_MCS',
            'Average_NR_UL_MCS',
            'NR_SCG_Failure',
            'Data_Delivery_Successes_%',
            'Final_Test_Speed',
            'Amount_of_Traffic',
            'Network_Types',
            'Network_Category'
                    ]]
        

    
    df = df.rename(columns={'End_Test_Latitude' :'lat', 'End_Test_Longitude' : 'lon'}, errors="raise")
    df = df.dropna(subset=['lat', 'lon'])
    
    
    # Create a GeoDataFrame from Pandas DataFrme
    gdf = gp.GeoDataFrame(df, geometry=gp.points_from_xy(df.lon, df.lat))
    
    
    # Create a geometry list from the GeoDataFrame
    geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in gdf.geometry ]
        
    return (gdf)

def f_cells_data ():
    
    url="http://datapro.eng.vzwcorp.com/download/sites_files/losangeles_cellver_0000.csv.gz"
    df = pd.read_csv(url, compression='gzip', header=0, sep=',', quotechar='"', error_bad_lines=False)

    df = df[[
        'BTS.',
        'Site',
        'CellCode',
        'Sector',
        'CellVersion',
        'Latitude(DecDeg)',
        'Longitude(DecDeg)',
        'Site Name',
        'Band',
        'CBSC_ECP_BSC',
        'ChannelNo',
        'Azimuth',
        'Dwntilt(Deg)',
        'Ant type',
        'Ant Bw(deg)',
        'Ant gain (dBi)',
        'cable loss(dB)',
        'Antenna c/l (m)',
        'AMSL (m)',
        'Air Interface',
        'Vendor',
        'V Ant Bw(deg)',
        'PCI Grp Index',
        'PCI Index',
        'LTE TAC',
        'eNodeB Sector ID',
        'PS Loc Code',
        'Ant Elec Tilt(deg)',
        'Ant Tip Height (feet)',
        'Location ID',
        'Remote Radio Head',
        'LTE Cell Type',
        'FIPS',
        'LTE Total Pwr (W)',
        'Num Tx Antennas',
        'Num Rx Antennas',
        'eNodeB Cell Name',
        'eNodeB Cell Alias'
                        ]]
    df = df.rename(columns={'Latitude(DecDeg)' :'lat', 'Longitude(DecDeg)' : 'lon'}, errors="raise")
    
    df = df[df['eNodeB Cell Name'].str.contains ('5G', na = False)]

    
    # Create a GeoDataFrame from Pandas DataFrme
    gdf = gp.GeoDataFrame(df, geometry=gp.points_from_xy(df.lon, df.lat))
    
    # Create a geometry list from the GeoDataFrame
    geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in gdf.geometry ]
    
    return(gdf)

def f_folium_root (df):
    
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

def f_popip_html (df):
    
    return ()

def f_folium_lamda (df):

    df_marks = df
    
    #render dataframe as html
    
    
    '''
    #html = df_marks.iloc[[0]].to_html()
    
    html = np.transpose(df_marks.iloc[[0]].to_html())


    #write html to file
    text_file = open("/Users/canobhu/Downloads/sites.html", "w")
    text_file.write(html)
    text_file.close()
        


    '''
    map_osm = folium.Map(location=[40.742, -73.956], zoom_start=11)

    df.apply(lambda row:folium.CircleMarker(
                                                location=[row["lat"], row["lon"]], 
                                                radius=3,
                                                fill=True,
                                                color="crimson",
                                                opacity=0.5,
                                                fill_opacity=0.5,
                                                popup = df_marks.iloc[[row]].to_html()
                                            )
                                                .add_to(map_osm), axis=1)

    minimap = plugins.MiniMap()
    map_osm.add_child(minimap)
    
    map_osm.save('/Users/canobhu/Downloads/py_folium_map_la.html')
    
    return ()
# ///////// BEGIN 

#df1 = f_root_data ()
df2 = f_cells_data ()

#print (df1.info())
#print (df2.info())

f_folium_lamda (df2)

#f_folium_root (df)

# ///////// END 

