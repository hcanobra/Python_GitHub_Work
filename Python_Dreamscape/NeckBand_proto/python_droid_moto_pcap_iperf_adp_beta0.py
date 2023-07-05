#!/usr/bin/env python3.9

import os
from multiprocessing import Process # install multiprocess
import nest_asyncio
import time
from datetime import date

import subprocess
import re
import pandas as pd

def f_global_definitions():
    v_test_cyles = 4
    v_bw = ['40M','50M','80M','100M']
    v_protocols =  ['TCP','UDP','ICMP']

    # Generating Today's lebel	
    today = date.today()
    v_date = today.strftime("%m%d%y")

    v_adb_dir = f'{os.path.dirname(__file__)}/platform-tools/'
    v_mec_sr_ip = '155.146.162.168'

    return (v_test_cyles,v_bw,today,v_date,v_adb_dir,v_mec_sr_ip,v_protocols)

class iperf3_test:
    def __init__(self,v_test_cyles,v_bw,today,v_date,v_adb_dir,v_mec_sr_ip,v_protocols):
        self.iperf_dir = '/data/./data/com.nextdoordeveloper.miperf.miperf/files/' 
        
        self.v_test_cyles = v_test_cyles
        self.v_bw = v_bw
        self.v_today = today
        self.v_date = v_date
        self.v_adb_dir = v_adb_dir
        self.v_mec_sr_ip = v_mec_sr_ip
        self.v_protocols = v_protocols
        
        self.v_test_duration = 6                       # This value specifies the length of the IPERF Test
        
    def iperf_tcp_start (self,c,b,p):
        v_cycle = c
        v_bw = b
        
        os.system(
        f"{self.v_adb_dir}./adb shell su 0 '{self.iperf_dir}iperf3 -c {self.v_mec_sr_ip} -t {self.v_test_duration} -R -b {v_bw}'>> {self.v_adb_dir}iperf_tcp_{self.v_date}_C{v_cycle}.txt")
        
        os.system(
                f"{self.v_adb_dir}./adb shell su 0 'killall tcpdump'"
                )   
        
        print ("<< ----- End Iperf3 TCP test... ")
        print ('#######################################')
        
    def iperf_icmp_start (self,c,b,p):
        v_cycle = c
        v_bw = b
        
        os.system(
        f"{self.v_adb_dir}./adb shell ping -c 1 -s 1472 -i 0.2 {self.v_mec_sr_ip}>> {self.v_adb_dir}iperf_icmp_{self.v_date}_C{v_cycle}.txt")
        
        os.system(
                f"{self.v_adb_dir}./adb shell su 0 'killall tcpdump'"
                ) 
        
        print ("<< ----- End Iperf3 ICMP test... ")
        print ('#######################################')
        
    def iperf_udp_start (self,c,b,p):
        v_cycle = c
        v_bw = b
        
        os.system(
        f"{self.v_adb_dir}./adb shell su 0 '{self.iperf_dir}iperf3 -u -c {self.v_mec_sr_ip} -t {self.v_test_duration} -R -b {v_bw}'>> {self.v_adb_dir}iperf_udp_{self.v_date}_C{v_cycle}.txt")
        print ("<< ----- End Iperf3 UDP test... ")
        print ('#######################################')

        #s.system(
        #        f"{self.v_adb_dir}./adb shell su 0 'killall tcpdump'"
        #        )  
        
def proc_iperf():
    print ('#######################################')
    print ('# Proc1 => Started .... Iperf3 Test   #')
    print ('#######################################')

    v_test_cyles,v_bw,today,v_date,v_adb_dir,v_mec_sr_ip,v_protocols = f_global_definitions()

    iperf_test = iperf3_test(v_test_cyles,v_bw,today,v_date,v_adb_dir,v_mec_sr_ip,v_protocols)

    for c in range (iperf_test.v_test_cyles):
        for p in iperf_test.v_protocols:
            if p == 'TCP':
                for b in iperf_test.v_bw:
                    time.sleep(5)
                    print ('---- >> Func1: Starting generating TCP IPERF traffic... ')
                    iperf_test.iperf_tcp_start(c+1,b,p)
            elif p =='ICMP':
                    print ('---- >> Func1: Starting generating ICMP IPERF traffic... ')
                    iperf_test.iperf_icmp_start (c+1,b,p)
            elif p == 'UDP':
                for b in iperf_test.v_bw:
                    print ('--- >> Func1: Starting generating UDP IPERF traffic... ')
                    iperf_test.iperf_udp_start(c+1,b,p)
                    
    
    os.system ('killall Python')
        
    return()

