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

## Reference commands:
- Add records to Prometheus Push Gateway
  ```
  registry = CollectorRegistry()
  g = Gauge('job_last_success_unixtime', 'Last time a batch job successfully finished', registry=registry)
  g.set_to_current_time()
  push_to_gateway('15.181.163.0:9091', job='pcap', registry=registry)
  ```
- for test
  ```
  python test.py
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
