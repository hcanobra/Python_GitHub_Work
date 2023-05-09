#!/bin/bash
myuser="mylovelyname"
echo my user is $myuser and my shell is $SHELL

MTU=1520

for i in {1..1000}
    do 
        #echo $i
        #MTU=`expr $MTU + 100` 
        #echo $MTU
        #rm /Users/hcanobra/Documents/Dreamscape/icmp.txt
        #rm -r /Users/hcanobra/Documents/Dreamscape/*.pcap
        #sudo wireshark -i en0 -k -f 'host 15.181.163.0' -a filesize:20000 -w /Users/hcanobra/Documents/Dreamscape/pcap_tcp_temp.pcap -b filesize:200
        echo ping 15.181.163.0 -s $MTU -c 2 -i 0.1  --apple-time >> /Users/hcanobra/Documents/Dreamscape/icmp.txt
    done

