import re
import time

# Define data
mServiceState = '''
    mServiceState={mVoiceRegState=0(IN_SERVICE), mDataRegState=0(IN_SERVICE), mChannelNumber=66536, duplexMode()=1, mCellBandwidths=[20000, 20000, 20000, 20000, 10000], mOperatorAlphaLong=Verizon , mOperatorAlphaShort=Verizon , isManualNetworkSelection=false(automatic), getRilVoiceRadioTechnology=14(LTE), getRilDataRadioTechnology=14(LTE), mCssIndicator=unsupported, mNetworkId=*1, mSystemId=*1, mCdmaRoamingIndicator=-1, mCdmaDefaultRoamingIndicator=-1, VoiceRegType=0, Snap=0, MobileData=IN_SERVICE, MobileDataRoamingType=home, MobileDataRat=LTE_CA, PsOnly=true, FemtocellInd=0, SprDisplayRoam=false, OptRadioTech=0, MsimSubmode=0, mIsEmergencyOnly=false, isUsingCarrierAggregation=false, mArfcnRsrpBoost=0, mNetworkRegistrationInfos=[NetworkRegistrationInfo{ domain=CS transportType=WWAN registrationState=HOME roamingType=NOT_ROAMING accessNetworkTechnology=LTE rejectCause=0 emergencyEnabled=false availableServices=[VOICE,SMS,VIDEO] cellIdentity=CellIdentityLte:{ mCi=7*****68 mPci=423 mTac=3**4 mEarfcn=66536 mBands=[66] mBandwidth=2147483647 mMcc=311 mMnc=480 mAlphaLong=Verizon Wireless mAlphaShort=VzW mAdditionalPlmns={} mCsgInfo=null} voiceSpecificInfo=VoiceSpecificRegistrationInfo { mCssSupported=false mRoamingIndicator=0 mSystemIsInPrl=0 mDefaultRoamingIndicator=0} dataSpecificInfo=null nrState=**** rRplmn=311480 isUsingCarrierAggregation=false}, NetworkRegistrationInfo{ domain=PS transportType=WWAN registrationState=HOME roamingType=NOT_ROAMING accessNetworkTechnology=LTE rejectCause=0 emergencyEnabled=false availableServices=[DATA] cellIdentity=CellIdentityLte:{ mCi=7*****68 mPci=423 mTac=3**4 mEarfcn=66536 mBands=[66] mBandwidth=2147483647 mMcc=311 mMnc=480 mAlphaLong=Verizon Wireless mAlphaShort=VzW mAdditionalPlmns={} mCsgInfo=null} voiceSpecificInfo=null dataSpecificInfo=android.telephony.DataSpecificRegistrationInfo :{ maxDataCalls = 16 isDcNrRestricted = false isNrAvailable = true isEnDcAvailable = true LteVopsSupportInfo :  mVopsSupport = 2 mEmcBearerSupport = 2 } nrState=**** rRplmn=311480 isUsingCarrierAggregation=false}], mNrFrequencyRange=0, mOperatorAlphaLongRaw=Verizon Wireless, mOperatorAlphaShortRaw=VzW, mIsDataRoamingFromRegistration=false, mIsIwlanPreferred=false}
        '''


v_split = (re.findall('([A-zA-Z]\w*=[0-9]\d*)', mServiceState))

print (v_split)
for i in v_split:
    print (i)
    
    
v_split = (re.findall('([A-zA-Z]\w*=[[].{2,33}[]])', mServiceState))


for i in v_split:
    print (i)
    
    