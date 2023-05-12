#!/usr/bin/env python3
# capture.py
import os
from multiprocessing import Process
import time
import pyshark
import pandas as pd


def func1 ():
    print (" Process 1 start... ")
    time.sleep (5)

    for times in range(5):
        os.system('ping 15.181.163.0 -s 1472 -c 1')
        time.sleep (3)

    return

def func2():
    print (" Process 2 start... ")
    fuc2_pyshark ()
    return

def fuc2_pyshark ():
    #os.system('iterm')
    try:
        while True:
            df1 = pd.DataFrame([])
            df2 = pd.DataFrame([])

            iface_name = 'en0'
            filter_string = 'host 15.181.163.0'
            capture = pyshark.LiveCapture(
                                        interface=iface_name,
                                        bpf_filter=filter_string
                                        )
            
            capture.sniff(packet_count=2,
                            timeout=5)
            
            if len(capture) > 0:
                for packet in capture:
                    df2 = pd.DataFrame ({
                                        'Time': packet.frame_info.time_epoch,
                                        'host': packet.ip.dst,
                                        'dest': packet.ip.src,
                                        'length': packet.length,
                                        'ttl': packet.ip.ttl,
                                        'Type': packet.icmp.type
                                        }, index=[0])
                    if hasattr(packet.icmp, 'resptime'):
                        df2['RTT'] = packet.icmp.resptime

                    df1 = pd.concat([df1,df2],axis=0)

                print ('Data Frame ready for PostgreSQL...')
                print (df1)
            else:
                print(" ---> No frames captured..")
                break
    except:
        pass            
   

os.system('clear')
if __name__ == '__main__':
    p1 = Process(target=func1)
    p1.start()
    p2 = Process(target=func2)
    p2.start()
    p1.join()
    p2.join()
