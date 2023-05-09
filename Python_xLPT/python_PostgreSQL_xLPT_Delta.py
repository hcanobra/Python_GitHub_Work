


import sys
import matplotlib
import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')
import PostgreSQL_API as pg


def q_query ():
    
    v_query =  ('''
                SELECT 
                    *
                FROM public."DMPL_XLPT_DAY"

            ''')
    
    return (v_query)

def c_postgresql_query_table (v_databasae,v_query):  
    cn = pg.Connection(v_databasae)  
    v_data =cn.PostgreSQL_query_df (v_query)
            
    return(v_data)  

def f_postgreSQL_query ():
       
    v_databasae = "vzw_xlpt"
    cn = pg.Connection(v_databasae)  
    v_data = cn.PostgreSQL_query_df (q_query())   
     
    v_data.to_csv ('/Users/canobhu/Downloads/xLPT_tmp/deltaq.csv', index=False)

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
    df_delta = df_delta[['DAY','MARKET','ENODEB','SITE',v_kpi]]

    df_delta['Diff_DELTA_%s'%v_kpi] = df_delta.groupby(['MARKET','ENODEB','SITE'])[v_kpi].diff().fillna(0)
    new_df = df_delta.groupby(['MARKET','ENODEB','SITE'])[v_kpi].agg({np.mean,np.median,np.std})
    df_stats = df_delta.merge(new_df, left_on=['MARKET','ENODEB','SITE'], right_index=True)
    
    df_stats['out'] =  np.where(
                                (df_stats['Peak_#_UE_In_Connected_Mode'] <= (df_stats['median'] - (df_stats['std']*1)))
                                |
                                (df_stats['Peak_#_UE_In_Connected_Mode'] >= (df_stats['median'] + (df_stats['std']*1)))
                                ,True,False)

    df_stats_sub = df_stats[df_stats['out']==True]
    
    print (df_stats_sub)
    

    v_df_low = df_stats_sub.sort_values(by=['Diff_DELTA_%s'%v_kpi])
    v_df_high = df_stats_sub.sort_values(by=['Diff_DELTA_%s'%v_kpi], ascending=False)
    
    print (v_df_low)
    print (v_df_high)
    
    v_df_low.to_csv('/Users/canobhu/Downloads/xLPT_tmp/v_df_low.csv',index=False)
    v_df_high.to_csv('/Users/canobhu/Downloads/xLPT_tmp/v_df_high.csv',index=False)
    
    

    #f_plot(df)

    
    
    df_stats.to_csv('/Users/canobhu/Downloads/xLPT_tmp/delta_dif.csv',index=False)

    return(df)

def f_plot(df): 
    
    v_mk_10 = df.loc[df['MARKET'] == 'MKT10']
    v_mk_11 = df.loc[df['MARKET'] == 'MKT11']
    v_mk_12 = df.loc[df['MARKET'] == 'MKT12']
    v_mk_13 = df.loc[df['MARKET'] == 'MKT13']


    v_data = [v_mk_10['DELTA_PEAK#_UE_IN_CONNECTED_MODE'],v_mk_11['DELTA_PEAK#_UE_IN_CONNECTED_MODE'],v_mk_12['DELTA_PEAK#_UE_IN_CONNECTED_MODE'],v_mk_13['DELTA_PEAK#_UE_IN_CONNECTED_MODE']]
    flierprops = dict(
                    marker='.', 
                    markerfacecolor='r', 
                    markersize=5,
                    linestyle='none',
                    markeredgecolor='g'
                    )
    
    fig1, ax1 = plt.subplots()
    ax1.set_title('Delta Peak# UE Connected Mode')
    ax1.boxplot(v_data,flierprops=flierprops)
    plt.xticks([1, 2, 3,4], ['MK10', 'MK11', 'MK12','MK13'])

    plt.show()
    
    return()

#/Begin

##v_kpi = 'UE_DL_Throughput_Mbps'

df = f_import_csv ()
df = f_postgreSQL_query ()
v_kpi = 'Peak_#_UE_In_Connected_Mode'
df = f_delta(df,v_kpi)

#/End

