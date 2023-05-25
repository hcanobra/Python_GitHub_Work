from multiprocessing import Process
import os
import time

def f_global_definitions ():
    v_bw = ['40M','50M','80M','100M']
    v_test = [1,2,3,4,5,6]
    v_date = '04032023'
    v_directory = '/Users/hcanobra/Documents/Dreamscape/pcap_udp/'

    return (v_bw, v_test, v_date, v_directory)

def f_iperf_command ():

    v_bw, v_test, v_date, v_directory = f_global_definitions()

    for test in v_test:
        for bw in v_bw:
            
            print ("")
            print ("############ Start test: %s with Bandwidth: %s"%(test,bw))
            print(os.system('date'))

            v_command = ('iperf3 -c 15.181.163.0 -u -t 600 -b %s -R --timestamp >> %sReadme_pcap_udp_%s_%s_NVIDIA_%s.txt'%(bw,v_directory,v_date,bw,test))
            #               |     |      |        | |   |  |  |       |        |       |          | |     |    |        |       |        |    |   |
            #               |     |      |        | |   |  |  |       |        |       |          | |     |    |        |       |        |    |   o---> Parameter:Defined from variable
            #               |     |      |        | |   |  |  |       |        |       |          | |     |    |        |       |        |    o-------> Parameter: Defined from variable
            #               |     |      |        | |   |  |  |       |        |       |          | |     |    |        |       |        o------------> Parameter: Defined from variable
            #               |     |      |        | |   |  |  |       |        |       |          | |     |    |        |       o---------------------> Parameter: Defined from variable
            #               |     |      |        | |   |  |  |       |        |       |          | |     |    |        o-----------------------------> Parameter: Defined from variable
            #               |     |      |        | |   |  |  |       |        |       |          | |     |    o--------------------------------------> Variable: Includes the test cycle ID (1,2,3,4,5...)
            #               |     |      |        | |   |  |  |       |        |       |          | |     o-------------------------------------------> Value: Naming standard
            #               |     |      |        | |   |  |  |       |        |       |          | o-------------------------------------------------> Variable: Includes the BW on the file name
            #               |     |      |        | |   |  |  |       |        |       |          o---------------------------------------------------> Variable: Includes the date on the file name
            #               |     |      |        | |   |  |  |       |        |       o--------------------------------------------------------------> Value: Naming standard
            #               |     |      |        | |   |  |  |       |        o----------------------------------------------------------------------> Variable: Includes de directory from v_directory variable
            #               |     |      |        | |   |  |  |       o-------------------------------------------------------------------------------> Parameter: We wil include the timestamp information
            #               |     |      |        | |   |  |  o---------------------------------------------------------------------------------------> Parameter: Indicates that we will be using IPERF as reversed (transmitting from remote host)
            #               |     |      |        | |   |  o------------------------------------------------------------------------------------------> Variable: Includes the bit rate of the transfer this value comes from variable BW
            #               |     |      |        | |   o---------------------------------------------------------------------------------------------> Parameter: Defines de Bandwidth speed to transmit
            #               |     |      |        | o-------------------------------------------------------------------------------------------------> Value: Defines the length of the test specified in seconds
            #               |     |      |        o---------------------------------------------------------------------------------------------------> Parameter: Indicates that we will define time as the length of the test
            #               |     |      o------------------------------------------------------------------------------------------------------------> Value: IPERF server ip address
            #               |     o-------------------------------------------------------------------------------------------------------------------> Parameter: Indicates that we will run IPERF as client
            #               o-------------------------------------------------------------------------------------------------------------------------> Command: Runs IPERF

            print (">> "+v_command)
            os.system (v_command)
            
            print(os.system('date'))
            print ("############ End of test: %s with Bandwidth: %s"%(test,bw))

    return ()

### Begin
os.system('clear')
f_iperf_command ()

### End

