from multiprocessing import Process
import os
import time

def f_global_definitions ():
    v_bw = ['40M','60','80','100']
    v_test = [1]
    v_date = '05222023'
    v_directory = '/Users/hcanobra/Documents/GitHub_Repository/GitHub_Could_Projects/Python_GitHub_Work/Python_Dreamscape/pcap_tcp/'

    return (v_bw, v_test, v_date, v_directory)

    

def func1():
    v_bw, v_test, v_date, v_directory = f_global_definitions()

    for test in v_test:

        for bw in v_bw:
            print ("")
            print ("############ Start test: %s with Bw: %s"%(test,bw))
            print ('>> Func1: Starting WireShark.. ')

            v_command = ("wireshark -i en0 -k -f 'host 15.181.163.0' -w %spcap_tcp_%s_%s_NVIDIA_%s.pcap -b filesize:200000"%(v_directory, v_date,bw,test))
            #                 |      |   |  |  |          |           |  |    |     |  |    |    |       |     |      |            |         |    |   |
            #                 |      |   |  |  |          |           |  |    |     |  |    |    |       |     |      |            |         |    |   o---> Parameter: Defined from variable v_test, how many test cycles are going to be run
            #                 |      |   |  |  |          |           |  |    |     |  |    |    |       |     |      |            |         |    o-------> Parameter: Defined from variable v_bw, Bandwidth to be tested on each cycle
            #                 |      |   |  |  |          |           |  |    |     |  |    |    |       |     |      |            |         o------------> Parameter: Defines the date of the test cycle this will be used for file name
            #                 |      |   |  |  |          |           |  |    |     |  |    |    |       |     |      |            o----------------------> Parameter: Defines the directory where files will be stored
            #                 |      |   |  |  |          |           |  |    |     |  |    |    |       |     |      o-----------------------------------> Value: 200M, The size of each pcap file
            #                 |      |   |  |  |          |           |  |    |     |  |    |    |       |     o------------------------------------------> Attribute: pcap files will be limited by size, when meeting the value, new pcap file will be created
            #                 |      |   |  |  |          |           |  |    |     |  |    |    |       o------------------------------------------------> Parameter: ring-buffer of capture, defines characteristics of the capture in this case file size rotation
            #                 |      |   |  |  |          |           |  |    |     |  |    |    o--------------------------------------------------------> Variable: Includes test cycle ID (1,2,3,4,5...)
            #                 |      |   |  |  |          |           |  |    |     |  |    o-------------------------------------------------------------> Value: File naming standard
            #                 |      |   |  |  |          |           |  |    |     |  o------------------------------------------------------------------> Variable: Includes the BW
            #                 |      |   |  |  |          |           |  |    |     o---------------------------------------------------------------------> Variable: Includes the date
            #                 |      |   |  |  |          |           |  |    o---------------------------------------------------------------------------> Value: File naming standard
            #                 |      |   |  |  |          |           |  o--------------------------------------------------------------------------------> Variable: Includes the directory path
            #                 |      |   |  |  |          |           o-----------------------------------------------------------------------------------> Parameter: Set the output filename
            #                 |      |   |  |  |          o-----------------------------------------------------------------------------------------------> Value: Capture filter defined by Host IP Address
            #                 |      |   |  |  o----------------------------------------------------------------------------------------------------------> Parameter: Packet filter in libpcap
            #                 |      |   |  o-------------------------------------------------------------------------------------------------------------> Parameter: Start capturing immediately
            #                 |      |   o----------------------------------------------------------------------------------------------------------------> Value: Definition of the interface name to ne used
            #                 |      o--------------------------------------------------------------------------------------------------------------------> Parameter: Defines the interface to be used during the capture
            #                 o---------------------------------------------------------------------------------------------------------------------------> Command: Runs WireShark on a CLI
            #
            # WireShar options
            # https://www.wireshark.org/docs/wsug_html_chunked/ChCustCommandLine.html#:~:text=The%20%2Dk%20option%20specifies%20that,packet%20capture%20will%20occur%20from.
                 
            print (">> "+v_command)
            os.system (v_command)
            

def func2():
    v_bw, v_test, v_date, v_directory = f_global_definitions()

    for test in v_test:
        for bw in v_bw:
        
            time.sleep(5)
            print ('>> Func2: Starting IPERF on TCP.. ')

            v_command = ('docker run -it --rm networkstatic/iperf3 -c 15.181.163.0 -t 5 -b %s -R --timestamp >> %sReadme_pcap_tcp_%s_%s_NVIDIA_%s.txt'%(bw,v_directory,v_date,bw,test))
            #                                                 |     |      |        | |   |  |  |       |        |       |          | |     |    |        |       |        |    |   |
            #                                                 |     |      |        | |   |  |  |       |        |       |          | |     |    |        |       |        |    |   o---> Parameter:Defined from variable
            #                                                 |     |      |        | |   |  |  |       |        |       |          | |     |    |        |       |        |    o-------> Parameter: Defined from variable
            #                                                 |     |      |        | |   |  |  |       |        |       |          | |     |    |        |       |        o------------> Parameter: Defined from variable
            #                                                 |     |      |        | |   |  |  |       |        |       |          | |     |    |        |       o---------------------> Parameter: Defined from variable
            #                                                 |     |      |        | |   |  |  |       |        |       |          | |     |    |        o-----------------------------> Parameter: Defined from variable
            #                                                 |     |      |        | |   |  |  |       |        |       |          | |     |    o--------------------------------------> Variable: Includes the test cycle ID (1,2,3,4,5...)
            #                                                 |     |      |        | |   |  |  |       |        |       |          | |     o-------------------------------------------> Value: Naming standard
            #                                                 |     |      |        | |   |  |  |       |        |       |          | o-------------------------------------------------> Variable: Includes the BW on the file name
            #                                                 |     |      |        | |   |  |  |       |        |       |          o---------------------------------------------------> Variable: Includes the date on the file name
            #                                                 |     |      |        | |   |  |  |       |        |       o--------------------------------------------------------------> Value: Naming standard
            #                                                 |     |      |        | |   |  |  |       |        o----------------------------------------------------------------------> Variable: Includes de directory from v_directory variable
            #                                                 |     |      |        | |   |  |  |       o-------------------------------------------------------------------------------> Parameter: We wil include the timestamp information
            #                                                 |     |      |        | |   |  |  o---------------------------------------------------------------------------------------> Parameter: Indicates that we will be using IPERF as reversed (transmitting from remote host)
            #                                                 |     |      |        | |   |  o------------------------------------------------------------------------------------------> Variable: Includes the bit rate of the transfer this value comes from variable BW
            #                                                 |     |      |        | |   o---------------------------------------------------------------------------------------------> Parameter: Defines de Bandwidth speed to transmit
            #                                                 |     |      |        | o-------------------------------------------------------------------------------------------------> Value: Defines the length of the test specified in seconds
            #                                                 |     |      |        o---------------------------------------------------------------------------------------------------> Parameter: Indicates that we will define time as the length of the test
            #                                                 |     |      o------------------------------------------------------------------------------------------------------------> Value: IPERF server ip address
            #                                                 |     o-------------------------------------------------------------------------------------------------------------------> Parameter: Indicates that we will run IPERF as client
            #                                                 o-------------------------------------------------------------------------------------------------------------------------> Command: Runs IPERF

            print (">> "+v_command)
            os.system (v_command)

            print ('>> Func2: Finishing IPERF on TCP.. ')
            print ('>> Func1: Stoping WireShark.. ')
            print ("############ End of test: %s with Bw: %s"%(test,bw))
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


