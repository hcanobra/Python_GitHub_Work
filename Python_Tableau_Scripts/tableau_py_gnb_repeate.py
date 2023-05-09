SCRIPT_STR(
"
import numpy as np
import pandas as pd

print (_arg1)

v_gnb = []

df = _arg1
for i in df:

    record = i

    df2 = record.split(',')
    df2 = [x.strip(' ') for x in df2]

    # to remove duplicated from list 
    result = [] 
    [result.append(x) for x in df2 if x not in result]

    # printing list after removal 
    #print ('The list after removing duplicates: ' + str(result)) 
    v_gnb.append(result)

#df = v_gnb.tolist()
print (v_gnb)
return (_arg1)
 
",
MIN([LTE_eNB_ID])
)




SCRIPT_REAL(
"
import json
import numpy as np
import pandas as pd

print (_arg1)

df = pd.DataFrame (_arg1)

df = df * 2

#df1 = df.to_numpy()
print (df)

df2 = df[0].tolist()
print (df2)

return (df2)
 
", 
avg([Max_LTE_RSRP])
)