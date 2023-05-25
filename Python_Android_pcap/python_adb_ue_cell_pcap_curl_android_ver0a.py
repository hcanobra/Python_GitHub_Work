#!/usr/bin/env python3.7

import contextlib
import os
import sys
from multiprocessing import Process
import time
import numpy as np

import pyshark
import nest_asyncio

import re
import warnings
import pandas as pd

import subprocess

warnings.simplefilter(action='ignore', category=FutureWarning)


v_work_dir = os.path.dirname(__file__)
v_adb_dir = f'{v_work_dir}/platform-tools/'

def f_curl():
    try:
        print ('#######################################')
        print ('# Proc1 => Started ....               #')
        print ('#######################################')
        
        print ('---> Creating temporary PCAP file  ... ')
        os.system(
                    f'{v_adb_dir}./adb shell curl -NLs http://127.0.0.1:8080  > {v_work_dir}/android.pcap'
            )
        
        print ('---> Capture ended, cleaning temporary files ... ')
        os.system(
            f'rm {v_work_dir}/android.pcap'
        )
    except:
        pass        

def f_pcap():
    time.sleep(3)
    print ('#######################################')
    print ('# Proc2 => Started ....               #')
    print ('#######################################')

    v_frame_recorded = []
    pkt_inf = {}
    with contextlib.suppress(Exception):
        while os.path.exists(f'{v_work_dir}/android.pcap'):

            cap = pyshark.FileCapture(f'{v_work_dir}/android.pcap') 

            for pkt in cap:
                if pkt.number not in v_frame_recorded:            
                    pkt_inf['Pkt_no'] = pkt.number
                    pkt_inf['Time'] = pkt.frame_info.time_epoch
                    pkt_inf['src'] = pkt.ip.src
                    pkt_inf['dst'] = pkt.ip.dst
                    pkt_inf['length'] = pkt.length
                    pkt_inf['ttl'] = pkt.ip.ttl
                    pkt_inf['Type'] = pkt.icmp.type

                    pkt_inf['RTT'] = pkt.icmp.resptime if hasattr(pkt.icmp, 'resptime') else np.nan

                    v_frame_recorded.append(pkt.number)

                    v_pcap_df = pd.DataFrame(pkt_inf,index=[0])

                    v_location = f_ue_location()
                    v_services = f_mServiceState()
                    v_ue = f_ue_SignalStrength()            
                    v_cell =f_cell_mServiceState()
                    v_ue_info_df = pd.concat([v_pcap_df,v_location,v_services,v_ue,v_cell],axis=1)

                    print (v_ue_info_df)

                    if not os.path.exists(f'{v_work_dir}/android.csv'):

                        v_ue_info_df.to_csv(f'{v_work_dir}/android.csv', index=False, header=v_ue_info_df.columns)

                    else: # else it exists so append without mentioning the header

                        v_ue_info_df.to_csv(f'{v_work_dir}/android.csv', mode='a', index=False, header=False)                    

        print ('======> Not android application running <======')

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
                    'lteLevel'
                    
                    
                    
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
        for h in range(len(v_kpi_list)):
            #print (i[0])
            if v_kpi_list[h][0] == i[0]:
                v_kpi_lst[v_kpi_list[h][0]] = v_kpi_list[h][1]
                #print (v_kpi_list[h][0])
                #print (v_kpi_list[h][1])
            
    v_df = pd.DataFrame (data=v_kpi_list)
    
        
    v_df = pd.DataFrame(v_kpi_list).drop_duplicates().transpose()

    v_df = pd.DataFrame(v_df.values[1:], columns=v_df.iloc[0])
    
    #print (v_df)
    
    return (v_df)

# ==> BEGINNING
os.system('clear')
nest_asyncio.apply()

if __name__ == '__main__':
    p1 = Process(target=f_curl)
    p1.start()
    p2 = Process(target=f_pcap)
    p2.start()
    p1.join()
    p2.join()
        
# ==> END

