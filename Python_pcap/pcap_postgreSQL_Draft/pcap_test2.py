'''
https://dpkt.readthedocs.io/en/latest/examples.html

'''



import dpkt

file_name = '/Users/canobhu/Documents/GitHub/GitHub/Python_Pcap/example-01.pcap'

f = open(file_name,'rb')

pcap = dpkt.pcap.Reader(f)

for ts, buf in pcap:
    eth_raw = dpkt.ethernet.Ethernet(buf)
    v_eth = eth_raw.data
    v_ip = v_eth.ip
    


    #if tcp.dport == 80 and len(tcp.data) > 0:
    #http = dpkt.http.Request(tcp.data)
    #print (http.uri)

f.close()