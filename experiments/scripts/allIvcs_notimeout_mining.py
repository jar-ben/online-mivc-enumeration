# gathering all minimal Ivcs

__author__ = "Elaheh"
__date__ = "$Jan 21, 2018 10:55:07 AM$"

#  This is meant to extract all-ivcs info
# run after allIvcs234
 

import xml.etree.cElementTree as ET
import os, glob, sys, shelve, shutil
from operator import itemgetter

RESULTS_DIR = 'all_ivcs_results' 
MINING_DIR = 'mining'
EXPERIMENTS_DIR = 'benchmarks'
SORTED_MODELS = 'list_of_sorted_models.txt' 

    

    
if not os.path.exists(RESULTS_DIR):
    print(RESULTS_DIR + " does not exist!")
    sys.exit(-1)

if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exist! first run result_mining_allIvcs.py")
    sys.exit(-1)

#
# Load a list of sorted models into models[]
#    
models = []
with open (os.path.join(MINING_DIR, SORTED_MODELS)) as models_name:
    for line in models_name:
        if (line is not '\n'):
            models.append(line.strip('\n'))
models_name.close()  

 
#
# Start to Extract all timings
#

minimal = []

#
# Extract ivc sets info
#
'''
for i, file in enumerate(sorted_models_mem): 
    with open(os.path.join(RESULTS_DIR, file + '.xml'), 'a') as f:
        f.write('</Results>')
        f.close()
'''
unm_of_ivcs = []

  
for i, file in enumerate(models): 
    try:
        tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '.xml'))
    except:
        print("no xml: " + file)
        pass
        
    for elem in tree.iter(tag = 'NumberOfIVCs'):
        unm_of_ivcs.append(elem.text)
    ivc_info = shelve.open(os.path.join(MINING_DIR, file + '_ivc_info'))
    
    try:
        ivc_info ['number_of_ivc_sets'] = unm_of_ivcs[i]
    except:
        ivc_info ['number_of_ivc_sets'] =  'nan'
        print(file)
        print("unknown") 
        pass
    id = 0
    min = 10000
    for elem in tree.iter(tag = 'IvcSet'): 
        ivc_set = [] 
        for e in elem.findall('Ivc'): 
            ivc_set.append(e.text)
 
        ivc_info ['set' + str(id)] = ivc_set
        id += 1
        if len(ivc_set) < min:
            minimal = list(ivc_set)
            min = len(ivc_set)
    ivc_info ['minimum'] = minimal   
    ivc_info.close() 
     
