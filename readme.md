# CS240
## 1.Doing
### 1.1 Training&&Optimize!
EE,1cSVM,isoForest: (time:sec)
```
For Test Set: err: 2149 right: 13853 rate 0.8657042869641295 Time: 36.188541412353516
For Test Set: err: 4626 right: 11376 rate 0.7109111361079865 Time: 62.57835841178894
For Test Set: err: 2581 right: 13421 rate 0.8387076615423072 Time: 428.6734094619751
```
### 1.2 real-time Detection System!
use Python API to parse DNS.qname

## 2. To Do:
### 2.1 Code Review
### 2.2 use Bloom-Filter? to "White List"


## 3.Finished 
### 3.1.Feature Generation
#### Data:
from [link](https://data.mendeley.com/datasets/mzn9hvdcxg/2)
#### Reference:
from [DNS_iFor](https://ieeexplore.ieee.org/document/8717806)
1. Total count of characters in FQDN 
2. Count of characters in sub-domain
3. count of uppercase characters 
4. count of numerical characters
5. Entropy
6. number of labels
7. maximum label length
8. average label length 

### 3.2 Modeling
EE OCSVM IF
