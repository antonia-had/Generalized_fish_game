#/bin/bash

source /etc/profile.d/modules.sh
module load python-2.7.5

python pareto.py ./Reoptimized/2343/sets/*.set -o 6-9 -e 5 0.005 1 1   --output Reoptimized_2343.resultfile --delimiter=" " --comment="#"
cut -d ' ' -f 7-10 Reoptimized_2343.resultfile >Reoptimized_2343.reference

python pareto.py ./Reoptimized/312/sets/*.set -o 6-9 -e 5 0.005 1 1   --output Reoptimized_312.resultfile --delimiter=" " --comment="#"
cut -d ' ' -f 7-10 Reoptimized_312.resultfile >Reoptimized_312.reference

python pareto.py ./Reoptimized/803/sets/*.set -o 6-9 -e 5 0.005 1 1   --output Reoptimized_803.resultfile --delimiter=" " --comment="#"
cut -d ' ' -f 7-10 Reoptimized_803.resultfile >Reoptimized_803.reference