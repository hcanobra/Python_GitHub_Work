#!/usr/bin/env python3

import sys
# adding Folder_2 to the system path
sys.path.append('/storage/emulated/0/Documents/Pydroid3/site-packages')


# capture.py
import os, signal
from multiprocessing import Process
import time
import datetime
import pyshark
import pandas as pd
import numpy as np
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

class pcap_capture:
    '''
    Class description:
    This class does all the magic, it initiates the interface and the pcap filter characteristics 
    the filter executes the frame during the pyshark capture, another function processes the frames 
    and sends the frame data to be processed later somewhere, this can be PostgreSQL, Prometheus or MongoDB.
    '''
    def __init__(self):
        self.v_host = '15.181.163.0'
        self.iface_name = 'wlan0'
        self.filter_string = f'host {self.v_host}'  # --> It concatenates the word "host" and the host IP address
                                                    # --> this will be used for pyshark capture filter
        self.capture = pyshark.LiveCapture(
                                    interface=self.iface_name,
                                    bpf_filter=self.filter_string
                                    )
    
    def ping_pcap (self):
        '''
        Function description:
        This function captures the frames from the wire and scrubs the frame looking for selected
        fields, those fields are the only relevant to calculate the RTT information for all
        network elements from point A ---> Z on the traceroute.
        '''
        
        self.pkt_inf = {}
        
        for self.packet in self.capture.sniff_continuously():           # --> This "For-loop" captures each packet from the wire
                                                                        # --> and sends it for scrub and processing
            self.pkt_inf['Time'] = self.packet.frame_info.time_epoch
            self.pkt_inf['host'] = self.packet.ip.dst
            self.pkt_inf['dest'] = self.packet.ip.src
            self.pkt_inf['length'] = self.packet.length
            self.pkt_inf['ttl'] = self.packet.ip.ttl
            self.pkt_inf['Type'] = self.packet.icmp.type
            
            if hasattr(self.packet.icmp, 'resptime'):                   # --> This "IF" function evaluates if there is a value on the 
                                                                        # --> argument "resptime' inside the frame, this will indicate
                                                                        # --> the value of RTT
                self.pkt_inf['RTT'] = self.packet.icmp.resptime
            else:
                self.pkt_inf['RTT'] = np.nan
            
            
            self.pkt_process ()         # ---> Calls for a function to process the frame, this can be PostgreSQL,
                                        # ---> Prometheus or MongoDB
            
        return ()
    
    # THIS FUNCITON WILL PROCESS EACH PACKET, THIS CAN BE DF, PostgreSQL, Prometheus or MongoDB
    def pkt_process (self):
        '''
        Function description:
        This function is the repository where the relevant data from the PCAP frames lands
        at this time I am just doing a basic print. I can integrate this function to load 
        the frame information to a PostgreSQL, Prometheus or MongoDB data bases.
        '''
        
        print (self.pkt_inf)
        
        v_time_stamps.v_end_time = datetime.datetime.now()
        
        return

def func1_f_packet_capture ():
    '''
    Function description:
    Process 1 main function, it initiates pyshark global variables initiates the PCAP capture
    '''
    pkt = pcap_capture()        # Initiate Class, the purpose is just to load the interface configuration,
                                # this improves performance during the packet capture.
    
    pkt.ping_pcap()             # Calls the function ping_pcap, this function will collect the icmp data from the
                                # icmp frame as they arrive on the wire
                                
    return ()

def func2_ICMP ():
    '''
    Function description:
    This function automates the ICMP (ping) process
    '''
    time.sleep(3)
    
    for _ in range(6000):       # --> This value defines the length of the test, 6000 = 10 min (10 pings = 1 sec) this is as a result of interval 0.1
        subprocess.run(["ping", "15.181.163.0", "-s", "1472", "-c", "1", "-i", "0.1"], stdout=subprocess.DEVNULL)
                        #              |                 |           |            |
                        #              |                 |           |            o-----------> Interval of the ping 0.1 = 1-e10 of a second
                        #              |                 |           o------------------------> Number of frames sent to the wire, the length of the test will be 
                        #              |                 |                                      defined on the "For-loop" above.
                        #              |                 o------------------------------------> MTU size
                        #              o------------------------------------------------------> Destination IP for ICMP packets
                        
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
    f_terminate_process()
    
    return

def f_terminate_process():
    '''
    Function description:
    This function will look for process IDs named 'tshark' and 'dumpcap'
    and will terminate them, this will be done after the test cycle is over
    there eis a buffer time between the end of the test and the kill process
    this will allow the last frames to arrive and being processed.
    '''
    
    # Name of process to be killed  
    v_process = ['tshark','dumpcap']
    
    try:
        # iterating through each instance of the process
        for process_name in v_process:
            for line in os.popen("ps ax | grep " + process_name + " | grep -v grep"):
                fields = line.split()
                
                # extracting Process ID from the output
                pid = fields[0]
                
                # terminating process
                os.kill(int(pid), signal.SIGKILL)
        print ("----- > pyshark process successfully terminated....")
        print ("###################################################")
        
    except Exception:
        print("Error Encountered while running script")


# ==> BEGINNING
os.system('clear')

'''
====> This section defines how many test cycles will be run
'''
v_times = 1

os.system('clear')
v_time_stamps = pcap_times()    # Initiating the class

for _ in range(v_times):
    
    if __name__ == '__main__':
        p1 = Process(target=func1_f_packet_capture)
        p1.start()
        #p2 = Process(target=func2_ICMP)
        #p2.start()
        p1.join()
        #p2.join()
        
# ==> END