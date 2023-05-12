#!/usr/bin/env python3
# capture.py
import os, signal
import subprocess
from multiprocessing import Process
import time
import datetime
import pyshark
import pandas as pd
import numpy as np


class pcap_times:
    def __init__(self):
        self.v_start_time = datetime.datetime.now()
        self.v_end_time = datetime.datetime.now()

class pcap_capture:
    def __init__(self):
        self.v_host = '15.181.163.0'
        self.v_proto = 'icmp'
        self.iface_name = 'en0'
        self.filter_string = self.v_proto
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

            if self.packet.ip.src == self.v_host:
                print ("you reach the point ...")
                break

            self.pkt_process ()

        return ()

    def pkt_process (self):
        
        print (self.pkt_inf)

        return

def func1_f_packet_capture ():

    pkt = pcap_capture()

    pkt.ping_pcap()

    return ()

def func2_ICMP_trace ():
    time.sleep(3)

    
    v_ttl = 100

    for ttl in range (v_ttl):
        subprocess.run(["ping", "15.181.163.0", "-s", "1472", "-c", "1", "-i 0.1", "-t 1 " , "-m {0}".format(ttl)], stdout=subprocess.DEVNULL)

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
    p2 = Process(target=func2_ICMP_trace)
    p2.start()
    p1.join()
    p2.join()





'''
ping 15.181.163.0 -m 2
usage: ping [-AaDdfnoQqRrv] [-c count] [-G sweepmaxsize]
            [-g sweepminsize] [-h sweepincrsize] [-i wait]
            [-l preload] [-M mask | time] [-m ttl] [-p pattern]
            [-S src_addr] [-s packetsize] [-t timeout][-W waittime]
            [-z tos] host
       ping [-AaDdfLnoQqRrv] [-c count] [-I iface] [-i wait]
            [-l preload] [-M mask | time] [-m ttl] [-p pattern] [-S src_addr]
            [-s packetsize] [-T ttl] [-t timeout] [-W waittime]
            [-z tos] mcast-group
Apple specific options (to be specified before mcast-group or host like all options)
            -b boundif           # bind the socket to the interface
            -k traffic_class     # set traffic class socket option
            -K net_service_type  # set traffic class socket options
            --apple-connect       # call connect(2) in the socket
            --apple-time          # display current time


'''