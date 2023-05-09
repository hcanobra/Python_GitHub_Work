
from ast import IsNot
from itertools import count
import os

import matplotlib.pyplot as plt
from numpy import int64
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, GeometryCollection
from sqlalchemy import null




def f_drive (df,cycle):

    df['point_start'] = gpd.GeoDataFrame(
                        geometry=gpd.points_from_xy(df['Start_Test_Longitude'],df['Start_Test_Latitude']),
                        crs = "EPSG:4326")

    df['point_end'] = gpd.GeoDataFrame(
                        geometry=gpd.points_from_xy(df['End_Test_Longitude'],df['End_Test_Latitude']),
                        crs = "EPSG:4326")

    df['line']=df.apply(lambda x: LineString([x['point_start'], x['point_end']]),axis=1)

    df['geo']=df.apply(lambda x: GeometryCollection([x['line'], x['point_start'], x['point_end']]),axis=1)


    #print(df)

    df = gpd.GeoDataFrame (df,
                        geometry=df['line'],
                        crs = "EPSG:4326")
                        
    df = df.drop(['point_start','point_end','line','geo'],1)

    df = df.to_crs('epsg:4326')

    v_cycle = (cycle.split('.'))
    
    f_file = ('/Users/canobhu/Documents/File_Resources/RootMetrics/Ogden/Ogden_RootMetrics_ShapeFiles/%s_drive_route.shp'%v_cycle[0])
    print (f_file)
    
    df.to_file(f_file)
    
def f_start_points (df,cycle):      ## BETA


    df['point_start'] = gpd.GeoDataFrame(
                        geometry=gpd.points_from_xy(df['Start_Test_Longitude'],df['Start_Test_Latitude']),
                        crs = "EPSG:4326")

    df['point_end'] = gpd.GeoDataFrame(
                        geometry=gpd.points_from_xy(df['End_Test_Longitude'],df['End_Test_Latitude']),
                        crs = "EPSG:4326")

    df['line']=df.apply(lambda x: LineString([x['point_start'], x['point_end']]),axis=1)

    df['geo']=df.apply(lambda x: GeometryCollection([x['line'], x['point_start'], x['point_end']]),axis=1)

    df = gpd.GeoDataFrame (df,
                        geometry=df['point_start'],
                        crs = "EPSG:4326")
                        
    df = df.drop(['point_start','point_end','line','geo'],1)

    df = df.to_crs('epsg:4326')

    v_cycle = (cycle.split('.'))
    
    f_file = ('/Users/canobhu/Documents/File_Resources/RootMetrics/Ogden/Ogden_RootMetrics_ShapeFiles/%s_start_points.shp'%v_cycle[0])
    print (f_file)
    
    df.to_file(f_file)

def f_end_points (df,cycle):        ## BETA

    df['point_start'] = gpd.GeoDataFrame(
                        geometry=gpd.points_from_xy(df['Start_Test_Longitude'],df['Start_Test_Latitude']),
                        crs = "EPSG:4326")

    df['point_end'] = gpd.GeoDataFrame(
                        geometry=gpd.points_from_xy(df['End_Test_Longitude'],df['End_Test_Latitude']),
                        crs = "EPSG:4326")

    df['line']=df.apply(lambda x: LineString([x['point_start'], x['point_end']]),axis=1)

    df['geo']=df.apply(lambda x: GeometryCollection([x['line'], x['point_start'], x['point_end']]),axis=1)

    df = gpd.GeoDataFrame (df,
                        geometry=df['point_end'],
                        crs = "EPSG:4326")
                        
    df = df.drop(['point_start','point_end','line','geo'],1)

    df = df.to_crs('epsg:4326')

    v_cycle = (cycle.split('.'))
    
    f_file = ('/Users/canobhu/Documents/File_Resources/RootMetrics/Ogden/Ogden_RootMetrics_ShapeFiles/%s_end_points.shp'%v_cycle[0])
    print (f_file)
    
    df.to_file(f_file)

def f_RF_quality ():                ## BETA
    
    v_rsrp_range = np.array_split(np.array(range(-132,1)),7)
    df_rsrp = pd.DataFrame(v_rsrp_range)
    df_rsrp = df_rsrp.T
    df_rsrp.columns = ["Bad","Poor","Poor-Med","Med","Med_Good","Good","Excelent"]
        
    v_rsrq_range = np.array_split(np.array(range(-23,-9)),7)
    df_rsrq = pd.DataFrame(v_rsrq_range)
    df_rsrq = df_rsrq.T
    df_rsrq.columns = ["Bad","Poor","Poor-Med","Med","Med_Good","Good","Excelent"]
        
    v_sinr_range = np.array_split(np.array(range(-20,1)),7)
    df_sinr = pd.DataFrame(v_sinr_range)
    df_sinr = df_sinr.T
    df_sinr.columns = ["Excelent","Good","Med_Good","Med","Poor-Med","Poor","Bad"]

    print (df_sinr)

    print (df['AverageLTERSRP'])
    print (min(df_rsrp['Bad']))
    
    print (df.info())
    df['RSRP_SCORE'] = df["AverageLTERSRP"]
    #df['RSRP_SCORE'] = np.where((df["AverageLTERSRP"].all <=120, "test",df["AverageLTERSRP"]))
    #df_test = df.loc[df["AverageLTERSRP"]  <= -120]
    df.loc[df['AverageLTERSRP']  <= -120, df['RSRP_SCORE']]  = 'Test'

    df.to_csv("test.csv")
    print (df)

    #print (df['AverageLTERSRQ'])
    #print (df['AverageLTESINR'])
    
    return()

