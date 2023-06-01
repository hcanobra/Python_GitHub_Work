

import pandas as pd
from prometheus_client import CollectorRegistry, Gauge,Histogram,Summary,Info, push_to_gateway
import time
import numpy

# Working as a directory input
class PrometheusClient_Gouge:
    def __init__(self,kpi_lebels,kpi_dic):
        
        self.kpi_lebels = kpi_lebels
        self.kpi_dic = kpi_dic
        
        self.kpi_message = 'Mobile_info'
        '''
        self.kpi_lebels = {
                'Time': '1684959180',
                'src': '172.217.14.68',
                'dst': '10.215.173.1'
        }
        '''

        self.kpi_lebels_names = list(self.kpi_lebels.keys())
        self.kpi_lebels_values = list(self.kpi_lebels.values())

        '''
        self.kpi_dic = {
            'ttl': 64,
            'lat': 40.493894,
            'lon': -111.865829,
            'Cell_ChannelNumber': 975,
            'Cell_Pci': 423,
            'mob_Pci': 423,
            'length': 132,
            'RTT': 12,
            'mob_rssi': -51,
            'mob_rsrp': -71,
            'mob_rsrq': -8,
            'mob_rssnr': 28,
            'mob_lteLevel': 5,
            'mob_Earfcn': 975,
            'Cell_rssi': -51,
            'Cell_rsrp': -69,
            'Cell_rsrq': -7,
        }
        '''

        # Start up the server to expose the metrics.
        self.registry = CollectorRegistry()    
    
    def Gouge_registry (self):
                
        for kpi_name,kpi_value in self.kpi_dic.items():
            
            self.g = Gauge(
                            kpi_name, 
                            self.kpi_message,
                            labelnames=self.kpi_lebels_names,
                            registry=self.registry
                            )
            v_kpi_value = float (kpi_value[0])
            self.g.labels(self.kpi_lebels_values[0],self.kpi_lebels_values[1],self.kpi_lebels_values[2]).set(v_kpi_value)

        self.g = Info(
                    'MEC_Dreamscape_event', 'Event information',
                    registry=self.registry   
                        )
        self.g.info(self.kpi_lebels)
            


            
    def Gouge_push(self):
        
        push_to_gateway('15.181.163.0:9091',
                        job='MEC_Dreamscape', 
                        registry=self.registry)

def f_gauge (kpi_lebels,kpi_dic):
    
    kpi_lebels = kpi_lebels
    kpi_dic = kpi_dic
    prom_instance = PrometheusClient_Gouge(kpi_lebels,kpi_dic)
    
    prom_instance.Gouge_registry()
    
    prom_instance.Gouge_push()

## Working as a directory input

#print ('hello')

#f_gauge ()
