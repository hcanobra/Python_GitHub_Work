#!/usr/bin/env python3
# capture.py
import pyshark
import pandas as pd
import os
from multiprocessing import Process
import threading


packet = ''


class init_var:
    def __init__(self):
        self.v_destination = ""
        self.v_ttl = 1
        self.data = {}
        self.v_delay = 10


class pcap_param:
    def __init__(self):
        self.iface_name = 'en0'
        self.filter_string = 'host 15.181.163.0'
        self.capture = pyshark.LiveCapture(
                            interface= self.iface_name,
                            bpf_filter= self.filter_string
                            )

def func1():

    print ("######################################")
    print ('Func1: Starting, PCAP in progress.... ')
    print ("######################################")

    


    try:
        while True:
            pcap = pcap_param()
            pcap.capture.sniff(packet_count=80)

            # create a process
            t1 = threading.Thread(target=func2, args=(pcap,))
            t1.start()


    except KeyboardInterrupt:
        print ("######################################")
        print ("# Func1: finishing        ############")
        print ("# Program terminated..... ############")
        print ("######################################")
        pass

def func2(packets):
    print ("     ------------------------------------------------------")
    print ("     -> Func2: Starting         ---------------------------")
    print ("     ->  Scrap PCAP and adding values to Prometheus ..... -")
    print ("     ------------------------------------------------------")



    v_df1 = pd.DataFrame([])
    for packet in packets.capture:
        v_df1 = pd.DataFrame(data = [
                                        [packet.frame_info.time_epoch,
                                        packet.ip.dst,
                                        packet.ip.src,
                                        packet.icmp.type,
                                        packet.ip.ttl
                                        ]
                                    ], 
                            columns = 
                                    [
                                        ['Time',
                                        'Dst',
                                        'Src',
                                        'type',
                                        'ttl'
                                        ]
                                    ])
        

        #v_df1 = v_df1.append(data,ignore_index=True)

        #print(v_df1)
        v_df1.to_csv ('/Users/hcanobra/Documents/Dreamscape/df_pcap.csv',mode='a', index='False', header='False')
        #x = x +1
        #print (x)
    v_df1 = pd.DataFrame([])

    print ("     ------------------------------------------------------")
    print ("     ->  Func2: finishing        --------------------------")
    print ("     ->  Program terminated..... --------------------------")
    print ("     ------------------------------------------------------")
    


func1()