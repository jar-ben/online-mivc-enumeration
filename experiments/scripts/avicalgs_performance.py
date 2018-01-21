# performance analysis of aivc algs

__author__ = "Elaheh"
__date__ = "$Jan 20, 2018 11:52:43 PM$"

import os, sys, shelve
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from operator import itemgetter
import numpy as np
import statistics as stat
from mpl_toolkits.axes_grid1 import host_subplot
import xml.etree.cElementTree as ET
import mpl_toolkits.axisartist as AA 
  
MINING_DIR = 'mining'
ANALYSES_DIR = 'timing_analyses' 
TIMING_INFO = 'timing_info' 
SORTED_MODELS = 'list_of_sorted_models.txt' 
SLICES = 'numOfEq'
            
if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exists! first, try to run mining scripts.")
    sys.exit(-1)

if not os.path.exists(ANALYSES_DIR):
    os.mkdir(ANALYSES_DIR) 

#
# Load timing info
#
  
reader = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 

ucpr_time = reader['uc_time_w_proof_alg1']
proof_time = reader['proof_time_alg1']
uc_time = reader['uc_time_no_proof_alg1']
#must_time =  reader['must_no_proof']
#must_w_proof = reader['must_w_proof']
#ucbf = reader['ucbf']
#aivc = reader['all_ivcs_w_proof']
all_ivcs_timing_alg1 = reader['all_ivcs_no_proof_alg1']
num_of_ivcs_alg1 = reader ['number_of_ivc_sets_alg1']
numofivccalls_alg1 = reader ['num_of_ivc_calls_alg1']
timedout_alg1 = reader ['timedout_alg1']

all_ivcs_timing_alg2 = reader['all_ivcs_no_proof_alg2']
num_of_ivcs_alg2 = reader ['number_of_ivc_sets_alg2']
numofivccalls_alg2 = reader ['num_of_ivc_calls_alg2']
timedout_alg2 = reader ['timedout_alg2']

all_ivcs_timing_alg3 = reader['all_ivcs_no_proof_alg3']
num_of_ivcs_alg3 = reader ['number_of_ivc_sets_alg3']
numofivccalls_alg3 = reader ['num_of_ivc_calls_alg3']
timedout_alg3 = reader ['timedout_alg3']

all_ivcs_timing_alg4 = reader['all_ivcs_no_proof_alg4']
num_of_ivcs_alg4 = reader ['number_of_ivc_sets_alg4']
numofivccalls_alg4 = reader ['num_of_ivc_calls_alg4']
timedout_alg4 = reader ['timedout_alg4']

reader.close()


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
# Extract results
#
 
numb_of_mivcs_alg1 = []
ad_chk_alg1 = []
inadeq_chk_alg1 = []

numb_of_mivcs_alg2 = []
ad_chk_alg2 = []
inadeq_chk_alg2 = []

numb_of_mivcs_alg3 = []
ad_chk_alg3 = []
inadeq_chk_alg3 = []

numb_of_mivcs_alg4 = []
ad_chk_alg4 = []
inadeq_chk_alg4 = []
numofallmivcs=[]
for indx, model in enumerate(models):
    reader = shelve.open(os.path.join(MINING_DIR, model +  '_ivc_info'))  
    numb_of_mivcs_alg1.append(float(reader['discovered_mivcs_alg1']))
    ad_chk_alg1.append(float(reader ['adeq_res_alg1']))
    inadeq_chk_alg1.append(float(reader ['inadeq_res_alg1']))
    
    numb_of_mivcs_alg2.append(float(reader['discovered_mivcs_alg2']))
    ad_chk_alg2.append(float(reader ['adeq_res_alg2']))
    inadeq_chk_alg2.append(float(reader ['inadeq_res_alg2']))
    
    numb_of_mivcs_alg3.append(float(reader['discovered_mivcs_alg3']))
    ad_chk_alg3.append(float(reader ['adeq_res_alg3']))
    inadeq_chk_alg3.append(float(reader ['inadeq_res_alg3']))
    
    numb_of_mivcs_alg4.append(float(reader['discovered_mivcs_alg4']))
    ad_chk_alg4.append(float(reader ['adeq_res_alg4']))
    inadeq_chk_alg4.append(float(reader ['inadeq_res_alg4']))
    
    numofallmivcs.append(float(reader ['number_of_ivc_sets']))
    reader.close() 
    
