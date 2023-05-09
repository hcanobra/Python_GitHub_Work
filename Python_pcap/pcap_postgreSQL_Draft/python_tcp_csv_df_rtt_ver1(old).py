
# Importing sys
import sys
  
# Adding Folder_2 to the system path
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
    return (f_df)
    
def f_rtt (df):
    f_df = df  
        
    # IMPORTANT NOTE:
    # This section creates a new column named idx_seq,
    # the value in this colum depends on the values of the field TCP_len
    # if TCP_len = 0, the new column will be the value on TCP_seq + 1
    # if TCP_len != 0, the new column will be the value on TCP_seq + TCP_len
    # this new column will be use later to generate the merge function.
    
    f_df.loc[f_df['TCP_len'] == 0, 'idx_seq'] = f_df['TCP_seq'] + 1
    f_df.loc[f_df['TCP_len'] != 0, 'idx_seq'] = f_df['TCP_seq'] + f_df['TCP_len']

#   idx         Relative_time       Frame_Delta     TCP_seq     TCP_len     TCP_ack     TCP_flags       Frame_flow                                                              Source                                  idx_seq
#   1674851985  0                   0               105603878   0           0           S           	Ether / IP / TCP 192.168.0.163:36812 > 15.181.163.0:targus_getdata1 S	tcp_pcap_01272023_00001_20230127133940	105603879
#   1674851985  0.082255            0.082255        3291415077  0	        105603879	SA	            Ether / IP / TCP 15.181.163.0:targus_getdata1 > 192.168.0.163:36812 SA  tcp_pcap_01272023_00001_20230127133940  3291415078
#   |           |                   |               |           |           |           |               |                                                                       |                                       |
#   |           |                   |               |           |           |           |               |                                                                       |                                       o--------> 
#   |           |                   |               |           |           |           |               |                                                                       o------------------------------------------------> 
#   |           |                   |               |           |           |           |               o------------------------------------------------------------------------------------------------------------------------>                                       
#   |           |                   |               |           |           |           o---------------------------------------------------------------------------------------------------------------------------------------->                                       
#   |           |                   |               |           |           o---------------------------------------------------------------------------------------------------------------------------------------------------->                                       
#   |           |                   |               |           o---------------------------------------------------------------------------------------------------------------------------------------------------------------->                                       
#   |           |                   |               o---------------------------------------------------------------------------------------------------------------------------------------------------------------------------->                                        
#   |           |                   o-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->                                        
#   |           o---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->                            
#   o---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->  


    # Creation of the sencod index that will beused on the merge function.
    f_df['idx_ack'] = f_df['TCP_ack']
    f_df.to_csv ('/Users/canobhu/Downloads/f_df.csv',index=False)

    # Reorganize the columns on the dataframe
    f_df = f_df [[
                'Frame_flow',
                'idx_ack',
                'idx_seq',
                'TCP_flags',
                'Relative_time',
                'Frame_Delta',
                'TCP_seq',
                'TCP_len',
                'TCP_ack',
                'Source'
                ]]
    
    # This section creates four teables that will be used in a convination to calculate the RTT    
    # Table 1 using TCP flag "S"
    # Table 2 using TCP flag "SA"
    # Table 3 using TCP flag "A"
    # Table 4 using TCP flag "PA"
    
    f_df_syn = f_df.loc[f_df['TCP_flags'] == "S"]
    f_df_syn_ack = f_df.loc[f_df['TCP_flags'] == "SA"]
    f_df_ack = f_df.loc[f_df['TCP_flags'] == "A"]
    f_df_psh_ack = f_df.loc[f_df['TCP_flags'] == "PA"]

    # This section calls a function "f_merge" passing the tables associated to the combinations:
    # Combination 1 using "S" ---> "SA"
    # Combination 2 using "SA" ---> "A"
    # Combination 3 using "PA" ---> "A"
    
    # Combination 1:
    f_df_a = f_merge (f_df_syn,f_df_syn_ack)
    df.dropna()

    # Combination 2:
    f_df_sa = f_merge (f_df_syn_ack,f_df_ack)

    # Combination 3: 
    f_df_pa = f_merge (f_df_psh_ack,f_df_ack)
    
    # Concatenate all DataFrames, remove NA rows and sort rows by relative value     
    f_df_rtt = pd.concat([f_df_a,f_df_sa,f_df_pa])                          # Concatenate
    f_df_rtt = f_df_rtt.dropna()                                            # Drop NA those records do not have RTT informaiton
    f_df_rtt = f_df_rtt.sort_values(by=['Seq_Relative_time'])               # Sort values
    
    # Calculate RTT values
    f_df_rtt['RTT'] = (f_df_rtt['ACK_Relative_time'] - f_df_rtt['Seq_Relative_time']) * 1000
    
    return (f_df_rtt)

def f_merge (df,df1):
    
    # Create subframe with using Seq number as index.
    f_df_tcp_seq = df [[
                        'Frame_flow',
                        'Relative_time',
                        'Frame_Delta',
                        'TCP_seq',
                        'TCP_len',
                        'TCP_ack',
                        'idx_seq',
                        'Source'
                        ]]
    
    # Rename "idx_seq" column which will be used as the index to merge the DataFrame
    f_df_tcp_seq.rename(
                        columns={
                                "idx_seq": "idx", 
                                "Relative_time": "Seq_Relative_time"
                                },inplace=True
                        )

    # Create subframe with using Ack number as index.
    f_df_tcp_ack = df1 [[
                        'Relative_time',
                        'idx_ack'
                        ]]

    # Drop duplicates and rename colums.
    f_df_tcp_ack = f_df_tcp_ack.drop_duplicates (subset = 'idx_ack')
    f_df_tcp_ack.rename(
                        columns={
                                "idx_ack": "idx", 
                                "Relative_time": "ACK_Relative_time"
                                },inplace=True
                        )
    
    # Merge function.
    df_merge = pd.merge(left=f_df_tcp_seq, right=f_df_tcp_ack, how='right')
    
    # Select the columns of relevance.
    df_merge = df_merge[[
                        'Frame_flow',
                        'TCP_seq',
                        'TCP_ack',
                        'ACK_Relative_time',
                        'Seq_Relative_time',
                        'Frame_Delta',
                        'Source'
                        ]]
    
#    Frame_flow       TCP_seq    TCP_ack     ACK_Relative_time       Seq_Relative_time       Frame_Delta         Source
#    |                |          |           |                       |                       |                   |
#    |                |          |           |                       |                       |                   o--------> 
#    |                |          |           |                       |                       o----------------------------> 
#    |                |          |           |                       o---------------------------------------------------->
#    |                |          |           o---------------------------------------------------------------------------->
#    |                |          o---------------------------------------------------------------------------------------->
#    |                o--------------------------------------------------------------------------------------------------->
#    o-------------------------------------------------------------------------------------------------------------------->

    return (df_merge)


# ///////// BEGIN 
os.system('clear')



# Data source reference, in this case comming from a CSV File
v_file = '/Users/canobhu/Downloads/pcap_tables_tcp_02122023.csv'

# Open the file with Pandas as DataFrame
v_df = pd.read_csv (v_file)

# Apply some formanting on the DF, replacing NA's with 0 and changing datatypes
v_df = f_df_formating (v_df)

# Calculates RTT on frames
v_rtt = f_rtt (v_df)

v_rtt.to_csv ('/Users/canobhu/Downloads/rtt.csv',index=False)

print (v_rtt.describe())
v_plot = v_rtt[['RTT','Seq_Relative_time']]
v_plot.plot (kind ='scatter', x='Seq_Relative_time', y='RTT')
plt.show()

# ///////// END

