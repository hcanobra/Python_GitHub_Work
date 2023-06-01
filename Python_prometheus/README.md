Python scripting with pyshark LiveCatpture
===
Initial version 05/09/2023
## Paper Information
- Title:  `Document reference`
- Authors:  `Hugo A Cano Bravo`
- Documentation repocitory: [https://TBD]()
- Other resources: [video position]()

## Install & Dependence
- python
- pyshark
- pandas
- os
- multiprocessing

## Dataset Preparation
| Dataset | Download |
| ---     | ---   |
| dataset-A | [download]() |
| dataset-B | [download]() |
| dataset-C | [download]() |
------------------------------------------------------------------------------------------------------------
# Reference documentation:
  - [Client library usage documentation for summaries on Python](https://prometheus.io/docs/concepts/metric_types/)
  ------------------------------------------------------------------------------------------------------------
## Creating environment in Python

- Creation of new environment in Python:
  ```
  mkdir prometheus_env
  python3 -m venv /path/to/new/virtual/environment/prometheus_env
  source /path/to/new/virtual/environment/bin/activate
  (prometheus_env)
  ```

- Add records to Prometheus Push Gateway
  ```
  registry = CollectorRegistry()
  g = Gauge('job_last_success_unixtime', 'Last time a batch job successfully finished', registry=registry)
  g.set_to_current_time()
  push_to_gateway('15.181.163.0:9091', job='pcap', registry=registry)
  ```
- Installing dependencies
  ```
  pip3 install prometheus_client
  ```

- Prometheus Metrics
  - [Prometheus documentation](https://prometheus.io/docs/concepts/metric_types/)
  
  The Prometheus client libraries offer four core metric types. These are currently only differentiated in the client libraries (to enable APIs tailored to the usage of the specific types) and in the wire protocol. The Prometheus server does not yet make use of the type information and flattens all data into untyped time series. This may change in the future.

------------------------------------------------------------------------------------------------------------
## Counter:
  
  - [Client library usage documentation for counters on Python](https://prometheus.io/docs/concepts/metric_types/)
  
  A counter is a cumulative metric that represents a single monotonically increasing counter whose value can only increase or be reset to zero on restart. For example, you can use a counter to represent the number of requests served, tasks completed, or errors.

  Do not use a counter to expose a value that can decrease. For example, do not use a counter for the number of currently running processes; instead use a gauge.
          
  Counters go up, and reset when the process restarts.

  ```Python
      from prometheus_client import Counter
      c = Counter('my_failures', 'Description of counter')
      c.inc()     # Increment by 1
      c.inc(1.6)  # Increment by given value
  ```
  If there is a suffix of _total on the metric name, it will be removed. When exposing the time series for counter, a _total suffix will be added. This is for compatibility between OpenMetrics and the Prometheus text format, as OpenMetrics requires the _total suffix.

  There are utilities to count exceptions raised:

  ```Python
      @c.count_exceptions()
      def f():
        pass

      with c.count_exceptions():
        pass

      # Count only one type of exception
      with c.count_exceptions(ValueError):
        pass
  ```
------------------------------------------------------------------------------------------------------------
## Gauges:
  - [Client library usage documentation for gauges: on Python](https://prometheus.io/docs/concepts/metric_types/)

  A gauge is a metric that represents a single numerical value that can arbitrarily go up and down.

  Gauges are typically used for measured values like temperatures or current memory usage, but also "counts" that can go up and down, like the number of concurrent requests.

  Gauges can go up and down.

  ```Python
    from prometheus_client import Gauge
    g = Gauge('my_inprogress_requests', 'Description of gauge')
    g.inc()      # Increment by 1
    g.dec(10)    # Decrement by given value
    g.set(4.2)   # Set to a given value
  ```

  There are utilities for common use cases:

  ```Python
    g.set_to_current_time()   # Set to current unixtime

    # Increment when entered, decrement when exited.
    @g.track_inprogress()
    def f():
      pass

    with g.track_inprogress():
      pass
  ```

  A Gauge can also take its value from a callback:

    d = Gauge('data_objects', 'Number of objects')
    my_dict = {}
    d.set_function(lambda: len(my_dict))

------------------------------------------------------------------------------------------------------------
## Histogram:
  - [Client library usage documentation for histograms on Python](https://prometheus.io/docs/concepts/metric_types/)
  
  A histogram samples observations (usually things like request durations or response sizes) and counts them in configurable buckets. It also provides a sum of all observed values.

  A histogram with a base metric name of <basename> exposes multiple time series during a scrape:

  cumulative counters for the observation buckets, exposed as <basename>_bucket{le="<upper inclusive bound>"}
  the total sum of all observed values, exposed as <basename>_sum
  the count of events that have been observed, exposed as <basename>_count (identical to <basename>_bucket{le="+Inf"} above)
  Use the histogram_quantile() function to calculate quantiles from histograms or even aggregations of histograms. A histogram is also suitable to calculate an Apdex score. When operating on buckets, remember that the histogram is cumulative. See histograms and summaries for details of histogram usage and differences to summaries.

  NOTE: Beginning with Prometheus v2.40, there is experimental support for native histograms. A native histogram requires only one time series, which includes a dynamic number of buckets in addition to the sum and count of observations. Native histograms allow much higher resolution at a fraction of the cost. Detailed documentation will follow once native histograms are closer to becoming a stable feature.
  

  Histograms track the size and number of events in buckets. This allows for aggregatable calculation of quantiles.

  ```Python
    from prometheus_client import Histogram
    h = Histogram('request_latency_seconds', 'Description of histogram')
    h.observe(4.7)    # Observe 4.7 (seconds in this case)
  ```

  The default buckets are intended to cover a typical web/rpc request from milliseconds to seconds. They can be overridden by passing buckets keyword argument to Histogram.

  There are utilities for timing code:

  ```Python
    @h.time()
    def f():
      pass

    with h.time():
      pass
  ```

  Current deployment.
  ```Python
  class PrometheusClient_Histogram:
    def __init__(self):
        #     # Start up the server to expose the metrics.
        self.registry = CollectorRegistry()
        self.g = Histogram(
                        'MEC_Dreamscape_job_last_success_unixtime_Histogram', 
                        'RTT data', 
                        labelnames=['Source_IP','Destination_IP'],
                        registry=self.registry   
                        )
            
    def Histogram_push(self, data):
        self.g.labels(data[0],data[1]).observe(data[2])
        push_to_gateway('15.181.163.0:9091',
                        job='MEC_Dreamscape', 
                        registry=self.registry)
                        
  
  prom_hist = PrometheusClient_Histogram()
  v_records = ['10.0.0.1', '10.0.0.2', time.time()]
  prom_hist.Histogram_push(v_records)

```


------------------------------------------------------------------------------------------------------------
  ## Summary
  - [Client library usage documentation for summaries on Python](https://prometheus.io/docs/concepts/metric_types/)

  Similar to a histogram, a summary samples observations (usually things like request durations and response sizes). While it also provides a total count of observations and a sum of all observed values, it calculates configurable quantiles over a sliding time window.

  A summary with a base metric name of <basename> exposes multiple time series during a scrape:

  streaming φ-quantiles (0 ≤ φ ≤ 1) of observed events, exposed as <basename>{quantile="<φ>"}
  the total sum of all observed values, exposed as <basename>_sum
  the count of events that have been observed, exposed as <basename>_count
  See histograms and summaries for detailed explanations of φ-quantiles, summary usage, and differences to histograms.

  Summaries track the size and number of events.

```Python
from prometheus_client import Summary
s = Summary('request_latency_seconds', 'Description of summary')
s.observe(4.7)    # Observe 4.7 (seconds in this case)
```
  There are utilities for timing code:
```Python
@s.time()
def f():
  pass

with s.time():
  pass
```
  The Python client doesn't store or expose quantile information at this time.
 
------------------------------------------------------------------------------------------------------------
## Info
Info tracks key-value information, usually about a whole target.

```Python
from prometheus_client import Info
i = Info('my_build_version', 'Description of info')
i.info({'version': '1.2.3', 'buildhost': 'foo@bar'})
```

------------------------------------------------------------------------------------------------------------
## Enum
Enum tracks which of a set of states something is currently in.

```Python
from prometheus_client import Enum
e = Enum('my_task_state', 'Description of enum',
        states=['starting', 'running', 'stopped'])
e.state('running')
```

------------------------------------------------------------------------------------------------------------
## Labels
All metrics can have labels, allowing grouping of related time series.

See the best practices on naming and labels.

Taking a counter as an example:

```Python
from prometheus_client import Counter
c = Counter('my_requests_total', 'HTTP Failures', ['method', 'endpoint'])
c.labels('get', '/').inc()
c.labels('post', '/submit').inc()
```
Labels can also be passed as keyword-arguments:

```Python
from prometheus_client import Counter
c = Counter('my_requests_total', 'HTTP Failures', ['method', 'endpoint'])
c.labels(method='get', endpoint='/').inc()
c.labels(method='post', endpoint='/submit').inc()
```
Metrics with labels are not initialized when declared, because the client can't know what values the label can have. It is recommended to initialize the label values by calling the .labels() method alone:

```Python
from prometheus_client import Counter
c = Counter('my_requests_total', 'HTTP Failures', ['method', 'endpoint'])
c.labels('get', '/')
c.labels('post', '/submit')
```
------------------------------------------------------------------------------------------------------------
## Exemplars

------------------------------------------------------------------------------------------------------------
# Exporting to a Pushgateway
The Pushgateway allows ephemeral and batch jobs to expose their metrics to Prometheus.

```Python
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()
g = Gauge('job_last_success_unixtime', 'Last time a batch job successfully finished', registry=registry)
g.set_to_current_time()
push_to_gateway('localhost:9091', job='batchA', registry=registry)
```

A separate registry is used, as the default registry may contain other metrics such as those from the Process Collector.

Pushgateway functions take a grouping key. push_to_gateway replaces metrics with the same grouping key, pushadd_to_gateway only replaces metrics with the same name and grouping key and delete_from_gateway deletes metrics with the given job and grouping key. See the Pushgateway documentation for more information.

instance_ip_grouping_key returns a grouping key with the instance label set to the host's IP address.

Handlers for authentication

If the push gateway you are connecting to is protected with HTTP Basic Auth, you can use a special handler to set the Authorization header.

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from prometheus_client.exposition import basic_auth_handler

```Python
def my_auth_handler(url, method, timeout, headers, data):
    username = 'foobar'
    password = 'secret123'
    return basic_auth_handler(url, method, timeout, headers, data, username, password)

registry = CollectorRegistry()

g = Gauge('job_last_success_unixtime', 'Last time a batch job successfully finished', registry=registry)
g.set_to_current_time()

push_to_gateway('localhost:9091', job='batchA', registry=registry, handler=my_auth_handler)
```

TLS Auth is also supported when using the push gateway with a special handler.

```Python
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from prometheus_client.exposition import tls_auth_handler


def my_auth_handler(url, method, timeout, headers, data):
    certfile = 'client-crt.pem'
    keyfile = 'client-key.pem'
    return tls_auth_handler(url, method, timeout, headers, data, certfile, keyfile)

registry = CollectorRegistry()

g = Gauge('job_last_success_unixtime', 'Last time a batch job successfully finished', registry=registry)

g.set_to_current_time()

push_to_gateway('localhost:9091', job='batchA', registry=registry, handler=my_auth_handler)
```





## Pretrained model
| Model | Download |
| ---     | ---   |
| Model-1 | [download]() |
| Model-2 | [download]() |
| Model-3 | [download]() |


## Directory Hierarchy
```
```
## Code Details
### Tested Platform
- software
  ```
  OS: Debian unstable (May 2021), Ubuntu LTS
  Python: 3.8.5 (anaconda)
  PyTorch: 1.7.1, 1.8.1
  ```
- hardware
  ```
  CPU: Intel Xeon 6226R
  GPU: Nvidia RTX3090 (24GB)
  ```
### Hyper parameters
```
```
## References
- [paper-1]()
- [paper-2]()
- [code-1](https://github.com)
- [code-2](https://github.com)
  
## License

## Citing
If you use xxx,please use the following BibTeX entry.
```
```
