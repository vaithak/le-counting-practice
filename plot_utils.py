import numpy as np
import matplotlib.pyplot as plt
import json
import os
import matplotlib.cm as cm

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

soln_execs   = {
    'Telescopic-Product': 'solutions/telescopic-product/basic {0} SwapLinextSampler',
    'Decomposition-Telescopic-Product': 'solutions/telescopic-product/decomposition {0} SwapLinextSampler',
    'Decomposition-Telescopic-Product-Gibbs': 'solutions/telescopic-product/decomposition {0} GibbsLinextSampler',
    'Tootsie-pop': 'solutions/tpa/count {0}',
    'Adaptive-Relaxation-Monte-Carlo': 'solutions/lecount/lecount {0} --algorithm=armc',
    'Variable-Elimination-via-Inclusion-Exclusion(exact)': 'solutions/lecount/lecount {0} --algorithm=veie',
    'Volesti-SOB': 'solutions/volesti_lecount/volesti_lecount {0} sob',
    'Volesti-CG': 'solutions/volesti_lecount/volesti_lecount {0} cg',
    'Volesti-CB': 'solutions/volesti_lecount/volesti_lecount {0} cb',
    'Volesti-SOB-SVD': 'solutions/volesti_lecount/volesti_lecount {0} sob SVD',
    'Volesti-CG-SVD': 'solutions/volesti_lecount/volesti_lecount {0} cg SVD',
    'Volesti-CB-SVD': 'solutions/volesti_lecount/volesti_lecount {0} cb SVD',
    # 'Volesti-SOB-MIN-ELLIPSOID': 'solutions/volesti_lecount/volesti_lecount {0} sob MIN_ELLIPSOID',
    # 'Volesti-CG-MIN-ELLIPSOID': 'solutions/volesti_lecount/volesti_lecount {0} cg MIN_ELLIPSOID',
    # 'Volesti-CB-MIN-ELLIPSOID': 'solutions/volesti_lecount/volesti_lecount {0} cb MIN_ELLIPSOID',
}

colors = cm.rainbow(np.linspace(0, 1, len(soln_execs.keys())))
soln_colors_map = dict(zip(soln_execs.keys(), colors))

# filename is the json file containing results for a (soln_prob) pair
def plot_file(filename, ax, label, c):
    with open(filename, 'r') as f:
        data = json.load(f)
        data_arr = data['results']

    plt_data = {}
    for data_point in data_arr:
        if data_point['num_elem'] not in plt_data:
            plt_data[data_point['num_elem']] = []
        plt_data[data_point['num_elem']].append(data_point['exec_time'])

    for key in plt_data:
        plt_data[key] = sorted(plt_data[key])

    x = sorted(plt_data.keys())
    y = []
    for key in x:
        y.append(np.mean(plt_data[key]))

    ax.plot(x, y, '-o', label=label, color=c, markersize=8)

folder_name = "results"
def plot_problem(prob_key, ax):
    for file in os.listdir(folder_name):
        if file.endswith(prob_key + ".json"):
            algo, _ = file.split('_', 1)
            plot_file(os.path.join(folder_name, file), ax, algo, soln_colors_map[algo])

    ax.set_xscale('log', base=2)
    ax.set_yscale('log', base=2)

    ax.set_yticks([0.1, 1, 10.0, 60.0, 600.0])
    ax.set_yticklabels(['0.1 s', '1 s', '10 s', '1 min', '10 min'])
    ax.set_xticks([8, 16, 32, 64, 128, 256])
    ax.set_xticklabels([8, 16, 32, 64, 128, 256])

    ax.set_title(prob_key)


#
# parser = argparse.ArgumentParser()
# parser.add_argument('--json_file', type=str, required=True,
#                     help='json file containing the result data')
# args = parser.parse_args()
#
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# plot_results(args.json_file, ax)
# plt.show()

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

nrows, ncols = 3, 3
fig, axes2d = plt.subplots(nrows=nrows, ncols=ncols,
                           sharex=True, sharey=True,
                           figsize=(18,14))

prob_file_suffix = prob_classes.values()
probs_arr = sorted(prob_classes.keys())
idx = 0
for i, row in enumerate(axes2d):
    for j, cell in enumerate(row):
        plot_problem(probs_arr[idx], cell)
        idx = idx + 1
plt.xlim(8, 256)
plt.ylim(0.1, 10*60)

lines, labels = fig.axes[-1].get_legend_handles_labels()
fig.legend(lines, labels, loc='upper left', ncol=4, bbox_to_anchor=(0, 1))

plt.tight_layout(rect=(0, 0, 1, 0.95))
plt.savefig("out.png")