def f_locations (df,cycle):

    df_shape = gpd.GeoDataFrame(
                        df,
                        geometry=gpd.points_from_xy(df['Longitude'],df['Latitude']),
                        crs = "EPSG:4326")

    
    v_cycle = (cycle.split('.'))
    
    f_file = ('/Users/canobhu/Documents/File_Resources/Spirent/Drive_Results_Shape_Files/Spirent_VQ/%s_drive_route.shp'%v_cycle[0])

    df_shape.to_file(f_file)
    return ()

def f_m2m_shape_file ():

    path = '/Users/canobhu/Documents/File_Resources/Spirent/Spirent_VQ/'
    dir_list = [f for f in os.listdir(path) if f.endswith('.csv')]

    for i in dir_list:   
        v_shape_files = (path+i)
        #print (v_shape_files)
        df = pd.read_csv (v_shape_files, low_memory=False)
        #print (df.head())
        
        df['IMEI'] = df['IMEI'].astype('Int64').astype('str')
        df['PhoneNumber'] = df['PhoneNumber'].astype('Int64').astype('str')
        df['idx'] =  df [['Carrier','IMEI','PhoneNumber']].apply(lambda x : ''.join(x), axis=1)

        options = ['Mobile-to-mobile Call Originating Test Start', 'Mobile-to-mobile Call Originating Test','Mobile-to-mobile Call Originating Test End']
        #values = df[df['Task_Summary'] == 'Failure']['idx'].tolist()

        df['Result'] = df['CallResult']
        
        df.loc[(df['CallResult']) == 'Term. Fail', 'Result'] = 'M2M_Ter_IA'
        df.loc[(df['CallResult']) == 'Orig. Fail', 'Result'] = 'M2M_Org_IA'
        df.loc[(df['CallResult']) == 'Drop', 'Result'] = 'M2M_DC'
        
        
        #f_locations (df,i)
        
    return (df)

def f_stats (df,v_carrier):
    
    df_verizon = df[df['Carrier'] == v_carrier]
    
    print ("############################################")
    print ("############ STATS FOR %s ##################"%v_carrier)

    df_verizon_stats = df_verizon[['CallSetupTime','AverageLTERSRP','AverageLTERSRQ','AverageLTESINR','Average5GNRRSRP','Average5GNRRSRQ','Average5GNRSINR']]

    print (df_verizon_stats.describe())
    

    # Section retreaves median, 95th percentile, 5th percentile
    v_median = df_verizon_stats['CallSetupTime'].quantile(.5)
    
    print ('####$#$#$#$#$',v_median)
    v_95_per = df_verizon_stats['CallSetupTime'].quantile(.95)
    v_5_per = df_verizon_stats['CallSetupTime'].quantile(.05)
    
    df_verizon_M2M = df_verizon[df_verizon['MOS_CallSeq'].notnull()]


    v_test_count = df_verizon_M2M[df_verizon_M2M['TaskType'] == 'VQ Test - MO'].shape[0]
        
        
         
    df_verizon_M2M_orig = df_verizon_M2M[df_verizon_M2M['TaskType'] == "VQ Test - MO"]
    df_verizon_M2M_orig_fail = df_verizon_M2M_orig[df_verizon_M2M_orig['CallResult'] == 'Orig. Fail']
    v_m2m_orig_failure = ((df_verizon_M2M_orig_fail.shape[0]*100)/df_verizon_M2M_orig.shape[0])

    
    df_verizon_M2M_term = df_verizon_M2M[df_verizon_M2M['TaskType'] == "VQ Test - MT"]
    df_verizon_M2M_term_fail = df_verizon_M2M_term[df_verizon_M2M_term['CallResult'] == 'Term. Fail']
    v_m2m_ter_failure = ((df_verizon_M2M_term_fail.shape[0]*100)/df_verizon_M2M_term.shape[0])
    
    df_verizon_M2M_dc = df_verizon_M2M[df_verizon_M2M['TaskType'] == "VQ Test - MT"]
    df_verizon_M2M_dc_fail = df_verizon_M2M_dc[df_verizon_M2M_dc['CallResult'] == 'Drop']
    v_m2m_dc_failure = ((df_verizon_M2M_dc_fail.shape[0]*100)/df_verizon_M2M_dc.shape[0])


    return(v_m2m_orig_failure,v_m2m_ter_failure,v_m2m_dc_failure,v_median,v_95_per,v_5_per,v_test_count)

