#!/usr/bin/env python3.7

import contextlib
import os
import sys
from multiprocessing import Process
import time
import numpy as np

import pyshark
import nest_asyncio

import pandas as pd

#v_work_dir = os.path.dirname(__file__)
#v_adb_dir = f'{v_work_dir}/platform-tools/'
#v_adb_dir = f'{v_work_dir}'


#import pyhon_adb_ue_cell_android_ver0a as adb_ue

class pcap_curl_android:
    def __init__(self):
        self.v_work_dir = os.path.dirname(__file__)
        self.v_adb_dir = '/Users/hcanobra/Documents/GitHub_Repository/GitHub_Could_Projects/Python_GitHub_Work/Python_Android_pcap/platform-tools/'
        

    def f_curl(self):
        with contextlib.suppress(Exception):
            print ('#######################################')
            print ('# Proc1 => Started ....               #')
            print ('#######################################')

            print ('---> Creating temporary PCAP file  ... ')
            os.system(
                f'{self.v_adb_dir}./adb shell curl -NLs http://127.0.0.1:8080  > {self.v_work_dir}/android.pcap'
            )

            print ('---> Capture ended, cleaning temporary files ... ')
            #os.system(
            #    f'rm {self.v_work_dir}/android.pcap'
            #)        

    def f_pcap(self):
        time.sleep(3)
        print ('#######################################')
        print ('# Proc2 => Started ....               #')
        print ('#######################################')

        self.v_frame_recorded = []
        self.pkt_inf = {}
        
        with contextlib.suppress(Exception):
            while os.path.exists(f'{self.v_work_dir}/android.pcap'):
                
                self.cap = pyshark.FileCapture(f'{self.v_work_dir}/android.pcap') 
                
                for pkt in self.cap:
                    if self.pkt.number not in v_frame_recorded:            
                        self.pkt_inf['Pkt_no'] = pkt.number
                        self.pkt_inf['Time'] = pkt.frame_info.time_epoch
                        self.pkt_inf['src'] = pkt.ip.src
                        self.pkt_inf['dst'] = pkt.ip.dst
                        self.pkt_inf['length'] = pkt.length
                        self.pkt_inf['ttl'] = pkt.ip.ttl
                        self.pkt_inf['Type'] = pkt.icmp.type
                        
                        self.pkt_inf['RTT'] = pkt.icmp.resptime if hasattr(pkt.icmp, 'resptime') else np.nan
                        
                        self.v_frame_recorded.append(pkt.number)
                        
                        self.v_pcap_df = pd.DataFrame(self.kt_inf,index=[0])
                        
                        print (self.v_pcap_df)
                        
                        if not os.path.isfile('android.csv'):
                            
                            self.v_pcap_df.to_csv('python_pcap_android.csv', index=False, header=self.v_ue_info_df.columns)
                            
                        else: # else it exists so append without mentioning the header
                            
                            self.v_pcap_df.to_csv('python_pcap_android.csv', mode='a', index=False, header=False)    
                        
                        
            print ('======> Not android application running <======')
            
    def p_f_curl(self):
        p1 = Process(target=self.f_curl)
        p1.start()
        p1.join()
        


        if __name__ != '__main__':
            p1 = Process(target=self.f_curl)
            p1.start()
            p2 = Process(target=self.f_pcap)
            p2.start()
            #p1.join()
            #p2.join()
                 
    def __main__(self):
        # ==> BEGINNING
        os.system('clear')
        nest_asyncio.apply()
        
        


        if __name__ != '__main__':
            p1 = Process(target=self.f_curl)
            p1.start()
            p2 = Process(target=self.f_pcap)
            p2.start()
            #p1.join()
            #p2.join()
                
        # ==> END

