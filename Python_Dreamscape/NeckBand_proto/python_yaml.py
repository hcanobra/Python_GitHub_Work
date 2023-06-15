import yaml
import re


mServiceState="""
mServiceState={mVoiceRegState=1(OUT_OF_SERVICE), mDataRegState=1(OUT_OF_SERVICE), mVideoRegState=1(OUT_OF_SERVICE), mChannelNumber=0, duplexMode()=0, mCellBandwidths=[], mOperatorAlphaLong=null, mOperatorAlphaShort=null, isManualNetworkSelection=false(automatic), getRilVoiceRadioTechnology=0(Unknown), getRilDataRadioTechnology=0(Unknown), mCssIndicator=unsupported, mNetworkId=0, mSystemId=0, mCdmaRoamingIndicator=0, mCdmaDefaultRoamingIndicator=0, mIsEmergencyOnly=false, isUsingCarrierAggregation=false, mArfcnRsrpBoost=0, mNetworkRegistrationInfos=[], mNrFrequencyRange=0, mOperatorAlphaLongRaw=null, mOperatorAlphaShortRaw=null, mIsDataRoamingFromRegistration=false, mIsIwlanPreferred=false, mIsCdmaFemtoCell=false, mIsLteFemtoCell=false, mIsOnCsgCell=false, mCsgId=0, mCsgName=null}
"""

adb_input = mServiceState

adb_input = adb_input.replace('={', '\n- ')
adb_input = adb_input.replace('}', '')
adb_input = adb_input.replace(',', '\n-')
yaml_output = yaml.dump(adb_input, sort_keys=False) 
print(yaml_output) 

mSignalStrength="""
mSignalStrength=SignalStrength:{mCdma=CellSignalStrengthCdma: cdmaDbm=2147483647 cdmaEcio=2147483647 evdoDbm=2147483647 evdoEcio=2147483647 evdoSnr=2147483647 level=0,mGsm=CellSignalStrengthGsm: rssi=2147483647 ber=2147483647 mTa=2147483647 mLevel=0,mWcdma=CellSignalStrengthWcdma: ss=2147483647 ber=2147483647 rscp=2147483647 ecno=2147483647 level=0,mTdscdma=CellSignalStrengthTdscdma: rssi=2147483647 ber=2147483647 rscp=2147483647 level=0,mLte=CellSignalStrengthLte: rssi=2147483647 rsrp=2147483647 rsrq=2147483647 rssnr=2147483647 cqiTableIndex=2147483647 cqi=2147483647 ta=2147483647 level=0 parametersUseForLevel=0,mNr=CellSignalStrengthNr:{ csiRsrp = 2147483647 csiRsrq = 2147483647 csiCqiTableIndex = 2147483647 csiCqiReport = [] ssRsrp = 2147483647 ssRsrq = 2147483647 ssSinr = 2147483647 level = 0 parametersUseForLevel = 0 },primary=CellSignalStrengthLte,mMaxLevel=4}
"""
adb_input = mSignalStrength

adb_input = adb_input.replace(' = ', '=')
adb_input = adb_input.replace(':{ ', ':{')
adb_input = adb_input.replace(':{', '\n')
adb_input = adb_input.replace('}', '')
adb_input = adb_input.replace(',', ' ')
adb_input = adb_input.replace('  ', ' ')
adb_input = adb_input.replace(' ', '\n-')


yaml_output = yaml.dump(adb_input, sort_keys=False) 
print(yaml_output) 

mCallQuality="""
    mCallQuality=CallQuality: {downlinkCallQualityLevel=0 uplinkCallQualityLevel=0 callDuration=0 numRtpPacketsTransmitted=0 numRtpPacketsReceived=0 numRtpPacketsTransmittedLost=0 numRtpPacketsNotReceived=0 averageRelativeJitter=0 maxRelativeJitter=0 averageRoundTripTime=0 codecType=0 rtpInactivityDetected=false txSilenceDetected=false rxSilenceDetected=false}
    """
    
    
mCallAttributes="""
    mCallAttributes=mPreciseCallState=Ringing call state: -1, Foreground call state: -1, Background call state: -1, Disconnect cause: -1, Precise disconnect cause: -1 mNetworkType=0 mCallQuality=CallQuality: {downlinkCallQualityLevel=0 uplinkCallQualityLevel=0 callDuration=0 numRtpPacketsTransmitted=0 numRtpPacketsReceived=0 numRtpPacketsTransmittedLost=0 numRtpPacketsNotReceived=0 averageRelativeJitter=0 maxRelativeJitter=0 averageRoundTripTime=0 codecType=0 rtpInactivityDetected=false txSilenceDetected=false rxSilenceDetected=false}
    """
#names = yaml.safe_load(mCallQuality)
#print (names)




