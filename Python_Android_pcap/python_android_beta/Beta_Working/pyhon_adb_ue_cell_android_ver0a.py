import re
import time
import sys
import warnings
import pandas as pd
import os

import subprocess

warnings.simplefilter(action='ignore', category=FutureWarning)


def f_ue_location():
    '''
    dumpsys location | grep last 
    '''
    v_df = pd.DataFrame (columns=['Time','Loc'])
    
    
    v_dir = '/Users/hcanobra/Documents/GitHub_Repository/GitHub_Could_Projects/Python_GitHub_Work/Python_Android_pcap/platform-tools/./adb shell '
    mCellInfo = 'dumpsys location | grep location=Location | grep fused'
    v_Location= subprocess.Popen(v_dir+mCellInfo, shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8').splitlines()
        
    v_split = (re.findall('[0-9]*\d.a?[0-9]*\d,-a?[0-9]*\d.a?[0-9]*\d', v_Location[0]))
    
    
    v_df['Loc'] = v_split
    v_df['Time'] = time.time()

    return (v_df)

def f_ue_SignalStrength():

    '''
    dumpsys telephony.registry | grep mSignalStrength=SignalStrength:
    '''
    # Define data

    v_dir = '/Users/hcanobra/Documents/GitHub_Repository/GitHub_Could_Projects/Python_GitHub_Work/Python_Android_pcap/platform-tools/./adb shell '
    mSignalStrength = 'dumpsys telephony.registry | grep mSignalStrength=SignalStrength:'
    v_mSignalStrength, null  = subprocess.Popen(v_dir+mSignalStrength, shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8').splitlines()
        
    '''
    mSignalStrength=
        SignalStrength:
            {
                mCdma=
                    Invalid,
                    mGsm=Invalid,
                    mWcdma=Invalid,
                    mTdscdma=Invalid,
                    mLte=CellSignal
                    StrengthLte: 
                        rssi=-51 
                        rsrp=-75 
                        rsrq=-6 
                        rssnr=26 
                        cqiTableIndex=2147483647 
                        cqi=2147483647 
                        ta=2147483647 
                        level=4 
                        parametersUseForLevel=0,
                        mNr=Invalid,
                        SignalBarInfo
                            { 
                                lteLevel=5 
                            },
                        rat=14,
                        primary=CellSignal
                        StrengthLte
            }

    '''    
    
    v_split = (re.findall('[a-zA-Z]\w*=[-]*[0-9]\d*', v_mSignalStrength))
        
    v_kpi_fields =[
                    'rssi',
                    'rsrp',
                    'rsrq',
                    'rssnr',
                    'lteLevel',
                    'rat'
                    ]

    v_kpi_values = [i for i in v_split if i.split('=')[0] in v_kpi_fields]
    
    v_kpi_list = [i.split('=') for i in v_kpi_values]
    
    v_df = pd.DataFrame(v_kpi_list).transpose()
    v_df = pd.DataFrame(v_df.values[1:], columns=v_df.iloc[0])
        
    return (v_df)

def f_mServiceState():

    '''
    dumpsys telephony.registry | grep mServiceState=

    '''
    v_dir = '/Users/hcanobra/Documents/GitHub_Repository/GitHub_Could_Projects/Python_GitHub_Work/Python_Android_pcap/platform-tools/./adb shell '
    mServiceState = 'dumpsys telephony.registry | grep mServiceState='
    v_kpi_mServiceState, null = subprocess.Popen(v_dir+mServiceState, shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8').splitlines()


    #print (v_kpi_mServiceState)

    '''
    mServiceState=
                    {mVoiceRegState=0(IN_SERVICE),                          # ----> INCLUDED
                    mDataRegState=0(IN_SERVICE),                            # ----> INCLUDED
                    mChannelNumber=66536,                                   # ----> INCLUDED
                    duplexMode()=1, 
                    mCellBandwidths=[20000, 20000, 20000, 20000, 10000],    # ----> INCLUDED
                    mOperatorAlphaLong=Verizon , 
                    mOperatorAlphaShort=Verizon , 
                    isManualNetworkSelection=false(automatic), 
                    getRilVoiceRadioTechnology=14(LTE), 
                    getRilDataRadioTechnology=14(LTE), 
                    mCssIndicator=unsupported, 
                    mNetworkId=*1, 
                    mSystemId=*1, 
                    mCdmaRoamingIndicator=-1, 
                    mCdmaDefaultRoamingIndicator=-1, 
                    VoiceRegType=0, 
                    Snap=0, 
                    MobileData=IN_SERVICE,                                  
                    MobileDataRoamingType=home, 
                    MobileDataRat=LTE_CA, 
                    PsOnly=true, 
                    FemtocellInd=0, 
                    SprDisplayRoam=false, 
                    OptRadioTech=0, 
                    MsimSubmode=0, 
                    mIsEmergencyOnly=false, 
                    isUsingCarrierAggregation=false, 
                    mArfcnRsrpBoost=0,
                    mNetworkRegistrationInfos=
                        [NetworkRegistrationInfo
                            {
                                domain=CS 
                                transportType=WWAN 
                                registrationState=HOME 
                                roamingType=NOT_ROAMING 
                                accessNetworkTechnology=LTE 
                                rejectCause=0 
                                emergencyEnabled=false 
                                availableServices=[VOICE,SMS,VIDEO] 
                                cellIdentity=
                                CellIdentityLte:
                                    {
                                        mCi=7*****68 
                                        mPci=423                        # ----> INCLUDED
                                        mTac=3**4 
                                        mEarfcn=66536                   # ----> INCLUDED
                                        mBands=[66]                     # ----> INCLUDED
                                        mBandwidth=2147483647 
                                        mMcc=311                        # ----> INCLUDED
                                        mMnc=480                        # ----> INCLUDED
                                        mAlphaLong=Verizon Wireless 
                                        mAlphaShort=VzW 
                                        mAdditionalPlmns={} 
                                        mCsgInfo=null
                                    } 
                                voiceSpecificInfo=VoiceSpecificRegistrationInfo 
                                    { 
                                        mCssSupported=false 
                                        mRoamingIndicator=0 
                                        mSystemIsInPrl=0 
                                        mDefaultRoamingIndicator=0
                                    } 
                                        dataSpecificInfo=null 
                                        nrState=**** 
                                        rRplmn=311480                   
                                        isUsingCarrierAggregation=false
                                    }, 
                                NetworkRegistrationInfo
                                    { 
                                        domain=PS transportType=WWAN registrationState=HOME roamingType=NOT_ROAMING accessNetworkTechnology=LTE 
                                                                                                                    rejectCause=0 
                                                                                                                    emergencyEnabled=false availableServices=[DATA] cellIdentity=
                                                                                                                    CellIdentityLte:
                                                                                                                        { 
                                                                                                                            mCi=7*****68 
                                                                                                                            mPci=423 
                                                                                                                            mTac=3**4 
                                                                                                                            mEarfcn=66536 
                                                                                                                            mBands=[66] 
                                                                                                                            mBandwidth=2147483647 
                                                                                                                            mMcc=311 
                                                                                                                            mMnc=480 
                                                                                                                            mAlphaLong=Verizon 
                                                                                                                            Wireless 
                                                                                                                            mAlphaShort=VzW 
                                                                                                                            mAdditionalPlmns={} 
                                                                                                                            mCsgInfo=null
                                                                                                                        }
                                                                                                                    voiceSpecificInfo=null dataSpecificInfo=android.telephony.DataSpecificRegistrationInfo :
                                                                                                                        { 
                                                                                                                            maxDataCalls = 16 
                                                                                                                            isDcNrRestricted = false 
                                                                                                                            isNrAvailable = true 
                                                                                                                            isEnDcAvailable = true 
                                                                                                                            LteVopsSupportInfo :  
                                                                                                                                mVopsSupport = 2 
                                                                                                                                mEmcBearerSupport = 2 
                                                                                                                        } 
                                                                                                                            nrState=**** 
                                                                                                                            rRplmn=311480 
                                                                                                                            isUsingCarrierAggregation=false
                                    }
                        ], 
                    mNrFrequencyRange=0, 
                    mOperatorAlphaLongRaw=Verizon Wireless, 
                    mOperatorAlphaShortRaw=VzW, 
                    mIsDataRoamingFromRegistration=false, 
                    mIsIwlanPreferred=false
                    }
    
    '''


    v_split_1 = (re.findall('([A-zA-Z]\w*=[0-9]\d*)', v_kpi_mServiceState))

    v_split_2 = (re.findall('([A-zA-Z]\w*=[[].{2,33}[]])', v_kpi_mServiceState))

    v_split = v_split_1+v_split_2
    v_kpi_fields =['mVoiceRegState',
                    'mDataRegState',
                    'mChannelNumber',
                    'mPci',
                    'mEarfcn',
                    'mCellBandwidths',
                    'mBands'
                    ]

    v_kpi_values = [i for i in v_split if i.split('=')[0] in v_kpi_fields]
    
    v_kpi_list = [i.split('=') for i in v_kpi_values]
    
    v_df = pd.DataFrame(v_kpi_list).drop_duplicates().transpose()

    v_df = pd.DataFrame(v_df.values[1:], columns=v_df.iloc[0])
    

    return (v_df)

def f_cell_mServiceState():


    '''
    dumpsys telephony.registry | grep mCellInfo=
    '''
    
    v_dir = '/Users/hcanobra/Documents/GitHub_Repository/GitHub_Could_Projects/Python_GitHub_Work/Python_Android_pcap/platform-tools/./adb shell '
    mCellInfo = 'dumpsys telephony.registry | grep mCellInfo='
    mCellInfo, null = subprocess.Popen(v_dir+mCellInfo, shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8').splitlines()

    '''
    mCellInfo=
        [
            CellInfoLte:
                {
                    mRegistered=YES 
                    mTimeStamp=81972791008779ns 
                    mCellConnectionStatus=0 
                    CellIdentityLte:
                        { 
                            mCi=7*****68 
                            mPci=423 
                            mTac=3**4 
                            mEarfcn=66536 
                            mBands=[66] 
                            mBandwidth=2147483647 
                            mMcc=311 
                            mMnc=480 
                            mAlphaLong=Verizon  
                            mAlphaShort=VzW 
                            mAdditionalPlmns={} 
                            mCsgInfo=null
                        } 
                    CellSignalStrengthLte: 
                        rssi=-51 
                        rsrp=-75 
                        rsrq=-9 
                        rssnr=2147483647 
                        cqiTableIndex=2147483647 
                        cqi=2147483647 
                        ta=0 
                        level=4 
                        parametersUseForLevel=0 
                        android.telephony.CellConfigLte :
                            { 
                            isEndcAvailable = false 
                            }
                }, 
            CellInfoLte:
                {
                    mRegistered=NO 
                    mTimeStamp=81972791008779ns 
                    mCellConnectionStatus=0 
                    CellIdentityLte:
                        { 
                            mCi=2147483647 
                            mPci=423 
                            mTac=2147483647 
                            mEarfcn=975 
                            mBands=[2] 
                            mBandwidth=2147483647 
                            mMcc=null 
                            mMnc=null 
                            mAlphaLong= 
                            mAlphaShort= 
                            mAdditionalPlmns={} 
                            mCsgInfo=null
                        } 
                    CellSignalStrengthLte: 
                        rssi=-53 
                        rsrp=-68 
                        rsrq=-6 
                        rssnr=2147483647 
                        cqiTableIndex=2147483647 
                        cqi=2147483647 
                        ta=0 
                        level=4 
                        parametersUseForLevel=0 
                        android.telephony.CellConfigLte :
                            { 
                                isEndcAvailable = false 
                            }
                }
        ]
    '''

    mCellInfo= mCellInfo.split('CellInfoLte:')

    v_split_1 = (re.findall('([A-zA-Z]\w*=[0-9]\d*)', mCellInfo[1]))

    v_split = (re.findall('[A-zA-Z]\w*=[-a?]*\d*[0-9]\d*', mCellInfo[1]))

    #v_split = v_split_1+v_split_2

    v_kpi_fields =[
                    'mPci',
                    'mEarfcn',
                    'rssi',
                    'rsrp',
                    'rsrq'
                    ]

    v_kpi_values = [i for i in v_split if i.split('=')[0] in v_kpi_fields]

    v_kpi_list = [i.split('=') for i in v_kpi_values]

    v_kpi_list_col_names = [v_kpi_list[i][0] for i in range(len(v_kpi_list))]

    v_kpi_lst = {}

    for i in v_kpi_list:   
        for vkpi in v_kpi_list:

            if vkpi[0] == i[0]:
                v_kpi_lst[vkpi[0]] = vkpi[1]


    v_df = pd.DataFrame (data=v_kpi_list)


    v_df = pd.DataFrame(v_kpi_list).drop_duplicates().transpose()

    v_df = pd.DataFrame(v_df.values[1:], columns=v_df.iloc[0])

    #print (v_df)

    return (v_df)
    

v_new_loc = ''
v_ue_info_df = pd.DataFrame ()

while True:
    

    time.sleep(1)
    v_location = f_ue_location()

    if v_location['Loc'].item() != v_new_loc:
        print ('#########################')
        print ("# ------- New Data point ... ")
        v_location = f_ue_location()
        v_services = f_mServiceState()
        v_ue = f_ue_SignalStrength()            
        v_cell =f_cell_mServiceState()
        v_ue_info_df = pd.concat([v_location,v_services,v_ue,v_cell],axis=1)
        
        
        if not os.path.isfile('android.csv'):

            v_ue_info_df.to_csv('android.csv', index=False, header=v_ue_info_df.columns)

        else: # else it exists so append without mentioning the header

            v_ue_info_df.to_csv('android.csv', mode='a', index=False, header=False)
        
        
        #v_ue_info_df.to_csv('/Users/hcanobra/Documents/GitHub_Repository/GitHub_Could_Projects/Python_GitHub_Work/Python_Android_pcap/android.csv', mode='a', index=False, header=v_ue_info_df.columns)
        
        v_new_loc = v_location['Loc'].item()

        print (v_ue_info_df)
        
        print ('#########################')
    
