import re
import time


'''
dumpsys telephony.registry | grep mSignalStrength=SignalStrength:


'''
# Define data
mServiceState = '''
    mSignalStrength=SignalStrength:{mCdma=Invalid,mGsm=Invalid,mWcdma=Invalid,mTdscdma=Invalid,mLte=CellSignalStrengthLte: rssi=-51 rsrp=-77 rsrq=-9 rssnr=26 cqiTableIndex=2147483647 cqi=2147483647 ta=2147483647 level=4 parametersUseForLevel=0,mNr=Invalid,SignalBarInfo{ lteLevel=5 },rat=14,primary=CellSignalStrengthLte}
    mSignalStrength=SignalStrength:{mCdma=Invalid,mGsm=Invalid,mWcdma=Invalid,mTdscdma=Invalid,mLte=Invalid,mNr=Invalid,SignalBarInfo{ no level },rat=14,primary=CellSignalStrengthLte}
        '''


v_split = (re.findall('[a-zA-Z]\w*=[-]*[0-9]\d*', mServiceState))

print (v_split)
for i in v_split:
    print (i)
    