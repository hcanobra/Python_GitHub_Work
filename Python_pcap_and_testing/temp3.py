
import pandas as pd
import os
import re


# ///////// BEGIN 

path = "/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/iperf3_tcp/"
file = 'data-1672179615203.csv'
file = path+file

df = pd.read_csv (file)

print (df)


v_options = df['TCP_TSval_TSecr']


v_options = v_options.str.split(re.compile(r"\(([^()]+)\)"), regex=True, expand=True)
v_options = v_options[[5,11]]

print (v_options.head(9))


v_options = v_options.rename(columns={5:'TSVal_TSecr',11:'SAck'})


print (v_options.head(9))

'''
for items, values in v_options.items():
    
    
    try: 
        df['TSVal_TSecr'] = values.options[2][1] if 'Timestamp' in values.options[2][0] else None

    except:
        None
       
print (df.info())
 


try:                
    l4_proto_SAck = tcp_pkt_sc.options[5][1] if 'Timestamp' in tcp_pkt_sc.options[5][0] else None

except:
    None

'''        

        
# // END 