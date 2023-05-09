


# importing sys
import sys
  
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')


import pandas as pd
import time
import numpy as np
import os
import matplotlib.pyplot as plt


def f_df_formating(df):
    f_df = df
    f_df = f_df.fillna(0)
    f_df['idx'] = f_df['idx'].astype(object)
    #f_df['TCP_len'] = f_df['TCP_len'].astype(int)
    return (f_df)
    
def f_unique (df):
    f_df = df
    #f_unique = f_df.loc[f_df['TCP_len'] == 0]
    f_unique = df
    f_unique = f_unique[['TCP_ack','Relative_time']]
    f_unique = f_unique.drop_duplicates (subset = 'TCP_ack')
    
    return (f_unique)

def f_rtt (df,unique ):
    #f_df = df.loc[df['TCP_len'] == 0]
    f_df = df
    f_unique = unique 
    
    #/ Renames the columns of unique DataFrame, these colums will be use later for the join function    
    '''
         TCP_seq  ACK_Relative_time
0              0           0.000000
1     2580699347           0.065545
2     1605494743           0.065887
4     2580699384           0.139292
    '''
    f_unique.columns = ['TCP_seq','ACK_Relative_time']
    
    
    f_df.to_csv ('/Users/canobhu/Downloads/f_df.csv',index=False)
    f_unique.to_csv ('/Users/canobhu/Downloads/f_unique.csv',index=False)

    #/ Join function, adds the ACK relative time column on the original dataframe when the column 'TCP_seq' value matches
    '''
TCP_seq     ACK_Relative_time       idx     Relative_time       Frame_Delta     TCP_ack     TCP_len     TCP_flags
    |       |                       |       |                   |               |           |           |
    |       |                       |       |                   |               |           |           o-> Column from f_df DF
    |       |                       |       |                   |               |           o-------------> Column from f_df DF
    |       |                       |       |                   |               o-------------------------> Column from f_df DF
    |       |                       |       |                   o-----------------------------------------> Column from f_df DF
    |       |                       |       o-------------------------------------------------------------> Column from f_df DF
    |       |                       o---------------------------------------------------------------------> Column index from f_df DF
    |       o---------------------------------------------------------------------------------------------> Relative time column from f_unique DF
    o-----------------------------------------------------------------------------------------------------> Column index from f_unique DF
    '''
    df = pd.merge(left=f_unique, right=f_df, how='right')
    print (df.head(50))
    df.to_csv ('/Users/canobhu/Downloads/f_merge.csv',index=False)


    #/ Make the calcualtion to subsract the ACK timestamp minus the SEQ time stamp
    df['RTT'] = df['ACK_Relative_time'] - df['Relative_time']

    #/ Re organize the columns 
    '''
    TCP_seq  ACK_Relative_time                idx  Relative_time  Frame_Delta     TCP_ack  TCP_len TCP_flags       RTT
0    2580699347           0.065545  1675356369.000976       0.000000     0.000000           0        0         S  0.065545
1    1605494743           0.065887  1675356369.066522       0.065545     0.065545  2580699347        0        SA  0.000342
2    2580699348                NaN  1675356369.066863       0.065887     0.000342  1605494743        0         A       NaN
3    1605494744           0.139537  1675356369.140268       0.139292     0.073329  2580699384        0         A  0.000245
    '''   
    df = df[[
            'idx',
            'Relative_time',
            'Frame_Delta',
            'ACK_Relative_time',
            'TCP_seq',
            'TCP_ack',
            'TCP_flags',
            'RTT'
            ]]
    
    #/ Sort the datapoints by Relative time value
    '''
                   idx  Frame_Delta  Relative_time  ACK_Relative_time     TCP_seq     TCP_ack TCP_flags       RTT
0    1675356369.000976     0.000000       0.000000           0.065545  2580699347           0         S  0.065545
1    1675356369.066522     0.065545       0.065545           0.065887  1605494743  2580699347        SA  0.000342
2    1675356369.066863     0.000342       0.065887                NaN  2580699348  1605494743         A       NaN
3    1675356369.140268     0.073329       0.139292           0.139537  1605494744  2580699384         A  0.000245
    '''
    df = df.sort_values(by=['Relative_time'])
    print (df.head(50))

    return (df)

def f_duplicate (df):
    f_df = df
    f_df['Duplicate'] = f_df['TCP_ack'].duplicated()
    
    
    return ()


# ///////// BEGIN 
os.system('clear')

v_file = '/Users/canobhu/Downloads/pcap_long.csv'

v_df = pd.read_csv (v_file)

v_df = f_df_formating (v_df)
v_unique = f_unique (v_df)

v_rtt = f_rtt (v_df,v_unique)


v_rtt.to_csv ('/Users/canobhu/Downloads/rtt.csv',index=False)

#v_plot = v_rtt[['TCP_seq','RTT','Relative_time']]
#v_plot.plot (kind ='scatter', x='Relative_time', y='RTT')
plt.show()

# ///////// END

