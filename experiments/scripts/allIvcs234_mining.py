# mining all ivcs alg 2,3,4

__author__ = "Elaheh"
__date__ = "$Jan 20, 2018 7:59:03 PM$" 

 

import xml.etree.cElementTree as ET
import os, sys, shelve, shutil
 
RESULTS_DIR = 'all_ivcs_results4'
MINING_DIR = 'mining'
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

proof_time = []
uc_time = []
all_ivcs_time = []
all_ivcs_w_proof = []
uc_w_proof = []
timedout = []
numofivccalls = []
for file in models:
    try:
        tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_alg4_uc.xml'))
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
    except:
        print("runtime: "+file)
        uc_time.append(float('nan'))  
        pass    
    
    try:
        tree2 = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_alg4_runtimeAllIvcs.xml'))
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
timing_info ['all_ivcs_no_proof_alg4'] = all_ivcs_time
timing_info ['proof_time_alg4'] = proof_time
timing_info ['uc_time_no_proof_alg4'] = uc_time
timing_info ['uc_time_w_proof_alg4'] = uc_w_proof
timing_info ['all_ivcs_w_proof_alg4'] = all_ivcs_w_proof
timing_info ['num_of_ivc_calls_alg4'] = numofivccalls
timing_info ['timedout_alg4'] = timedout

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

  
for i, file in enumerate(models): 
    try:
        tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '.xml'))
    except:
        print("no xml: " + file)
        
    for elem in tree.iter(tag = 'NumberOfIVCs'):
        unm_of_ivcs.append(elem.text)
    ivc_info = shelve.open(os.path.join(MINING_DIR, file + '_ivc_info'))
    
    try:
        ivc_info ['number_of_ivc_sets_alg4'] = unm_of_ivcs[i]
    except:
        ivc_info ['number_of_ivc_sets_alg4'] =  'nan'
        print(file)
        print("unknown") 
    id = 0
    min = 10000
    for elem in tree.iter(tag = 'IvcSet'): 
        ivc_set = [] 
        for e in elem.findall('Ivc'): 
            ivc_set.append(e.text)
 
        ivc_info ['alg4_set' + str(id)] = ivc_set
        id += 1
        if len(ivc_set) < min:
            minimal = list(ivc_set)
            min = len(ivc_set)
    ivc_info ['minimum_alg4'] = minimal   
    ivc_info.close() 
    
timing_info['number_of_ivc_sets_alg4'] = unm_of_ivcs    
timing_info.close()

