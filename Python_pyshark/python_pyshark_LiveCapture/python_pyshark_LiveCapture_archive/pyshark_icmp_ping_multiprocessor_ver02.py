#!/usr/bin/env python3
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
    def __init__(self):
        self.v_start_time = datetime.datetime.now()
        self.v_end_time = datetime.datetime.now()

class pcap_capture:
    def __init__(self):
        self.v_host = '15.181.163.0'
        self.iface_name = 'en0'
        self.filter_string = 'host '+self.v_host
        self.capture = pyshark.LiveCapture(
                                    interface=self.iface_name,
                                    bpf_filter=self.filter_string
                                    )
    
    def ping_pcap (self):
        
        self.pkt_inf = {}

        for self.packet in self.capture.sniff_continuously():
            self.pkt_inf['Time'] = self.packet.frame_info.time_epoch
            self.pkt_inf['host'] = self.packet.ip.dst
            self.pkt_inf['dest'] = self.packet.ip.src
            self.pkt_inf['length'] = self.packet.length
            self.pkt_inf['ttl'] = self.packet.ip.ttl
            self.pkt_inf['Type'] = self.packet.icmp.type
            if hasattr(self.packet.icmp, 'resptime'):
                self.pkt_inf['RTT'] = self.packet.icmp.resptime
            else:
                self.pkt_inf['RTT'] = np.nan

            # This section is a way to place the informaiton from the frame into a Pandas data frame
            # the problem is that the DF increments in size.
            '''
            self.df1 = pd.DataFrame([])     # --- > If I want to use Pandas DF instead I need to move this declaration at the begining of the function
            self.df2 = pd.DataFrame([])     # --- > If I want to use Pandas DF instead I need to move this declaration at the begining of the function

            self.df2 = pd.DataFrame ({
                                'Time': self.packet.frame_info.time_epoch,
                                'host': self.packet.ip.dst,
                                'dest': self.packet.ip.src,
                                'length': self.packet.length,
                                'ttl': self.packet.ip.ttl,
                                'Type': self.packet.icmp.type
                                }, index=[0])
            if hasattr(self.packet.icmp, 'resptime'):
                self.df2['RTT'] = self.packet.icmp.resptime
            
            self.df1 = pd.concat([self.df1,self.df2],axis=0)
            '''

            self.pkt_process ()

        return ()

    # THIS FUNCITON WILL PROCESS EACH PACKET, THIS CAN BE DF, PostgreSQL, Prometheus or MongoDB
    def pkt_process (self):
        
        print (self.pkt_inf)

        v_time_stamps.v_end_time = datetime.datetime.now()

        return

def func1_f_packet_capture ():

    pkt = pcap_capture()

    pkt.ping_pcap()

    return ()

def func2_ICMP ():
    time.sleep(3)

    for times in range(300):
        subprocess.run(["ping", "15.181.163.0", "-s", "1472", "-c", "1", "-i", "0.1"], stdout=subprocess.DEVNULL)

    v_end_icmp = datetime.datetime.now()
    
    time.sleep(2)

    print ("Process started @:  ",v_time_stamps.v_start_time)
    print ("ICMP ended @:       ",v_end_icmp)
    print ("Test lasted:        ",v_end_icmp - v_time_stamps.v_start_time)    
    
    f_terminate_process()

    return

def f_terminate_process():

    # Ask user for the name of process    
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
        print("Process Successfully terminated")
         
    except:
        print("Error Encountered while running script")
    

os.system('clear')
v_time_stamps = pcap_times()    # Initiating the class

if __name__ == '__main__':

    p1 = Process(target=func1_f_packet_capture)
    p1.start()
    p2 = Process(target=func2_ICMP)
    p2.start()
    p1.join()
    #p2.join()

    p1.terminate()