def f_m2m (df):
    vzw_m2m_orig_failure,vzw_m2m_ter_failure,vzw_m2m_dc_failure,vzw_setup_median,vzw_95_per,vzw_5_per,vzw_test_count = f_stats (df,"Verizon")
    tmo_m2m_orig_failure,tmo_m2m_ter_failure,tmo_m2m_dc_failure,tmo_setup_median,tmo_95_per,tmo_5_per,tmo_test_count = f_stats (df,"T-Mobile")
    att_m2m_orig_failure,att_m2m_ter_failure,att_m2m_dc_failure,att_setup_median,att_95_per,att_5_per,att_test_count = f_stats (df,"AT&T")
    
    
    print ("############################################")
    print ("M2M Test count: ")
    print("Verizon: ",vzw_test_count)
    print("T-Mobile: ",tmo_test_count)
    print("At&T: ",att_test_count) 
    
    print ("############################################")
    print ("Median Setup Times: ")
    print("Verizon: ",vzw_setup_median)
    print("T-Mobile: ",tmo_setup_median)
    print("At&T: ",att_setup_median)
    
    print ("############################################")
    print ("5th percentile Setup Times: ")  
    print("Verizon: ",vzw_5_per)
    print("T-Mobile: ",tmo_5_per)
    print("At&T: ",att_5_per)
    
    print ("############################################")
    print ("95th percentile Setup Times: ")
    print("Verizon: ",vzw_95_per)
    print("T-Mobile: ",tmo_95_per)
    print("At&T: ",att_95_per)
    
    print ("############################################")
    print ("Spirent M2M (%) Call Initition Failures: ")
    print("Verizon: ",vzw_m2m_orig_failure)
    print("T-Mobile: ",tmo_m2m_orig_failure)
    print("At&T: ",att_m2m_orig_failure)

    print ("############################################")
    print ("Spirent M2M (%) Call Termination Failures: ")
    print("Verizon: ",vzw_m2m_ter_failure)
    print("T-Mobile: ",tmo_m2m_ter_failure)
    print("At&T: ",att_m2m_ter_failure)

    print ("############################################")
    print ("Spirent M2M (%) Call Drops: ")
    print("Verizon: ",vzw_m2m_dc_failure)
    print("T-Mobile: ",tmo_m2m_dc_failure)
    print("At&T: ",att_m2m_dc_failure)
    
    return ()


def f_data_shape_file ():
    path = '/Users/canobhu/Documents/File_Resources/Spirent/Spirent_Data/'
    dir_list = [f for f in os.listdir(path) if f.endswith('.csv')]

    for i in dir_list:   
        v_shape_files = (path+i)
        #print (v_shape_files)
        df = pd.read_csv (v_shape_files, low_memory=False)
        #print (df.head())
        
        df['IMEI'] = df['IMEI'].astype('Int64').astype('str')
        df['PhoneNumber'] = df['PhoneNumber'].astype('Int64').astype('str')
        df['idx'] =  df [['Carrier','IMEI','PhoneNumber']].apply(lambda x : ''.join(x), axis=1)
        
        df = df.loc[(df['DataTaskType'] == 'HTTP_DOWNLOAD') | (df['DataTaskType'] == 'HTTP_UPLOAD')] # Filter the data set by Upload and down load only
        #print (df['DataTaskType'].unique())
        #f_locations (df,i)
        
    return (df)

def f_data (df):
    
    return ()

# Get the list of all files and directories

# M2M Information 
m2m_df =  f_m2m_shape_file ()
f_m2m (m2m_df)

'''
# Data Information 
data_df =  f_data_shape_file ()

data_df_down = data_df[(data_df['DataTaskType'] == 'HTTP_DOWNLOAD')]
data_df_up = data_df[(data_df['DataTaskType'] == 'HTTP_UPLOAD')]

print (data_df['DataTaskType'].unique())

data_df_Test = data_df_down[['Carrier','ServingNetwork']]
data_df_nr = data_df_Test.groupby(['Carrier','ServingNetwork'])['ServingNetwork'].count()
print (data_df_nr)
data_df_nr1=data_df_Test.groupby(['Carrier','ServingNetwork'])['ServingNetwork'].count().rename("Pct").groupby(level = 0).transform(lambda x: x/x.sum())
print(data_df_nr1)

data_df_Test = data_df_up[['Carrier','ServingNetwork']]
data_df_nr = data_df_Test.groupby(['Carrier','ServingNetwork'])['ServingNetwork'].count()
print (data_df_nr)
data_df_nr1=data_df_Test.groupby(['Carrier','ServingNetwork'])['ServingNetwork'].count().rename("Pct").groupby(level = 0).transform(lambda x: x/x.sum())
print(data_df_nr1)

print (data_df_down.describe())
'''