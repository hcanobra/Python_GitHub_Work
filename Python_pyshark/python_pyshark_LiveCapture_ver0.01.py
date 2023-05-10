import pyshark
import pandas as pd
import matplotlib.pyplot as plt
 
filename = input("Please enter OUTPUT filename with Extension csv/pcap example- file.csv or file.pcap:: ")
try:
    capture = pyshark.LiveCapture(interface="en0", output_file=filename)
    capture.sniff()
except KeyboardInterrupt:
    print(capture)
    if len(capture) > 10:
        capture1 = pyshark.FileCapture(filename)
        ip = []
        for pkt in capture1:
            if ("IP" in pkt):
                if ("UDP" in pkt):
                    print(pkt.ip.src, pkt.udp.dstport)
                    ip.append([pkt.ip.src, pkt.udp.dstport])
                elif ("TCP" in pkt):
                    print(pkt.ip.src, pkt.tcp.dstport)
                    ip.append([pkt.ip.src, pkt.tcp.dstport])
            elif ("IPV6" in pkt):
                if ("UDP" in pkt):
                    print(pkt.ipv6.src, pkt.udp.dstport)
                    ip.append([pkt.ipv6.src, pkt.udp.dstport])
                elif ("TCP" in pkt):
                    print(pkt.ipv6.src, pkt.tcp.dstport)
                    ip.append([pkt.ipv6.src, pkt.tcp.dstport])

        data = pd.DataFrame(ip, columns=['sourceip', 'port'])
        data['port'] = data['port'].astype(int)
        data_crosstab = pd.crosstab(data['sourceip'], data['port'])
        print(data_crosstab)
        data_crosstab.plot.bar(stacked=True)
        plt.show()
    else:
        print("[-] YOU HAVE LESS PACKETS TO PLOT THE GRAPH")