class Android_pcap:
    def __init__(self,v_test_cyles,v_bw,today,v_date,v_adb_dir,v_mec_sr_ip,v_protocols):
        self.droid_rep = '/storage/emulated/0/Documents/Dreamscape_Pcap/'
        
        self.v_test_cyles = v_test_cyles
        self.v_bw = v_bw
        self.v_today = today
        self.v_date = v_date
        self.v_adb_dir = v_adb_dir
        self.v_mec_sr_ip = v_mec_sr_ip
        
        self.v_protocols = v_protocols
        
    def start_droind_pcap (self,c,b,p):
        v_cycle = c
        v_bw = b
        v_prot = p
        
        os.system(
                f"{self.v_adb_dir}./adb -s NNKS0F0054 shell su 0 'tcpdump -vv -i any host {self.v_mec_sr_ip} -C 100000000 -w {self.droid_rep}android_{v_prot}_{v_bw}_{self.v_date}_C{v_cycle}.pcap'"
                )
        
        '''
        Usage: tcpdump [-aAbdDefhHIJKlLnNOpqStuUvxX#] [ -B size ] [ -c count ]
		[ -C file_size ] [ -E algo:secret ] [ -F file ] [ -G seconds ]
		[ -i interface ] [ -j tstamptype ] [ -M secret ] [ --number ]
		[ -Q in|out|inout ]
		[ -r file ] [ -s snaplen ] [ --time-stamp-precision precision ]
		[ --immediate-mode ] [ -T type ] [ --version ] [ -V file ]
		[ -w file ] [ -W filecount ] [ -y datalinktype ] [ -z postrotate-command ]
		[ -Z user ] [ expression ]
        '''
    
def proc_pcap ():
    
    print ('#######################################')
    print ('# Proc2 => Started PCAP capture       #')
    print ('#######################################')
    
    v_test_cyles,v_bw,today,v_date,v_adb_dir,v_mec_sr_ip,v_protocols = f_global_definitions()

    tcpdump_cap = Android_pcap(v_test_cyles,v_bw,today,v_date,v_adb_dir,v_mec_sr_ip,v_protocols)

    for c in range (tcpdump_cap.v_test_cyles):
        for p in tcpdump_cap.v_protocols:
            if p == 'TCP':
                for b in tcpdump_cap.v_bw:
                    print ('===== >> Func2: Starting PCAP capture for TCP traffic.. ')
                    tcpdump_cap.start_droind_pcap(c+1,b,p)
            elif p =='ICMP':
                for b in tcpdump_cap.v_bw:
                    print ('===== >> Func2: Starting PCAP capture for ICMP traffic.. ')
                    tcpdump_cap.start_droind_pcap(c+1,b,p)
            elif p == 'UDP':
                for b in tcpdump_cap.v_bw: 
                    print (f"===== >> Func2: NO PCAP generated for UDP traffic at {b}.. ")
                    #iperf_test.iperf_udp_start()


    return()

