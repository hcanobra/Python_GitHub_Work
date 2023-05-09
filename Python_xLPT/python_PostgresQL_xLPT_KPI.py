
import sys
import matplotlib
import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')
import PostgreSQL_API as pg


def q_query (v_eNB,v_date,v_kpi):
    
    v_kpi = '","'.join(map(str, v_kpi))
    v_eNB = "','".join(map(str, v_eNB))
    
    v_query =  ('''
                SELECT 
                    "%s"
                FROM public."DMPL_XLPT_DAY"
                WHERE "DAY" = '%s'
                AND
                "ENODEB" IN ('%s')
                

            '''%(v_kpi,v_date,v_eNB))
    
    return (v_query)

def c_postgresql_query_table (v_databasae,v_query):  
    cn = pg.Connection(v_databasae)  
    v_data =cn.PostgreSQL_query_df (v_query)
            
    return(v_data)  

def f_postgreSQL_query (v_query):
       
    v_databasae = "vzw_xlpt"
    cn = pg.Connection(v_databasae)  
    
    
    v_data = cn.PostgreSQL_query_df (v_query)   
     
    v_data.to_csv ('/Users/canobhu/Downloads/xLPT_tmp/Python_xLPT_kpi.csv', index=False)

    return(v_data)     

def f_import_csv ():
    v_file = '/Users/canobhu/Downloads/xLPT_tmp/deltaq.csv'
    df = pd.read_csv (v_file)

    #df = df.astype({'MARKET': 'object'}).dtypes
    df['MARKET']= df['MARKET'].astype(object)
    
    print (df.head())
    print (df.info())
    return(df)

def f_delta(df,v_kpi):
    
    df_delta = df
    df_delta = df_delta[['DAY','MARKET','ENODEB','SITE','weekday',v_kpi]]

    df_delta['Diff_DELTA_%s'%v_kpi] = df_delta.groupby(['MARKET','ENODEB','SITE','weekday'])[v_kpi].diff().fillna(0)
    new_df = df_delta.groupby(['MARKET','ENODEB','SITE','weekday'])[v_kpi].agg({np.mean,np.median,np.std})
    df_stats = df_delta.merge(new_df, left_on=['MARKET','ENODEB','SITE','weekday'], right_index=True)
    
    df_stats = df_stats[df_stats['mean']>0]

    #print('filtered')
    #print (df_stats.sort_values(by=['mean']))
    
    
    df_stats['out'] =  np.where(
                                (df_stats['Peak_#_UE_In_Connected_Mode'] <= (df_stats['median'] - (df_stats['std']*1)))
                                |
                                (df_stats['Peak_#_UE_In_Connected_Mode'] >= (df_stats['median'] + (df_stats['std']*1)))
                                ,True,False)

    print (df_stats)


    df_stats_sub = df_stats[df_stats['out']==True]    
    
    print (df_stats_sub)
    
    v_df_low = df_stats_sub.sort_values(by=['Diff_DELTA_%s'%v_kpi])
    v_df_high = df_stats_sub.sort_values(by=['Diff_DELTA_%s'%v_kpi], ascending=False)
    
    
    #v_df_high.to_csv('/Users/canobhu/Downloads/xLPT_tmp/v_df_high.csv',index=False)
    df_stats.to_csv('/Users/canobhu/Downloads/xLPT_tmp/delta_dif.csv',index=False)

    #f_plot(df)

    return(v_df_low,v_df_high,df_stats)

def f_day_week(df,v_kpi):
    df["weekday"] = pd.to_datetime(df['DAY']).dt.day_name()
    
    #print (df["weekday"].unique())
    #print (df)

    return (df)

#/Begin
######## 

v_eNB = ['11300',
        '10330',
        '10349',
        '11163',
        '10023',
        '13204',
        '13210']
v_date = '07/04/2022' 


v_kpi = ["DAY",
"MARKET",
"ENODEB",
"SITE",
"Peak_#_UE_In_Connected_Mode",
"UE_DL_Throughput_Mbps",
"Cell_Availability",
"Context_Droppct_Num",
"Context_Droppct_Den",
"RRC_Setup_Failurepct_Num",
"RRC_Setup_Failurepct_Den",
"Bearer_Setup_Failurepct_Num",
"Bearer_Droppct_Den",
"Context_Setup_Failurepct_Num",
"Context_Setup_Failurepct_Den",
"SIP_SC_Call_Attempts",
"SIP_SC_Call_Setup_Failures",
"SIP_SC_Call_Completions",
"SIP_SC_Call_Drops",
"Downlink_Data_Volume_MB_Test",
"Downlink_Throughput_in_Mbps",
"DL_Data_Vol_MAC_in_MB",
"UL_Data_Vol_MAC_in_Mb"]

v_query = q_query (v_eNB,v_date,v_kpi)
f_postgreSQL_query (v_query)


'''
v_kpi = 'Peak_#_UE_In_Connected_Mode'
df = f_day_week(df,v_kpi)

print (df['weekday'].unique())

for days in df['weekday'].unique():
    df1 = df.loc[df['weekday']==days]
    v_df_low,v_df_high,df_stats = f_delta(df1,v_kpi)
        
    ## Outlier data frame by lower volume delta
    try:
        v_df2_low = pd.read_csv('/Users/canobhu/Downloads/xLPT_tmp/v_df_low.csv', header=0)
        #print ("File exist")
        frames = [v_df2_low,v_df_low.head()]
        v_df2_low = pd.concat(frames)
        #print (v_df2_low)
        v_df2_low.to_csv('/Users/canobhu/Downloads/xLPT_tmp/v_df_low.csv',index=False)

    except:
        #print ("File does not exist")
        v_df_low.head().to_csv('/Users/canobhu/Downloads/xLPT_tmp/v_df_low.csv',index=False)

    ## Outlier data frame by high volume delta
    try:
        v_df2_high = pd.read_csv('/Users/canobhu/Downloads/xLPT_tmp/v_df_high.csv', header=0)
        #print ("File exist")
        frames = [v_df2_high,v_df_high.head()]
        v_df2_high = pd.concat(frames)
        #print (v_df2_high)
        v_df2_high.to_csv('/Users/canobhu/Downloads/xLPT_tmp/v_df_high.csv',index=False)

    except:
        #print ("File does not exist")
        v_df_high.head().to_csv('/Users/canobhu/Downloads/xLPT_tmp/v_df_high.csv',index=False)
'''
#/End