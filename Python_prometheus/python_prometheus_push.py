'''

https://prometheus.io/docs/concepts/metric_types/

'''

import pandas as pd
from prometheus_client import CollectorRegistry, Gauge,Histogram,Summary,Info, push_to_gateway
import time
import numpy

# Working as a directory input
class PrometheusClient_Gouge:
    def __init__(self):
        
        self.kpi_message = 'Mobile_info'    
        self.kpi_lebels = {
                'Time': '1684959180',
                'src': '172.217.14.68',
                'dst': '10.215.173.1'
                }
        
        self.kpi_lebels_names = list(self.kpi_lebels.keys())
        self.kpi_lebels_values = list(self.kpi_lebels.values())
        
        self.kpi_dic = {
                    'ttl': 64,
                    'lat': 40.493894,
                    'lon': -111.865829,
                    'Cell_ChannelNumber': 975,
                    'Cell_Pci': 423,
                    'mob_Earfcn': 975,           
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
                    'Cell_rsrq': -7
                    }
        
        # Start up the server to expose the metrics.
        self.registry = CollectorRegistry()    
    
    def Gouge_registry (self):
        
                
        for kpi_name,kpi_value in self.kpi_dic.items():
            print (kpi_name)
            print (kpi_value)
            
            self.g = Gauge(
                            kpi_name, 
                            self.kpi_message,
                            labelnames=self.kpi_lebels_names,
                            registry=self.registry
                            )
            
            self.g.labels(1,2,3).set(kpi_value)

        self.g = Info(
                    'my_build_version', 'Description of info',
                    registry=self.registry   
                        )
        self.g.info(self.kpi_lebels)
            


            
    def Gouge_push(self):
        
        push_to_gateway('15.181.163.0:9091',
                        job='MEC_Dreamscape', 
                        registry=self.registry)

def f_gauge ():
    

    
    prom_instance = PrometheusClient_Gouge()
    
    prom_instance.Gouge_registry()
    
    prom_instance.Gouge_push()

class PrometheusClient_Histogram:
    def __init__(self):
        # Start up the server to expose the metrics.
        self.registry = CollectorRegistry()    
    
    def Histogram_registry (self, kpi_family, kpi_message, kpi_data):
        self.g = Histogram(
                        kpi_family, 
                        kpi_message,
                        labelnames=['Source_IP',
                                    'Destination_IP'],
                        registry=self.registry
                        )
        self.g.labels('1.1','2.2').observe(kpi_data)

            
    def Histogram_push(self):
        
        push_to_gateway('15.181.163.0:9091',
                        job='MEC_Dreamscape', 
                        registry=self.registry)

def f_histogram ():
    
    kpi_message = 'Mobile_info'
    kpi_dic = {'MEC_Dreamscape_mob_ChannelNumber': 100, 'MEC_Dreamscape_mob_Earfcn': 20}
    prom_instance = PrometheusClient_Histogram()
    
    for x,y in kpi_dic.items():
        prom_instance.Histogram_registry (x, kpi_message, y)
    
    prom_instance.Histogram_push()

## Working as a directory input

class PrometheusClient_Summary:
    def __init__(self):
        #     # Start up the server to expose the metrics.
        self.registry = CollectorRegistry()
        
    def Summary_registry (self, kpi_family, kpi_message, kpi_data):
        self.g = Summary(
                        kpi_family, 
                        kpi_message, 
                        labelnames=['Source_IP','Destination_IP'],
                        registry=self.registry   
                        )
        
        self.g.labels(kpi_data[0],kpi_data[1]).observe(kpi_data[2])

        
    def Summary_push(self, data):
        push_to_gateway('15.181.163.0:9091',
                        job='MEC_Dreamscape', 
                        registry=self.registry)

def f_summary():
    kpi_family = 'MEC_Dreamscape_Summary'
    kpi_message = "KPI"
    kpi_data = ['10.0.0.1', '10.0.0.2', 1]

    prom_sum = PrometheusClient_Summary()
    prom_sum.Summary_registry (kpi_family, kpi_message, kpi_data)
    prom_sum.Summary_push(kpi_data)

class PrometheusClient_Info:
    def __init__(self):
        #     # Start up the server to expose the metrics.
        self.registry = CollectorRegistry()
        
    def Info_registry (self, kpi_family):
        
        self.g = Info(
                    'my_build_version', 'Description of info',
                    registry=self.registry   
                        )
        self.g.info({'version': '1.2.3', 'buildhost': 'foo@bar'})

    def Info_push(self):
        push_to_gateway('15.181.163.0:9091',
                        job='MEC_Dreamscape', 
                        registry=self.registry
                        )
                        

def f_info ():
    kpi_dic = {'MEC_Dreamscape_mob_ChannelNumber': 1, 'MEC_Dreamscape_mob_Earfcn': 2}

    prom_sum = PrometheusClient_Info()
    prom_sum.Info_registry (kpi_dic)
    prom_sum.Info_push()

f_gauge ()
#f_histogram ()
#f_info ()

'''

prom_instance = PrometheusClient_Gouge()
v_records.append(time.time())
prom_instance.Gouge_push(v_records)


prom_hist = PrometheusClient_Histogram()
prom_hist.Histogram_push(v_records)




'''












v_documentation = {
                'Time': '1684959180',       # Info
                'src': '172.217.14.68',     # Info
                'dst': '10.215.173.1',      # Info
                'length': '132',            # Histogram
                'ttl': '64',                # Info
                'RTT': '12',                # Histogram
                'lat': '40.493894',         # Info
                'lon': '-111.865829',       # Info
                'mChannelNumber': '975',    # Gauge
                'mPci': '423',              # Info
                'mEarfcn': '975',           # Gouge           
                'rssi': '-51',              # Gouge
                'rsrp': '-71',              # Gouge
                'rsrq': '-8',               # Gouge
                'rssnr': '28',              # Gouge
                'lteLevel': '5',            # Gouge
                'mPci': '423',              # Gouge
                'mEarfcn': '975',           # Gouge
                'rssi': '-51',              # Gouge
                'rsrp': '-69',              # Gouge
                'rsrq': '-7'                # Gouge
                }




'''
    'Time': '1684959180',       # Info
    'src': '172.217.14.68',     # Info
    'dst': '10.215.173.1',      # Info
    'ttl': '64',                # Info
    'lat': '40.493894',         # Info
    'lon': '-111.865829',       # Info
    'mob_Pci': '423',           # Info
    
    'length': '132',            # Gauge    
    'RTT': '12',                # Gauge
    'mob_ChannelNumber': '975',    # Gauge
    'mob_Earfcn': '975',           # Gouge           
    'mob_rssi': '-51',             # Gouge
    'mob_rsrp': '-71',             # Gouge
    'mob_rsrq': '-8',              # Gouge
    'mob_rssnr': '28',             # Gouge
    'mob_lteLevel': '5',           # Gouge
    'mob_Pci': '423',              # Gouge
    'mob_Earfcn': '975',           # Gouge
    'Cell_rssi': '-51',            # Gouge
    'Cell_rsrp': '-69',            # Gouge
    'Cell_rsrq': '-7'              # Gouge

    {
    'Time': '1684959180',
    'src': '172.217.14.68',
    'dst': '10.215.173.1',
    'ttl': '64',
    'lat': '40.493894',
    'lon': '-111.865829',
    'Cell_ChannelNumber': '975',
    'Cell_Pci': '423',
    'mob_Earfcn': '975',           
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
    'Cell_rsrq': -7
    }
    
'''