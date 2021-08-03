#! /bin/bash
# main script for generating ion-ion configurations
## uses g#-*.* subscripts
# author: Henry Agnew 5/7/2021

if [ $# -eq 0 ]; then
    echo "Usage: $0 ion-ion..."
    exit 1
fi
trap "kill 0" EXIT

# generate jupyter notebook for each input argument pair
python3 ./i1-generate_fitting.py $@
if [ $? -ne 0 ]; then
    exit 1
fi

here=$(pwd)

for ionpair in $@; do
    cd ../2b_${ionpair}/notebook
    rm -r ttm-nrg_fits/
    # convert jupyter notebook into python script and run it for each ion pair
    jupyter nbconvert --to python 2b_${ionpair}_2b_fitting.ipynb
    python3 2b_${ionpair}_2b_fitting.py

    cd $here
done
