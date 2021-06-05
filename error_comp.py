import numpy as np
import json
import os


prob_classes = {
    'AvgDeg_3': 'avgdeg_3',
    'AvgDeg_5': 'avgdeg_5',
    'Bipartite_0.2': 'bipartite_0.2',
    'Bipartite_0.5': 'bipartite_0.5',
    'Andes': 'bayesiannetwork_andes',
    'Diabetes': 'bayesiannetwork_diabetes',
    'Munin': 'bayesiannetwork_munin',
    'Link': 'bayesiannetwork_link',
    'Pigs': 'bayesiannetwork_pigs',
}


def compare_results(res_1, res_2):
    m, M = np.inf, 0
    for i in range(min(len(res_1), len(res_2))):
        out_str_1, out_str_2 = res_1[i]['out_str'], res_2[i]['out_str']
        if len(out_str_1) < 2 or len(out_str_2) < 2:
            break
        out_str_1, out_str_2 = out_str_1[:-1], out_str_2[:-1]
        if out_str_1 == "inf" or out_str_2 == "inf":
            break

        curr_res = float(out_str_2)/float(out_str_1)
        m = min(m, curr_res)
        M = max(M, curr_res)

    return round(m, 2), round(M, 2)


algo_name_1 = "Adaptive-Relaxation-Monte-Carlo"
algo_name_2 = "Volesti-CB"

prob_cmp_res = {}
for prob in prob_classes.keys():
    filename_1 = os.path.join("results", algo_name_1 + "_" + prob + ".json")
    filename_2 = os.path.join("results", algo_name_2 + "_" + prob + ".json")

    results_1, results_2 = [], []
    with open(filename_1, 'r') as f:
        data = json.load(f)
        results_1 = data['results']
    with open(filename_2, 'r') as f:
        data = json.load(f)
        results_2 = data['results']

    prob_cmp_res[prob] = compare_results(results_1, results_2)
    # break

print(prob_cmp_res)

