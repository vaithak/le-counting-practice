## Running and testing solutions
* First generate all instance problems and build the executables of the provided algorithms by running `make`.
* Next build executable of your custom algorithms and place them in the `solutions` directory. You custom executable should take the input file containing the poset as a command line input.
* Now there are three main python files for running, plotting and analyzing the solutions.
  - `run.py`: This file is for running combinations of algorithms and problem classes
    - All the algorithms executables that will be run are defined in the dict `soln_execs` - [link](https://github.com/vaithak/le-counting-practice/blob/master/run.py#L33). The keys of this dict are the name of the algorithms and the corresponding value is the command to run the executable of that algorithm, where {0} will be replaced by the input filename.
    - The problem classes that will be run for each algorithm are defined in the dict `prob_classes` - [link](https://github.com/vaithak/le-counting-practice/blob/master/run.py#L44).  
    - For each combination of (algorithm, problem_class), the results will be logged in a separate file in the `results` folder.  
      If a file already exists for a pair then it won't be run again. For example, if the `results` folder already contains a file `Tootsie-pop_AvgDeg_3.json` 
      , then the algorithm `Tootsie-Pop` won't be run again for the problem class `AvgDeg_3` (this is to ensure that one has moved the results someplace else and
      they don't get overwritten by mistake).
  - `plot_utils,py`: This file is for reading the logs from the results folder and plotting the results. This file also contains similar dicts for 
     problem classes and solutions. Simply run `python plot_utils.py`. 
  - `error_comp,py`: This file is for comparing results of two algorithms. One can specify the algo names here: [link](https://github.com/vaithak/le-counting-practice/blob/master/error_comp.py#L36). Then the script will read the result logs for the specified problem classes of both of these algorithms and calculate relative error between them.
  
<hr>  

# Counting Linear Extensions in Practice

The code used for the experiments in the IJCAI 2018 paper [A Scalable Scheme for Counting Linear Extensions](https://www.ijcai.org/proceedings/2018/0710.pdf) and AAAI 2018 paper [Counting Linear Extensions in Practice: MCMC versus Exponential Monte Carlo](https://tuhat.helsinki.fi/portal/services/downloadRegister/120857481/paper.pdf).

## COMPILING

The Makefile in the root can be used to compile all solutions and generate all
instances:

```$ make```

The running make in the subdirectories can be used to compile parts
selectively.

## DEPENDENCIES

Instance generation requires Python 3. The solutions require a version of the
g++ compiler that supports C++11. In addition, the LEcount solutions (Exact
Dynamic Programming and Adaptive Relaxation Monte Carlo) require Boost and GMP.

## USAGE

The instances are generated to instances/*.txt as adjacency matrices. The
draw.py script can be used to visualize them to instances/img/ (requires
GraphViz).

Each solution program in solutions/ takes the name of the adjacency matrix file
as the first command line argument, possibly followed by solution-specific
options, and outputs the estimate for the number of linear extensions. Some
solutions also write extra information to the standard error stream. All
solutions support partial orders with at most 512 elements.

### IJCAI 2018: A Scalable Scheme for Counting Linear Extensions

Relaxation Tootsie Pop:

```$ solutions/relaxation-tpa/count INSTANCE```

Trivial Relaxation Tootsie Pop:

```$ solutions/relaxation-tpa/trivial INSTANCE```

Telescopic Product:

```$ solutions/telescopic-product/decomposition INSTANCE GibbsLinextSampler```

Extension Tootsie Pop:

```$ solutions/extension-tpa/count INSTANCE```

Adaptive Relaxation Monte Carlo:

```$ solutions/lecount/lecount INSTANCE --algorithm=armc```

SAT Encodings #1 and #2:

These output a DIMACS CNF encoding for the instance, which can then be used as input for a SAT model counter (D4, sharpSAT and ApproxMC2 in the paper) to count the linear extensions.

```
$ solutions/sat/encoding.py INSTANCE 1
$ solutions/sat/encoding.py INSTANCE 2
```

### AAAI 2018: Counting Linear Extensions in Practice: MCMC versus Exponential Monte Carlo

Telescopic Product:

```$ solutions/telescopic-product/basic INSTANCE SwapLinextSampler```

Decomposition Telescopic Product:

```$ solutions/telescopic-product/decomposition INSTANCE SwapLinextSampler```

Decomposition Telescopic Product using the Gibbs sampler:

```$ solutions/telescopic-product/decomposition INSTANCE GibbsLinextSampler```

Tootsie Pop:

```$ solutions/tpa/count INSTANCE```

Exact Dynamic Programming:

```$ solutions/lecount/lecount INSTANCE --algorithm=dp```

Adaptive Relaxation Monte Carlo:

```$ solutions/lecount/lecount INSTANCE --algorithm=armc```

Variable Elimination via Inclusion-Exclusion (exact):

```$ solutions/lecount/lecount INSTANCE --algorithm=veie```
