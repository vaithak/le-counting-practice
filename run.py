import time
import argparse
import os
import json
import itertools
import time
import subprocess

timeout = 3600 * 2  # 2 hours
DEBUG = False


def execute_soln(soln_exec, instance):
    command = soln_exec.format(os.path.join("instances", instance))
    start_time = time.time()
    try:
        out_str = subprocess.run(command.split(' '), capture_output=True, text=True, timeout=timeout).stdout
        end_time = time.time() - start_time
    except:
        out_str = ""
        end_time = -1

    return out_str, end_time

def get_stats_from_instance_filename(filename):
    no_ext = filename.split('.', 1)[0]
    idx = int(no_ext.split('_')[-1])
    num_elem = int(no_ext.split('_')[-2])
    return num_elem, idx


soln_execs   = {'Telescopic-Product': 'solutions/telescopic-product/basic {0} SwapLinextSampler',
                'Decomposition-Telescopic-Product': 'solutions/telescopic-product/decomposition {0} SwapLinextSampler',
                'Decomposition-Telescopic-Product-Gibbs': 'solutions/telescopic-product/decomposition {0} GibbsLinextSampler',
                'Tootsie-pop': 'solutions/tpa/count {0}',
                # 'Exact-DP': 'solutions/lecount/lecount {0} --algorithm=dp',
                'Adaptive-Relaxation-Monte-Carlo': 'solutions/lecount/lecount {0} --algorithm=armc',
                'Variable-Elimination-via-Inclusion-Exclusion(exact)': 'solutions/lecount/lecount {0} --algorithm=veie',
                }


# values are prefixes of files
prob_classes = {'AvgDeg_3': 'avgdeg_3',
                'AvgDeg_5': 'avgdeg_5',    
                'Bipartite_0.2': 'bipartite_0.2',
                'Bipartite_0.5': 'bipartite_0.5',
                'Andes': 'bayesiannetwork_andes',
                'Diabetes': 'bayesiannetwork_diabetes',
                'Munin': 'bayesiannetwork_munin',
                'Link': 'bayesiannetwork_link',
                'Pigs': 'bayesiannetwork_pigs',
                }


sol_prob_pairs = list(itertools.product(soln_execs.keys(), prob_classes.keys()))
print("Number of possible pairs (soln, prob_class): ", len(sol_prob_pairs))


instance_files = {}
for file in os.listdir("instances"):
    for prob_class in prob_classes.keys():
        if file.startswith(prob_classes[prob_class]):
            if prob_class not in instance_files:
                instance_files[prob_class] = []
            
            instance_files[prob_class].append(file)

for prob_class in instance_files.keys():
    instance_files[prob_class] = sorted(instance_files[prob_class])

if DEBUG:
    with open("a.json", 'w') as f:
        json.dump(instance_files, f, indent=4, sort_keys=True)


# run solutions on all problems
for (soln, prob_class) in sol_prob_pairs:
    out_filename = f"results/{soln}_{prob_class}.json"
    results = []
    for instance_file in instance_files[prob_class]:
        if DEBUG:
            instance_file = "avgdeg_3_008_2.txt" # remove
        
        print("Soln: ", soln, ", prob_class: ", prob_class, ", instance_file: ", instance_file)
        
        out_str, exec_time = execute_soln(soln_execs[soln], instance=instance_file)
        if exec_time == -1:
            print("Timeout")
            if DEBUG:
                break # remove
            
            continue

        num_elem, idx = get_stats_from_instance_filename(instance_file) 
        res = {
                'num_elem': num_elem,
            'run_idx': idx,
            'out_str': out_str,
            'exec_time': exec_time
        }
       
        print(res)
        results.append(res)
        if DEBUG:
            break # remove
    
    # write curr results into file
    with open(out_filename, 'w') as f:
        json.dump({'results': results}, f, indent=4)

    if DEBUG:
        break #remove

