#  This is meant to extract all-ivcs info

__author__ = "Elaheh"
__date__ = "$Aug 4, 2016 2:04:41 AM$"

import xml.etree.cElementTree as ET
import os, glob, sys, shelve, shutil
from operator import itemgetter

RESULTS_DIR = 'all_ivcs_results1' 
MINING_DIR = 'mining'
EXPERIMENTS_DIR = 'benchmarks'
SORTED_MODELS = 'list_of_sorted_models.txt' 

    
if not os.path.exists(RESULTS_DIR):
    print(RESULTS_DIR + " does not exist!")
    sys.exit(-1)

if os.path.exists(MINING_DIR):
    print(MINING_DIR + " already exists!")
    sys.exit(-1)

if not os.path.exists(EXPERIMENTS_DIR):
    print("'" + EXPERIMENTS_DIR + "' directory does not exist")
    sys.exit(-1)    

os.mkdir(MINING_DIR) 

#
# Gather name of the models
#
os.chdir(EXPERIMENTS_DIR)
lus_files = glob.glob("*.lus")
if len(lus_files) == 0:
    print("No Lustre files found in '" + EXPERIMENTS_DIR + "' directory")
    sys.exit(-1)
os.chdir("..") 
 
#
# Extract proof time
#
models = [] 
for file in lus_files: 
    try:
        tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_alg1_uc.xml'))
        for elem in tree.iter(tag = 'ProofTime'):
            models.append({'name': file, 'time': float(elem.text)})
    except: 
        print(file)
        #os.remove(os.path.join(EXPERIMENTS_DIR, file))
        pass

sorted_models = sorted(models, key=itemgetter('time')) 
sorted_models_mem = []
sorted_models_dsk = open (os.path.join(MINING_DIR, SORTED_MODELS), 'w')
#######################################################################
# the order of the file names will be used as x-axis in the graphs
# these files are sorted based on the runtime results in  SORT_BASE
#######################################################################
for pair in sorted_models:
    sorted_models_dsk.write(pair['name'])
    sorted_models_dsk.write('\n')
    sorted_models_mem.append(pair['name'])
sorted_models_dsk.close()


del sorted_models 
del models


#
# Start to Extract all timings
#

proof_time = []
uc_time = []
all_ivcs_time = []
all_ivcs_w_proof = []
uc_w_proof = []
timedout = []
numofivccalls = []
for file in sorted_models_mem:
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_alg1_uc.xml'))
    proof = 0.0
    for elem in tree.iter(tag = 'ProofTime'):
        proof = float(elem.text)
        proof_time.append(proof)
    for elem in tree.iter(tag = 'Runtime'):
        uc_w_proof.append(float(elem.text))
    uc = 0.0
    for elem in tree.iter(tag = 'UcRuntime'):
        uc = float(elem.text)
        uc_time.append(uc)    
        
    try:
        tree2 = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_alg1_runtimeAllIvcs.xml'))
        for elem in tree2.iter(tag = 'AllIvcRuntime'):
            all = (float(elem.text) + uc)
            all_ivcs_time.append(all)
            all_ivcs_w_proof.append(all + proof)
        for elem in tree2.iter(tag = 'Timedout'): 
            timedout.append(elem.text) 
        for elem in tree2.iter(tag = 'NumOfTimedOuts'): 
            numofivccalls.append(float(elem.text)) 
    except:
        all = (float('nan'))
        all_ivcs_time.append(float('nan'))
        all_ivcs_w_proof.append(float('nan'))
        numofivccalls.append(float('nan'))
        timedout.append('true')
        pass
        
timing_info = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 
timing_info ['all_ivcs_no_proof_alg1'] = all_ivcs_time
timing_info ['proof_time_alg1'] = proof_time
timing_info ['uc_time_no_proof_alg1'] = uc_time
timing_info ['uc_time_w_proof_alg1'] = uc_w_proof
timing_info ['all_ivcs_w_proof_alg1'] = all_ivcs_w_proof
timing_info ['num_of_ivc_calls_alg1'] = numofivccalls
timing_info ['timedout_alg1'] = timedout

del all_ivcs_time
del proof_time
del uc_time
del uc_w_proof

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

  
for i, file in enumerate(sorted_models_mem): 
    try:
        tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '.xml'))
    except:
        print("no xml: " + file)
        
    for elem in tree.iter(tag = 'NumberOfIVCs'):
        unm_of_ivcs.append(elem.text)
    ivc_info = shelve.open(os.path.join(MINING_DIR, file + '_ivc_info'))
    
    try:
        ivc_info ['number_of_ivc_sets_alg1'] = unm_of_ivcs[i]
    except:
        ivc_info ['number_of_ivc_sets_alg1'] =  'nan'
        print(file)
        print("unknown") 
    id = 0
    min = 10000
    for elem in tree.iter(tag = 'IvcSet'): 
        ivc_set = [] 
        for e in elem.findall('Ivc'): 
            ivc_set.append(e.text)
 
        ivc_info ['alg1_set' + str(id)] = ivc_set
        id += 1
        if len(ivc_set) < min:
            minimal = list(ivc_set)
            min = len(ivc_set)
    ivc_info ['minimum_alg1'] = minimal  
    ''' ivcuc=[]
    treeuc = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_alg1_uc.xml'))
    for ivc in treeuc.iter(tag = 'TRIVC'):
        ivcuc.append(ivc.text)
    ivc_info ['uc_input_for_ucbf_alg1'] = ivcuc'''
    ivc_info.close() 
    
timing_info['number_of_ivc_sets_alg1'] = unm_of_ivcs    
timing_info.close()

