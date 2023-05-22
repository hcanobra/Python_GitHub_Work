import re
import time

# Define data
mServiceState = '''
    mCellIdentity=CellIdentityLte:{ mCi=7*****68 mPci=423 mTac=3**4 mEarfcn=66536 mBands=[66] mBandwidth=2147483647 mMcc=311 mMnc=480 mAlphaLong=Verizon Wireless mAlphaShort=VzW mAdditionalPlmns={} mCsgInfo=null}
    mBarringInfo=BarringInfo {mCellIdentity=CellIdentityLte:{ mCi=7*****68 mPci=0 mTac=3**4 mEarfcn=0 mBands=[1] mBandwidth=0 mMcc=311 mMnc=480 mAlphaLong= mAlphaShort= mAdditionalPlmns={} mCsgInfo=null}, mBarringServiceInfos={8={isBarred: false (type: 0, isConditionally: false), factor: 0, timeseconds: 0}}}
    mCellIdentity=null
    mBarringInfo=BarringInfo {mCellIdentity=null, mBarringServiceInfos={0={isBarred: false (type: 0, isConditionally: false), factor: 0, timeseconds: 0}, 1={isBarred: false (type: 0, isConditionally: false), factor: 0, timeseconds: 0}, 2={isBarred: false (type: 0, isConditionally: false), factor: 0, timeseconds: 0}, 3={isBarred: false (type: 0, isConditionally: false), factor: 0, timeseconds: 0}, 4={isBarred: false (type: 0, isConditionally: false), factor: 0, timeseconds: 0}, 5={isBarred: false (type: 0, isConditionally: false), factor: 0, timeseconds: 0}, 6={isBarred: false (type: 0, isConditionally: false), factor: 0, timeseconds: 0}, 7={isBarred: false (type: 0, isConditionally: false), factor: 0, timeseconds: 0}, 8={isBarred: false (type: 0, isConditionally: false), factor: 0, timeseconds: 0}, 9={isBarred: false (type: 0, isConditionally: false), factor: 0, timeseconds: 0}}}
        '''


v_split = (re.findall('[a-zA-Z]\w*=[-]*[0-9]\d*', mServiceState))

print (v_split)
for i in v_split:
    print (i)
    