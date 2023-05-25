from multiprocessing import Process
import os
import time

def f_global_definitions ():
    v_test = [1,2,3,4,5,6]
    v_date = '04032023'
    v_directory = '/Users/hcanobra/Documents/GitHub_Repository/GitHub_Could_Projects/Python_GitHub_Work/Python_Dreamscape/pcap_icmp/'

    return (v_test, v_date, v_directory)

    

def func1():
    v_test, v_date, v_directory = f_global_definitions()

    for test in v_test:
            print ("")
            print ("############ Start test: %s "%(test))
            print ('>> Func1: Starting WireShark.. ')

            v_command = ("wireshark -i en0 -k -f 'host 15.181.163.0' -w %spcap_tcp_%s_NVIDIA_%s.pcap -b filesize:200000"%(v_directory, v_date,test))
            #                 |      |   |  |  |          |           |  |    |     |  |     |        |     |      |            |         |    |   |
            #                 |      |   |  |  |          |           |  |    |     |  |     |        |     |      |            |         |    |   o---> Parameter: Defined from variable v_test, how many test cycles are going to be run
            #                 |      |   |  |  |          |           |  |    |     |  |     |        |     |      |            |         |    o-------> Parameter: Defined from variable v_bw, Bandwidth to be tested on each cycle
            #                 |      |   |  |  |          |           |  |    |     |  |     |        |     |      |            |         o------------> Parameter: Defines the date of the test cycle this will be used for file name
            #                 |      |   |  |  |          |           |  |    |     |  |     |        |     |      |            o----------------------> Parameter: Defines the directory where files will be stored
            #                 |      |   |  |  |          |           |  |    |     |  |     |        |     |      o-----------------------------------> Value: 200M, The size of each pcap file
            #                 |      |   |  |  |          |           |  |    |     |  |     |        |     o------------------------------------------> Attribute: pcap files will be limited by size, when meeting the value, new pcap file will be created
            #                 |      |   |  |  |          |           |  |    |     |  |     |        o------------------------------------------------> Parameter: ring-buffer of capture, defines characteristics of the capture in this case file size rotation
            #                 |      |   |  |  |          |           |  |    |     |  |     o---------------------------------------------------------> Variable: Includes test cycle ID (1,2,3,4,5...)
            #                 |      |   |  |  |          |           |  |    |     |  o---------------------------------------------------------------> Value: File naming standard
            #                 |      |   |  |  |          |           |  |    |     o------------------------------------------------------------------> Variable: Includes the date
            #                 |      |   |  |  |          |           |  |    o------------------------------------------------------------------------> Value: File naming standard
            #                 |      |   |  |  |          |           |  o-----------------------------------------------------------------------------> Variable: Includes the directory path
            #                 |      |   |  |  |          |           o--------------------------------------------------------------------------------> Parameter: Set the output filename
            #                 |      |   |  |  |          o--------------------------------------------------------------------------------------------> Value: Capture filter defined by Host IP Address
            #                 |      |   |  |  o-------------------------------------------------------------------------------------------------------> Parameter: Packet filter in libpcap
            #                 |      |   |  o----------------------------------------------------------------------------------------------------------> Parameter: Start capturing immediately
            #                 |      |   o-------------------------------------------------------------------------------------------------------------> Value: Definition of the interface name to ne used
            #                 |      o-----------------------------------------------------------------------------------------------------------------> Parameter: Defines the interface to be used during the capture
            #                 o------------------------------------------------------------------------------------------------------------------------> Command: Runs WireShark on a CLI
            #
            # WireShark options
            # https://www.wireshark.org/docs/wsug_html_chunked/ChCustCommandLine.html#:~:text=The%20%2Dk%20option%20specifies%20that,packet%20capture%20will%20occur%20from.
                 
            print (">> "+v_command)
            os.system (v_command)
            

def func2():

    v_test, v_date, v_directory = f_global_definitions()

    for test in v_test:
            time.sleep(5)
            
            print ('func2: starting')

            v_command = ('ping 15.181.163.0 -s 1472  -c 6000 -i 0.1  --apple-time >> %sReadme_pcap_icmp_%s_NVIDIA_%s.txt'%(v_directory,v_date,test))
            #               |     |           |  |    |  |    |  |         |          |          |       |        |             |       |    |
            #               |     |           |  |    |  |    |  |         |          |          |       |        |             |       |    o---> Parameter:Defined from variable
            #               |     |           |  |    |  |    |  |         |          |          |       |        |             |       o--------> Parameter: Defined from variable
            #               |     |           |  |    |  |    |  |         |          |          |       |        |             o----------------> Parameter: Defined from variable
            #               |     |           |  |    |  |    |  |         |          |          |       |        o------------------------------> Variable: Add test cycle id
            #               |     |           |  |    |  |    |  |         |          |          |       o---------------------------------------> Variable: Add date information
            #               |     |           |  |    |  |    |  |         |          |          o-----------------------------------------------> Value: Naming definition
            #               |     |           |  |    |  |    |  |         |          o----------------------------------------------------------> Variable: Add directory path
            #               |     |           |  |    |  |    |  |         o---------------------------------------------------------------------> Parameter: Add time stamp information
            #               |     |           |  |    |  |    |  o-------------------------------------------------------------------------------> Attribute: Each ping will be send every 0.1 sec
            #               |     |           |  |    |  |    o----------------------------------------------------------------------------------> Parameter: Interval definition
            #               |     |           |  |    |  o---------------------------------------------------------------------------------------> Value: 10 min (10 pings = 1 sec) this is as a result of interval 0.1 sec per ping
            #               |     |           |  |    o------------------------------------------------------------------------------------------> Parameter: Count
            #               |     |           |  o-----------------------------------------------------------------------------------------------> Value: Definition of frame size 1470 bits + 28 payload = MTU 1500
            #               |     |           o--------------------------------------------------------------------------------------------------> Parameter: Frame size 
            #               |     o--------------------------------------------------------------------------------------------------------------> Value: IP address to ping
            #               o--------------------------------------------------------------------------------------------------------------------> Command: Execute ping command
            

            print (">> "+v_command)
            os.system (v_command)

            print ('>> Func2: Finishing IPERF on ICMP.. ')
            print ('>> Func1: Stopping WireShark.. ')
            print ("############ End of test: %s "%(test))
            print ("")
            os.system('killall wireshark')
            time.sleep(5)


if __name__ == '__main__':
  os.system('clear')
  p1 = Process(target=func1)
  p1.start()
  p2 = Process(target=func2)
  p2.start()
  p1.join()
  p2.join()