print("num of mivcs discovered by algorithm1: " + str(sum(numb_of_mivcs_alg1)))
print("num of mivcs discovered by algorithm2: " + str(sum(numb_of_mivcs_alg2)))
print("num of mivcs discovered by algorithm3: " + str(sum(numb_of_mivcs_alg3)))
print("num of mivcs discovered by algorithm4: " + str(sum(numb_of_mivcs_alg4)))
ucpr_time = [float(x) for x in ucpr_time]
proof_time = [float(x) for x in proof_time]
uc_time = [float(x) for x in uc_time]

all_ivcs_timing_alg1 = [float(x) for x in all_ivcs_timing_alg1]
num_of_ivcs_alg1 = [float(x) for x in num_of_ivcs_alg1]
numofivccalls_alg1 = [float(x) for x in numofivccalls_alg1] 

all_ivcs_timing_alg2 = [float(x) for x in all_ivcs_timing_alg2]
num_of_ivcs_alg2 = [float(x) for x in num_of_ivcs_alg2]
numofivccalls_alg2 = [float(x) for x in numofivccalls_alg2] 

all_ivcs_timing_alg3 = [float(x) for x in all_ivcs_timing_alg3]
num_of_ivcs_alg3 = [float(x) for x in num_of_ivcs_alg3]
numofivccalls_alg3 = [float(x) for x in numofivccalls_alg3] 

all_ivcs_timing_alg4 = [float(x) for x in all_ivcs_timing_alg4]
num_of_ivcs_alg4 = [float(x) for x in num_of_ivcs_alg4]
numofivccalls_alg4 = [float(x) for x in numofivccalls_alg4] 

#
# Gather mining files for support
#  
'''
for indx, item in enumerate(aivc):
    if(item <= ucbf[indx]):
        print(models[indx])'''
#sys.exit(0)

# how many models terminate in each algorithm
term1 = 0
term2 = 0
term3 = 0
term4 = 0
term1_time = []
term2_time = []
term3_time = []
term4_time = []

for indx, item in enumerate(timedout_alg1):
    if(item == 'false'):
        term1 = term1 + 1
        term1_time.append(all_ivcs_timing_alg1[indx])
for indx, item in enumerate(timedout_alg2):
    if(item == 'false'):
        term2 = term2 + 1
        term2_time.append(all_ivcs_timing_alg2[indx])
for indx, item in enumerate(timedout_alg3):
    if(item == 'false'):
        term3 = term3 + 1
        term3_time.append(all_ivcs_timing_alg3[indx])
for indx, item in enumerate(timedout_alg4):
    if(item == 'false'):
        term4 = term4 + 1
        term4_time.append(all_ivcs_timing_alg4[indx])

print("algorithm 1 finished successfuly in 10 mins without timeout for " + str(term1) + " models")
print("algorithm 2 finished successfuly in 10 mins without timeout for " + str(term2) + " models")
print("algorithm 3 finished successfuly in 10 mins without timeout for " + str(term3) + " models")
print("algorithm 4 finished successfuly in 10 mins without timeout for " + str(term4) + " models")

print("\n\nalgorithm 1 average runtime for models that terminated in 10 min: " + str(np.nanmean(term1_time)))
print("algorithm 1 standard dv. runtime for models that terminated in 10 min: " + str(np.nanstd(term1_time)))
print("algorithm 2 average runtime for models that terminated in 10 min: " + str(np.nanmean(term2_time)))
print("algorithm 2 standard dv. runtime for models that terminated in 10 min: " + str(np.nanstd(term2_time)))
print("algorithm 3 average runtime for models that terminated in 10 min: " + str(np.nanmean(term3_time)))
print("algorithm 3 standard dv. runtime for models that terminated in 10 min: " + str(np.nanstd(term3_time)))
print("algorithm 4 average runtime for models that terminated in 10 min: " + str(np.nanmean(term4_time)))
print("algorithm 4 standard dv. runtime for models that terminated in 10 min: " + str(np.nanstd(term4_time)))
#
# Compute min, max, avg, std deviation storing them on all_ivcs_timing = []
# 


