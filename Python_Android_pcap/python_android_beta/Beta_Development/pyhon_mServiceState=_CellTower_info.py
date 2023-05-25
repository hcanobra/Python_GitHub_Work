import re
import time
import sys

import subprocess


'''
dumpsys telephony.registry | grep mServiceState=

'''
v_dir = '/Users/hcanobra/Documents/GitHub_Repository/GitHub_Could_Projects/Python_GitHub_Work/Python_Android_pcap/platform-tools/./adb shell '
mServiceState = 'dumpsys telephony.registry | grep mServiceState='
p = subprocess.Popen(v_dir+mServiceState, shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8').splitlines()


for v_kpi_mServiceState in p:

    v_split = (re.findall('([A-zA-Z]\w*=[0-9]\d*)', v_kpi_mServiceState))

    for i in v_split:
        print (i)
        
        
    v_split = (re.findall('([A-zA-Z]\w*=[[].{2,33}[]])', v_kpi_mServiceState))


    for i in v_split:
        print (i)
        
    