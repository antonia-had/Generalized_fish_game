### Generalized_fish_game

Intended for use with the MOEAFramework, Borg and pareto.py. Licensed under the GNU Lesser General Public License.

Stage 0 - Set up

* Make sure you have the [MOEAFramework](http://www.moeaframework.org). Download the MOEAFramework-*-Demo.jar file and copy it to this directory.

* Download the [Borg](http://borgmoea.org/) source code and move files in this directory.

* Download [Pareto.py](https://github.com/matthewjwoodruff/pareto.py) and put it in this directory

* Within this directory create a directory called Generalized and inside it, create directories objs, sets, cnstrs, and runtime

Stage 1 - Optimization

* Run the parallel optimization by running qsub fish_game_opt_batch_script.pbs

* Get reference set and result file by running sh find_refSets.sh

* Visualize solutions on parallel axis plot by running parallel_coordinate.py 

Stage 2 - Re-evaluation in other SOW

* Generate Latin Hypercube Sample of deeply uncertain parameters by running sh sample_parameters.sh. To replicate the analysis with the same SOW as in the paper, skip this step and use the parameter_samples.txt file already found in this directory.
