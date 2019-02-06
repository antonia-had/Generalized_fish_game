### Generalized_fish_game

Intended for use with the MOEAFramework, Borg and pareto.py. Licensed under the GNU Lesser General Public License.

Stage 0 - Set up

* Make sure you have the [MOEAFramework](http://www.moeaframework.org). Download the MOEAFramework-*-Demo.jar file and copy it to this directory.

* Download the [Borg](http://borgmoea.org/) source code and move files in this directory.

* Download [Pareto.py](https://github.com/matthewjwoodruff/pareto.py) and put it in this directory

* Within this directory create a directory called Generalized and inside it, create directories objs, sets, cnstrs, and runtime

Stage 1 - Optimization

* Run the parallel optimization by running "qsub fish_game_opt_batch_script.pbs"

* Get reference set and result file by running "sh find_refSets.sh". Notice the epsilon values used here, if you'd like a richer set of solutions, you should reduce the epsilon values for each objective. 

* Visualize solutions on parallel axis plot by running parallel_coordinate.py 

Stage 2 - Re-evaluation of solutions in other SOWs

* Generate Latin Hypercube Sample of deeply uncertain parameters by running "sh sample_parameters.sh". To replicate the analysis with the exact same SOWs as in the paper, skip this step (and use the parameter_samples.txt file already found in this directory).

* Within the Generalized directory, create two directories: resim_objs and resim_cnstr

* Re-simulate all identified solutions in all generated SOW by running "qsub resimulate_fish_game.sh". This will resimulate all identified solutions in all sampled SOWs. 

* To visualize how the entire sets of solutions shift under different SOWs, run scatter_uncertain_SOW.py. This file evaluates all the SOWs sampled and sorts them into stable and unstable, as well as calculate their distance from the base SOW. In the figure in the paper, the SOWs visualized are: Orange - Closest stable SOW, Green - Most distant stable SOW, Red - Unstable without deterministic extinction (closest), Brown - Unstable with deterministic extinction (furthest away from inequality). 
