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

Stage 2 - Re-evaluation of solutions in other SOWs

* Generate Latin Hypercube Sample of deeply uncertain parameters by running sh sample_parameters.sh. To replicate the analysis with the same SOWs as in the paper, skip this step and use the parameter_samples.txt file already found in this directory.

* Within the Generalized directory, create two directories: resim_objs and resim_cnstr

* Re-simulate all identified solutions in all generated SOW by running qsub resimulate_fish_game.sh

* The sampled SOWs that are used to demostrate dynamics in the paper are the following (with python indexing): 70, 212, 1280, and 3489. These will be different if you generated your own Latin Hypercube Sample, and need to be identified using the conditional equations mentioned in the paper

