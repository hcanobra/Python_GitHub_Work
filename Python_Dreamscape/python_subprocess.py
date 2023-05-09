from multiprocessing import Process
import os
import time

def func1():
    print ('func1: starting')
    v_time = 30
    v_file = [1,2]
    for file in v_file:
       
        os.system (" wireshark -i en0 -k -f 'host 15.181.163.0' -w /Users/hcanobra/Documents/Dreamscape/pcap_tcp_temp_%s.pcap -b filesize:1000 -a duration:%s"%(file,v_time))
        # -b filesize:<switch to next file after NUM KB>  /// -b filesize:1000 equals 1M Data on the frame frame size 1024

    print ('func1: finishing')

def func2():
    time.sleep(5)
    print ('func2: starting')
    v_test = [1,2]
    v_file_size = [2000]

    '''
    40Mbps
    40000000 -- 1 sec
    4000000 -- 0.1 sec 

    1 - 8
    X - 4000000

    MTU == 1500
    -s 1472 (28 payload)
    (1500*2)*8 = 24Kb

    ((1472+28)*2)*8 = 24Kb

    24 / 84.034 = 1.56 Mbps

    '''
    for test in v_test:
        os.system ('ping 15.181.163.0 -s 1472 -c 10 -i 0.1  --apple-time >> /Users/hcanobra/Documents/Dreamscape/icmp_%s.txt'%test)
        # -s <packet size in Bytes
        os.system('killall wireshark')
    print ('func2: finishing')

if __name__ == '__main__':
  p1 = Process(target=func1)
  p1.start()
  p2 = Process(target=func2)
  p2.start()
  p1.join()
  p2.join()