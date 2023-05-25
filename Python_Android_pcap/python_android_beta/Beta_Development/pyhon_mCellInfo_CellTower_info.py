import re
import time


'''
dumpsys telephony.registry | grep mCellInfo=

'''
# Define data
mServiceState = '''
    mCellInfo=[CellInfoLte:{mRegistered=YES mTimeStamp=68694041640ns mCellConnectionStatus=0 CellIdentityLte:{ mCi=7*****68 mPci=423 mTac=3**4 mEarfcn=66536 mBands=[66] mBandwidth=2147483647 mMcc=311 mMnc=480 mAlphaLong=Verizon  mAlphaShort=VzW mAdditionalPlmns={} mCsgInfo=null} CellSignalStrengthLte: rssi=-51 rsrp=-78 rsrq=-8 rssnr=2147483647 cqiTableIndex=2147483647 cqi=2147483647 ta=0 level=4 parametersUseForLevel=0 android.telephony.CellConfigLte :{ isEndcAvailable = false }}, CellInfoLte:{mRegistered=NO mTimeStamp=68694041640ns mCellConnectionStatus=0 CellIdentityLte:{ mCi=2147483647 mPci=423 mTac=2147483647 mEarfcn=975 mBands=[2] mBandwidth=2147483647 mMcc=null mMnc=null mAlphaLong= mAlphaShort= mAdditionalPlmns={} mCsgInfo=null} CellSignalStrengthLte: rssi=-57 rsrp=-73 rsrq=-7 rssnr=2147483647 cqiTableIndex=2147483647 cqi=2147483647 ta=0 level=4 parametersUseForLevel=0 android.telephony.CellConfigLte :{ isEndcAvailable = false }}, CellInfoLte:{mRegistered=NO mTimeStamp=68694041640ns mCellConnectionStatus=0 CellIdentityLte:{ mCi=2147483647 mPci=423 mTac=2147483647 mEarfcn=55942 mBands=[48] mBandwidth=2147483647 mMcc=null mMnc=null mAlphaLong= mAlphaShort= mAdditionalPlmns={} mCsgInfo=null} CellSignalStrengthLte: rssi=-77 rsrp=-106 rsrq=-9 rssnr=2147483647 cqiTableIndex=2147483647 cqi=2147483647 ta=0 level=1 parametersUseForLevel=0 android.telephony.CellConfigLte :{ isEndcAvailable = false }}, CellInfoLte:{mRegistered=NO mTimeStamp=68694041640ns mCellConnectionStatus=0 CellIdentityLte:{ mCi=2147483647 mPci=423 mTac=2147483647 mEarfcn=55744 mBands=[48] mBandwidth=2147483647 mMcc=null mMnc=null mAlphaLong= mAlphaShort= mAdditionalPlmns={} mCsgInfo=null} CellSignalStrengthLte: rssi=-89 rsrp=-109 rsrq=-10 rssnr=2147483647 cqiTableIndex=2147483647 cqi=2147483647 ta=0 level=1 parametersUseForLevel=0 android.telephony.CellConfigLte :{ isEndcAvailable = false }}]
    mCellInfo=null
        '''


v_split = (re.findall('([A-zA-Z]\w*=[0-9]\d*)', mServiceState))

for i in v_split:
    print (i)
    
    
v_split = (re.findall('([A-zA-Z]\w*=[[].{2,33}[]])', mServiceState))


for i in v_split:
    print (i)
    
    
    
