### Generalized_fish_game

Intended for use with the MOEAFramework, Borg and pareto.py. Licensed under the GNU Lesser General Public License.

Stage 0 - Set up

* Make sure you have the [MOEAFramework](http://www.moeaframework.org). Download the MOEAFramework-*-Demo.jar file and copy it to this directory.

* Download the [Borg](http://borgmoea.org/) source code and move files in this directory.

* Download [Pareto.py](https://github.com/matthewjwoodruff/pareto.py) and put it in this directory

* Within this directory create a directory called Generalized and inside it, create directories objs, sets, cnstrs, and runtime

Stage 1 - Optimization

* Run the parallel optimization by typing qsub fish_game_opt_batch_script.pbs