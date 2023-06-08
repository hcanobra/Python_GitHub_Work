#!/usr/bin/env python3


import platform
import os, signal
import time
import datetime
import pyshark
import pandas as pd
import numpy as np

from multiprocessing import Process
import subprocess

class pcap_times:
    '''
    Class description:
    The purpose of this class is just to declare time stamps as a reference for
    time processing of the test
    '''
    def __init__(self):
        self.v_start_time = datetime.datetime.now()
        self.v_end_time = datetime.datetime.now()


def func2_ICMP ():
    '''
    Function description:
    This function automates the ICMP (ping) process
    '''
    time.sleep(3)
    
    for _ in range(60):       # --> This value defines the length of the test, 6000 = 10 min (10 pings = 1 sec) this is as a result of interval 0.1
        subprocess.run(["ping", "-c", "1", "-s", "1472", "-i", "0.2", "15.181.163.0"], stdout=subprocess.DEVNULL)
        print ("Frame #: ",_+1)
        time.sleep(1)

                        
    # Sets a time when the ICMP test cycle ends, point of reference just to calculate how long it took the test
    v_end_icmp = datetime.datetime.now()
    
    # ---> Process will wait for 2 seconds to alow the las packets to arrive and being processed
    # ---> before pyshark is terminated
    time.sleep(2)
    
    print ("###################################################")
    print ("Process started @:  ",v_time_stamps.v_start_time)
    print ("ICMP ended @:       ",v_end_icmp)
    print ("Test lasted:        ",v_end_icmp - v_time_stamps.v_start_time)
    print ("###################################################")  
    
    time.sleep(2)
    
    # ---> Calls for the function to terminate pyshark
    #f_terminate_process()
    
    return

# ==> BEGINNING
os.system('clear')

'''
====> This section defines how many test cycles will be runsource 
'''
v_times = 1

os.system('clear')
v_time_stamps = pcap_times()    # Initiating the class



for _ in range(v_times):
    
    if __name__ == '__main__':
        p2 = Process(target=func2_ICMP)
        p2.start()
        p2.join()
        
# ==> END