class adb_ue_info ():
    def __init__ (self):

        # Generating Today's lebel	
        today = date.today()
        self.v_date = today.strftime("%m%d%y")

        self.adb_dir = f'{os.path.dirname(__file__)}/platform-tools/'
        self.iperf_dir = '/data/./data/com.nextdoordeveloper.miperf.miperf/files/' 
        
        self.v_mec_sr_ip = '155.146.162.168'

        self.mSignalStrength = './adb shell dumpsys telephony.registry | grep mSignalStrength=SignalStrength:'
        self.mServiceState = './adb shell dumpsys telephony.registry | grep mServiceState='
        self.mCellInfo = './adb shell dumpsys telephony.registry | grep mCellInfo='

    def f_epoch_time (self):
        
        self.v_epoch  = subprocess.Popen( f"{self.adb_dir}./adb -s NNKS0F0054 shell su 0 'echo $EPOCHREALTIME'", shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8').splitlines()[0]

        return (self.v_epoch)
    
    def f_ue_SignalStrength(self):
        import json
        self.mSignalStrength = subprocess.Popen( self.adb_dir+self.mSignalStrength, shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8').splitlines()[0]
        

        
        #output = subprocess.Popen(self.adb_dir+self.mSignalStrength, shell=True, stdout=subprocess.PIPE)
        #jsonS = json.dumps(output.communicate())
        #print (json.loads(jsonS)['data'])
        
        #data = json.dump(self.mSignalStrength)
        
        self.v_split = (re.findall('[a-zA-Z]\w*=[-]*[0-9]\d*', self.mSignalStrength))
            
        self.v_kpi_fields =[
                        'rssi',
                        'rsrp',
                        'rsrq',
                        'rssnr',
                        'lteLevel'
                        ]

        self.v_kpi_values = [i for i in self.v_split if i.split('=')[0] in self.v_kpi_fields]
        
        self.v_kpi_list = [i.split('=') for i in self.v_kpi_values]
        
        self.v_kpi_list = self.v_kpi_list[2:]
        
        self.v_df = pd.DataFrame(self.v_kpi_list).transpose()
        self.v_df = pd.DataFrame(self.v_df.values[1:], columns=self.v_df.iloc[0])
            
        return (self.v_df)

    def f_mServiceState(self):

        '''
        dumpsys telephony.registry | grep mServiceState=

        '''
        v_dir = '/Users/hcanobra/Documents/GitHub_Repository/GitHub_Could_Projects/Python_GitHub_Work/Python_Android_pcap/platform-tools/./adb shell '
       
        self.kpi_mServiceState = subprocess.Popen(self.adb_dir+self.mServiceState, shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8').splitlines()[0]

        self.v_split_1 = (re.findall('([A-zA-Z]\w*=[0-9]\d*)', self.kpi_mServiceState))

        self.v_split_2 = (re.findall('([A-zA-Z]\w*=[[].{2,33}[]])', self.kpi_mServiceState))

        self. v_split = self.v_split_1+self.v_split_2
        self.v_kpi_fields =[
                        'mPci',
                        'mEarfcn'
                        ]
        
        self.v_kpi_values = [i for i in self.v_split if i.split('=')[0] in self.v_kpi_fields]
        
        self.v_kpi_list = [i.split('=') for i in self.v_kpi_values]
        
        self.v_df = pd.DataFrame(self.v_kpi_list).drop_duplicates().transpose()
        
        self.v_df = pd.DataFrame(self.v_df.values[1:], columns=self.v_df.iloc[0])
        
        return (self.v_df)

    def f_cell_mServiceState(self):
        '''
        dumpsys telephony.registry | grep mCellInfo=
        '''
        
        v_dir = '/Users/hcanobra/Documents/GitHub_Repository/GitHub_Could_Projects/Python_GitHub_Work/Python_Android_pcap/platform-tools/./adb shell '
        self.mCellInfo = subprocess.Popen(self.adb_dir+self.mCellInfo, shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8').splitlines()[0]

        self.mCellInfo= self.mCellInfo.split('CellInfoLte:')

        self.v_split_1 = (re.findall('([A-zA-Z]\w*=[0-9]\d*)', self.mCellInfo[1]))

        self.v_split = (re.findall('[A-zA-Z]\w*=[-a?]*\d*[0-9]\d*', self.mCellInfo[1]))

        self.v_kpi_fields =[
                        'mPci',
                        'rssi',
                        'rsrp',
                        'rsrq'
                        ]

        self.v_kpi_values = [i for i in self.v_split  if i.split('=')[0] in self.v_kpi_fields]

        self.v_kpi_list = [i.split('=') for i in self.v_kpi_values]

        self.v_kpi_list_col_names = [self.v_kpi_list[i][0] for i in range(len(self.v_kpi_list))]
        self.v_kpi_list_col_names= ["Cell_" + sub for sub in self.v_kpi_list_col_names]

        self.v_kpi_lst = {}

        for i in self.v_kpi_list:   
            for vkpi in self.v_kpi_list:
                if vkpi[0] == i[0]:
                    self.v_kpi_lst[vkpi[0]] = vkpi[1]


        self.v_df = pd.DataFrame (data=self.v_kpi_list)

        self.v_df = pd.DataFrame(self.v_kpi_list).drop_duplicates().transpose()

        self.v_df = pd.DataFrame(self.v_df.values[1:], columns=self.v_df.iloc[0])

        self.v_df.columns = self.v_kpi_list_col_names

        return (self.v_df)

def adb_rf():
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    
    while True:
            try:
                ue_info = adb_ue_info()

                v_ue_signal = ue_info.f_ue_SignalStrength()

                v_ue_service = ue_info.f_mServiceState()

                v_cell_service = ue_info.f_cell_mServiceState()

                df = pd.concat([v_ue_signal,v_ue_service,v_cell_service], axis=1)

                df['epoch'] = ue_info.f_epoch_time()

                #print (df)

                if not os.path.isfile (ue_info.adb_dir+'ue_rf_data_adb.csv'):
                    df.to_csv (ue_info.adb_dir+'ue_rf_data_adb.csv',index=False)

                else:
                    df.to_csv (ue_info.adb_dir+'ue_rf_data_adb.csv', mode='a', index=False, header=False)
            except Exception:
                    break       
    
    
    return ()


# ==> BEGINNING
os.system('clear')
nest_asyncio.apply()
time.sleep (1)


if __name__ == '__main__':
    p1 = Process(target=proc_iperf)
    p2 = Process(target=proc_pcap)
    p3 = Process (target=adb_rf)
    
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

# ==> END


