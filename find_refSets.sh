#/bin/bash

source /etc/profile.d/modules.sh
module load python-2.7.5

python pareto.py ./Generalized/sets/*.set -o 6-10 -e 5 0.005 1 1 5   --output Generalized.resultfile --delimiter=" " --comment="#"
cut -d ' ' -f 7-11 Generalized.resultfile >Generalized.reference
