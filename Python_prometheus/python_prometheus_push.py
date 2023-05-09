from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

 

registry = CollectorRegistry()

g = Gauge('job_last_success_unixtime', 'Last time a batch job successfully finished', registry=registry)

g.set_to_current_time()

push_to_gateway('10.1.1.12:9091', job='pcap', registry=registry)