#/bin/bash

source /etc/profile.d/modules.sh
module load python-2.7.5

python pareto.py ./Reoptimized/1540/sets/*.set -o 6-10 -e 5 0.005 1 1 5  --output Reoptimized_1540.resultfile --delimiter=" " --comment="#"
cut -d ' ' -f 7-11 Reoptimized_1540.resultfile >Reoptimized_1540.reference

python pareto.py ./Reoptimized/2832/sets/*.set -o 6-10 -e 5 0.005 1 1 5  --output Reoptimized_2832.resultfile --delimiter=" " --comment="#"
cut -d ' ' -f 7-11 Reoptimized_2832.resultfile >Reoptimized_2832.reference

python pareto.py ./Reoptimized/1253/sets/*.set -o 6-10 -e 5 0.005 1 1 5 --output Reoptimized_1253.resultfile --delimiter=" " --comment="#"
cut -d ' ' -f 7-11 Reoptimized_1253.resultfile >Reoptimized_1253.reference
