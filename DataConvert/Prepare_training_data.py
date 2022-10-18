import sys
sys.path.append("museum_vis/")

from DataConvert.utils.data_utils import extract_rules
from DataConvert.utils.data_utils import generate_datasets

## 1. extract the CFG rules
extract_rules('DataConvert/sourcedata/data_log.json', 'DataConvert/trainingdata/rules-cfg1.txt')

## 2. generate the traning and testing datasets
generate_datasets('DataConvert/sourcedata/data_log.json', 'DataConvert/trainingdata/rules-cfg1.txt', 'DataConvert/trainingdata/')
