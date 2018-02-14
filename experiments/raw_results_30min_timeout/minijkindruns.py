#minijkind runs in aivc
__author__ = "Elaheh"
__date__ = "$Jan 20, 2018 11:17:33 PM$"
# run after allIvcs_notimeout_mining.py 

import xml.etree.cElementTree as ET
import os, glob, sys, shelve, shutil
from operator import itemgetter

RESULTS_DIR = 'all_ivcs_results1' 
MINING_DIR = 'mining'
EXPERIMENTS_DIR = 'benchmarks'
SORTED_MODELS = 'list_of_sorted_models.txt'

models = []
with open (os.path.join(MINING_DIR, SORTED_MODELS)) as models_name:
    for line in models_name:
        if (line is not '\n'):
            models.append(line.strip('\n'))
models_name.close()  
adequate = 0
inadequate = 0
for indx, file in enumerate(models):
    runs = []
    ivc_info = shelve.open(os.path.join(MINING_DIR, file + '_ivc_info')) 
    try:
        tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_alg1_allivcs_inter_loop_runs.xml'))
        for elem in tree.iter(tag = 'Run'):
            t = ""
            s = ""
            times = elem.find('Time')
            sts = elem.find('Result')
            for e1 in times.iter('Time') :
                t = e1.text
            for e2 in sts.iter('Result'):
                s = e2.text
                if(s == 'VALID'):
                    adequate = adequate + 1
                else:
                    inadequate = inadequate + 1
            #runs.append({'status': s, 'time': t}) 
    except:
        #runs.append({'status': "", 'time': str(0)})
        pass
    ivc_info ['adeq_res_alg1'] = adequate
    ivc_info ['inadeq_res_alg1'] = inadequate
    ivc_info.close() 
 
  
    
#flag = 1    
for indx, file in enumerate(models):
    ivc_info = shelve.open(os.path.join(MINING_DIR, file + '_ivc_info')) 
    # loading miniaml IVCs from the complete execution
    count = int(ivc_info ['number_of_ivc_sets'])
    mivcs = []
    for x in range(0, count):
        mivcs.append(set(ivc_info ['set' + str(x)]))
      
    n = 0
    try: 
        tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_alg1_all_uc_minijkind.xml')) 
        for elem in tree.iter(tag = 'Results'):
            '''t = ""
            s = ""
            rid = ""
            times = elem.find('Time')
            for e1 in times.iter('Time') :
                t = e1.text''' 
            theset = set() 
            for e3 in elem.findall('IVC'):
                theset.add(e3.text) 
            if theset in mivcs:
                if (len(theset) > 0):
                    n = n + 1  
    except:
        #print(sys.exc_info()[0])
        #runs.append({'new_set': "", 'time': str(0), 'runid': str(0)}) 
        pass  
    if (n == 0):
        print (file)
    ivc_info ['discovered_mivcs_alg1'] = n
    ivc_info.close()
 
    
    
    
