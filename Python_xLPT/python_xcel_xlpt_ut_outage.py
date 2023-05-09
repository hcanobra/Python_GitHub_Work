import pandas as pd











v_file = '/Users/canobhu/Downloads/slc_outage.csv'

df = pd.read_csv (v_file)



df['bd_pct'] = (df['Bearer_Setup_Failure%_Num']/df['Bearer_Setup_Failure%_Den'])*100
df['csf_pct'] = (df['Context_Setup_Failure%_Num']/df['Context_Setup_Failure%_Den'])*100

df2 = df[['date_time','ENODEB','bd_pct','csf_pct']]


#print (df2.info())
#print (df2)

df3 = df2[(df2['date_time'] == '03/24/2022 3:30')|(df2['date_time'] == '03/24/2022 4:00')]
df4 = df2[(df2['date_time'] == '03/24/2022 3:00')]

#print (df3)


v_directory = {'date_time' : [], 
               'ENODEB' : [], 
               'target_enb_bd_pct' : [],
               'target_enb_csf_pct' : [],
               'baseline_enb_bd_pct' : [],
               'baseline_enb_csf_pct' : [],
               'bd_pct_delta' : [], 
               'csf_pct_delta' : []}

for target_enb, target_enb_row in df3.iterrows():
    for baseline_enb, baseline_enb_row in df3.iterrows():
        if target_enb_row['ENODEB'] == baseline_enb_row['ENODEB']:
            if target_enb_row['bd_pct'] > baseline_enb_row['bd_pct']:
                
                
                v_bd_pct_delta = ((target_enb_row['bd_pct']*100) / baseline_enb_row['bd_pct'])-100
                v_csf_pct_delta = target_enb_row['csf_pct'] - baseline_enb_row['csf_pct']
                
                v_directory['date_time'].append(target_enb_row['date_time'])
                v_directory['ENODEB'].append(target_enb_row['ENODEB'])
                
                v_directory['target_enb_bd_pct'].append(target_enb_row['bd_pct'])
                v_directory['target_enb_csf_pct'].append(target_enb_row['csf_pct'])              
                v_directory['baseline_enb_bd_pct'].append(baseline_enb_row['bd_pct'])
                v_directory['baseline_enb_csf_pct'].append(baseline_enb_row['csf_pct'])
                
                
                v_directory['bd_pct_delta'].append(v_bd_pct_delta)
                v_directory['csf_pct_delta'].append(v_csf_pct_delta)


#print (v_directory)


v_directory_df = pd.DataFrame(v_directory)

v_directory_df = v_directory_df.sort_values('bd_pct_delta', ascending = False)

v_directory_df.to_csv('/Users/canobhu/Downloads/slc_outage_top.csv')
print (v_directory_df)