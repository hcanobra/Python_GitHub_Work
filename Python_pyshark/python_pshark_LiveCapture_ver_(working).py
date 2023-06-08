#!/usr/bin/env python3
# capture.py
import pyshark
import pandas as pd
import os
from multiprocessing import Process


def f_initiate ():
    v_df1 = pd.DataFrame([])
    v_destination = ""
    v_ttl = 1
    data = {}
    v_delay = 10
    return (v_df1,v_destination,v_ttl,data,v_delay)

iface_name = 'en0'
filter_string = 'host 15.181.163.0'
capture = pyshark.LiveCapture(
                            interface=iface_name,
                            bpf_filter=filter_string
                            )


def func1():
    print ('func1: Starting, PCAP in progress.... ')

    v_df = pd.DataFrame([])
    v_host = "15.181.163.0"

    try:
        capture.sniff(packet_count=2,
                    timeout=5)
        func2()

    except KeyboardInterrupt:
        print ("###########################")
        print ("# Func1: finishing        #")
        print ("# Program terminated..... #")
        print ("###########################")
        pass

def func2():
    print ('Func2: starting')
    v_df1,v_destination,v_ttl,data,v_delay = f_initiate ()
    
    try:
        if len(capture) > 0:
            for packet in capture:

                #data['Cycle'] = cycle
                data['Frame'] = packet.number
                data['Time'] = packet.frame_info.time_epoch
                data['host'] = packet.ip.dst
                data['dest'] = packet.ip.src
                data['ttl'] = packet.ip.ttl
                

                v_df1 = v_df1.append(data,ignore_index=True)

                print(v_df1)

    
    except KeyboardInterrupt:
        print ('Func2: finishing')
        pass
    


if __name__ == '__main__':
    try:
      while True:
        p1 = Process(target=func1)
        p1.start()
        p2 = Process(target=func2)
        p2.start()
        p1.join()
        p2.join()
    except:
        pass