'''writer = open(os.path.join(ANALYSES_DIR, 'all_ivcs_timing_analyses.txt'), 'w')

writer.write('\nmin runtime of all-ivcs (without proof): ' + str(min(all_ivcs_timing)))
writer.write('\nmax runtime of all-ivcs: ' + str(max(all_ivcs_timing)))
writer.write('\nstdev runtime of all-ivcs: ' + str(np.nanstd(all_ivcs_timing)))
writer.write('\naverage runtime of all-ivcs: ' + str(np.nanmean(all_ivcs_timing)))  
writer.close()  '''


#
# Calculate all-ivcs overhead
# This shows what percentage of the overal runtime is because of all-ivcs comutation
# Formula:  overhead_percentage = 100 * (all-ivcs runtime/ Prooftime)
#

'''
    
overhead_ucbf = []
overhead_uc = []
overhead_all_ivcs = []
overhead_minimization = []
large_models = []
      
for i in range(len(ucbf)): 
    overhead_ucbf.append ((ucbf[i]-proof_time[i])/ proof_time[i])
    overhead_uc.append(uc_time[i]/ proof_time[i])
    overhead_all_ivcs.append(all_ivcs_timing[i]/ proof_time[i])
    if(proof_time[i] >= 6.0):
        large_models.append(all_ivcs_timing[i]/ proof_time[i])
        
'''         
#
# Visualize the results
#
LEGENDS =  ['JKind Verification',
            'Algorithm 1 [what is the name?]', 'Algorithm 2', 'Algorithm 3', 'Algorithm 4'
            ,'#of MIVCs discovered by Algorithm 1', '#of MIVCs discovered by Algorithm 2',
            '#of MIVCs discovered by Algorithm 3', '#of MIVCs discovered by Algorithm 4',
            '#of IVC reduction calls', '#of adequate results', '#of inadequate results',
            '#of all MIVCs']

# Build a list for x-axis
x_axis = []
for i in range(len(proof_time)):
    x_axis.append(i)
 

fig = plt.figure()
plt.subplots_adjust(hspace=0.1)
#ax = plt.subplot(111)  
host = host_subplot(111, axes_class=AA.Axes) 

part1 = host.twinx() 
offset = 60  
  
host.set_xlabel("Models")
host.set_ylabel("Runtime (sec)")
part1.set_ylabel("#of MIVCs") 

# Sort based on number of ivcs

'''aivc_dic = [] 
for indx, val in enumerate(numb_of_ivcs):
    aivc_dic.append({'id': indx, 'val': val})

sorted_dic = sorted(aivc_dic, key=itemgetter('val'))  
del aivc_dic 
sorted_all_ivcs = []
sorted_uc = []
sorted_proof = []
sorted_ucbf = []
sorted_numofivcs = []
for item in sorted_dic:
    #sorted_numofivcs.append(item['val'])
    sorted_uc.append(ucpr_time[item['id']])
    sorted_ucbf.append(ucbf[item['id']])
    sorted_proof.append(proof_time[item['id']])
    sorted_all_ivcs.append(aivc[item['id']])
del sorted_dic'''

#sorted based on aivc


'''numb_of_mivcs_alg4 
ad_chk_alg4 
inadeq_chk_alg4 
all_ivcs_timing_alg1   
numofivccalls_alg1'''
   
