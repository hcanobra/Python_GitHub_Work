#!/usr/bin/env python3.7

import contextlib
import os
import sys
from multiprocessing import Process
import time
import numpy as np

import pyshark
import nest_asyncio

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
    try: 
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
                    
                    
                    #p3 = Process(target=f_adb_rf)
                    #p3.start()
                    
                    print (pkt_inf)
        
        print ('======> Not android application running <======')
        
    except Exception:
        pass

def f_adb_rf():
    print ('P3 sarted')
    
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

