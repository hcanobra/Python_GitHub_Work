import os
import nest_asyncio
from multiprocessing import Process


import python_pcap_curl_android_ver0a as ue_pcap


v_init = ue_pcap.pcap_curl_android()



# ==> BEGINNING
os.system('clear')
nest_asyncio.apply()

#v_init.p_f_curl()

if __name__ == '__main__':
    p1 = Process(target=v_init.f_curl())
    p1.start()
    p2 = Process(target=v_init.f_pcap())
    p2.start()
    p1.join()
    p2.join()
        
# ==> END