'''host.plot(x_axis, all_ivcs_timing_alg1,'rs', markersize=4, label=LEGENDS[1]) 
host.plot(x_axis, all_ivcs_timing_alg2,'g+', markersize=4, label=LEGENDS[2]) 
host.plot(x_axis, all_ivcs_timing_alg3,'mx', markersize=4, label=LEGENDS[3]) 
host.plot(x_axis, all_ivcs_timing_alg4, 'b', markersize=4, label=LEGENDS[4]) '''
part1.plot(x_axis, numofallmivcs, ':kd', markersize=4, label=LEGENDS[12]) 

part1.plot(x_axis, numb_of_mivcs_alg1, ':rs', markersize=4, label=LEGENDS[5]) 
part1.plot(x_axis, numb_of_mivcs_alg2, ':g+', markersize=8, label=LEGENDS[6]) 
part1.plot(x_axis, numb_of_mivcs_alg3, ':mx', markersize=7, label=LEGENDS[7]) 
part1.plot(x_axis, numb_of_mivcs_alg4, '--b', markersize=4, label=LEGENDS[8]) 
#par1.scatter(x_axis, sorted_numofivcs, marker='s', color='b', label=LEGENDS[4]) 
host.plot(x_axis, proof_time, ':k', markersize=5 , label=LEGENDS[0]) 

host.legend() 
host.set_yscale('log')
part1.set_yscale('log')
host.grid(True)
plt.show()

 
















'''# graph #3 sort with model size
eqsize = []

# Load a list of sorted models into models[]    
models = []
with open (os.path.join(MINING_DIR, SORTED_MODELS)) as models_name:
    for line in models_name:
        if (line is not '\n'):
            models.append(line.strip('\n'))
models_name.close()  


for model in models:
    tree = ET.ElementTree(file = os.path.join('numOfEq', model + '_NUMEQ.xml'))
    for elem in tree.iter(tag = 'InitialNumberOfEqs'):
        eqsize.append (int(elem.text))

eq_dic = [] 
for indx, val in enumerate(eqsize):
    eq_dic.append({'id': indx, 'val': val})

sorted_dic = sorted(eq_dic, key=itemgetter('val'))  
del eq_dic 
sorted_uc = []
sorted_e = []
sorted_all_ivcs = [] 
sorted_proof = []
sorted_ucbf = []
sorted_numofivcs = []
for item in sorted_dic:
    sorted_e.append(item['val'])
    sorted_ucbf.append(ucbf[item['id']])
    sorted_uc.append(ucpr_time[item['id']])
    sorted_all_ivcs.append(aivc[item['id']])
    sorted_proof.append(proof_time[item['id']])
    sorted_numofivcs.append(numb_of_ivcs[item['id']])
del sorted_dic

fig = plt.figure()
plt.subplots_adjust(hspace=0.1)  
    
host = host_subplot(111, axes_class=AA.Axes) 

par1 = host.twinx() 
par2 = host.twinx() 
offset = 60  
new_fixed_axis = par2.get_grid_helper().new_fixed_axis
par2.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par2,
                                        offset=(offset, 0))

par2.axis["right"].toggle(all=True)
 

host.set_xlabel("Models")
host.set_ylabel("Runtime (sec)")
par1.set_ylabel("#of IVCs") 
par2.set_ylabel("#of equations") 

host.plot(x_axis, sorted_all_ivcs, ':mx',  markersize=7 ,label=LEGENDS[0])
#host.plot(x_axis, sorted_ucbf, ':g',  markersize=2 , label=LEGENDS[1])
#host.plot(x_axis, sorted_uc, 'b+', markersize=8, label=LEGENDS[2])
host.plot(x_axis, sorted_proof,'b.', markersize=4, label=LEGENDS[3]) 
#par1.scatter(x_axis, sorted_numofivcs, marker='s', color='b', label=LEGENDS[4]) 
par1.plot(x_axis, sorted_numofivcs, 'r+' , markersize=6, label=LEGENDS[4]) 
par2.plot(x_axis, sorted_e, color='k', label='#of equations') 



host.legend() 
host.set_yscale('log')  
par2.set_yscale('log')
host.grid(True)
 
plt.show()'''

