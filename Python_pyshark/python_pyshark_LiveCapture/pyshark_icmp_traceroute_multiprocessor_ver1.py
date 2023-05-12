#!/usr/bin/env python3
# pyshark_icmp_traceroute_multiprocessor_ver1.py
'''

Those a re the option for the command "PING". I will be using some of them for this script

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
import os, signal
import subprocess
from multiprocessing import Process
import time
import datetime
import pyshark
import pandas as pd
import numpy as np


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
    executes the pyshark, processes the frames and sends the frame data to be processed later somewhere
    this can be PostgreSQL, Prometheus or MongoDB
    '''
    def __init__(self):
        '''
        Function description:
        This function initiates the parameters for the PCAP
        including the destination IP, protocol to be captured (ICMP),
        interface used to "SNIFF"
        '''
        self.v_host = '15.181.163.0'
        self.v_proto = 'icmp'
        self.iface_name = 'en0'             # --- > From a different computer, verify the "SNIFF" interface
        self.filter_string = self.v_proto
        
        # ---> pyshark LiveCapture definitions
        self.capture = pyshark.LiveCapture(
                                    interface=self.iface_name,
                                    bpf_filter=self.filter_string
                                    )
        
    def icmp_pcap (self):
        '''
        Function description:
        This function captures the frames from the wire and craps the frame looking for selected
        fields, those fields are the only relevant to calculate the RTT information for all
        network elements from point A ---> Z on the traceroute.
        '''
        self.pkt_inf = {}
        
        for self.packet in self.capture.sniff_continuously():
            if self.packet.icmp.type in ('11','0'):     # ---> This "IF" function is intended jus to select the relevant frames
                                                        # ---> for the traceroute.
                                                        # ---> icmp.type = 11 ( means Time-to-live-expired)
                                                        # ---> icmp.type = 0  ( means ICMP-response)
                                                        # ---> pyshark calculates the time delta between the previous frame
                                                        # ---> and the next, this will provide the RTT with Time-to-live-expired
                                                        # ---> under field "icmp.resptime"
                self.pkt_inf['Time'] = self.packet.frame_info.time_epoch
                self.pkt_inf['src'] = self.packet.ip.dst
                self.pkt_inf['dest'] = self.packet.ip.src
                self.pkt_inf['Type'] = self.packet.icmp.type
                
                if hasattr(self.packet.icmp, 'resptime'):   # --> When icmp.type = 11 ( means Time-to-live-expired)
                    self.pkt_inf['RTT'] = self.packet.icmp.resptime
                else:                                       # --> icmp.type = 0  ( means ICMP-response)
                    self.pkt_inf['RTT'] = ("{0:.2f}".format(float (self.packet.frame_info.time_delta) *1000))
                    
                self.pkt_process ()                         # ---> Calls for a function to process the frame, this can be PostgreSQL,
                                                            # ---> Prometheus or MongoDB
                
                if self.packet.ip.src == self.v_host:       # ---> When we reach the destination, the capture will end.
                    print ("###############################")
                    print (" --- > Traceroute completed ...")
                    print ("###############################")
                    
                    break
    
    def pkt_process (self):
        '''
        Function description:
        
        '''
        print (self.pkt_inf)


def func1_f_packet_capture ():
    '''
    Function description:
    
    '''
    pkt = pcap_capture()        # Initiate Class, the purpose is just to load the interface configuration,
                                # this improves performance during the packet capture.

    pkt.icmp_pcap()             # Calls the function icmp_pcap, this function will collect the icmp data from the
                                # icmp frame as they arrive on the wire

    return ()

def func2_ICMP_trace ():
    '''
    Function description:
    
    '''
    
    time.sleep(3)               # This delay is set just to let pyshark process to initiate the interface for our capture.
    
    v_ttl = 100                 # This value is randomly set, the max TTL for the ICMP will be 100
                                # however when the ICMP packet reaches the destination the process will be terminated
                                # as a consequence we will not need to reach the 100 TTL setting.
    
    # --> This "for loop" is the key pease on the Trace route, the objective is just to
    # --> perform a ICMP ping incrementing the TTL, this will discover the next hop on the route
    for ttl in range (v_ttl):
        subprocess.run(["ping", "15.181.163.0 -s 1472 -c 1 -i 0.1 -t 1 " , "-m {0}".format(ttl)], stdout=subprocess.DEVNULL)
                       #             |             |     |     |     |          |       |                       |
                       #             |             |     |     |     |          |       |                       o----> Removes the command from the output
                       #             |             |     |     |     |          |       o----------------------------> Adds the TTL value inside the ICMP command
                       #             |             |     |     |     |          o------------------------------------> Wild card for TTL variable
                       #             |             |     |     |     o-----------------------------------------------> Timeout in seconds
                       #             |             |     |     o-----------------------------------------------------> Timer between ICMP packets wait-time
                       #             |             |     o-----------------------------------------------------------> Will send one ICMP packet
                       #             |             o-----------------------------------------------------------------> MTU size
                       #             o-------------------------------------------------------------------------------> Destination IP
    
    # Sets a time when the ICMP test cycle ends, point of reference just to calculate how long it took the test
    v_end_icmp = datetime.datetime.now()
    
    # Self explanatory
    print ("###################################################")
    print ("Process started @:  ",v_time_stamps.v_start_time)
    print ("ICMP ended @:       ",v_end_icmp)
    print ("Test lasted:        ",v_end_icmp - v_time_stamps.v_start_time)
    print ("###################################################")
    
    # ---> Process will wait for 3 seconds to alow the las packets to arrive and being processed
    # ---> before pyshark is terminated
    time.sleep(3)
    
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
        print("----- > Error Encountered while running script")


# ==> BEGINNING
os.system('clear')

'''
====> This section defines how many test cycles will be run
'''
v_times = 3

for _ in range(v_times):
    
    v_time_stamps = pcap_times()    # Initiating the class
    
    if __name__ == '__main__':
        
        p1 = Process(target=func1_f_packet_capture)
        p1.start()
        p2 = Process(target=func2_ICMP_trace)
        p2.start()
        p1.join()
        p2.join()
# ==> END