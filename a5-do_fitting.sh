#! /bin/bash
# main script for fitting ttm and mb ion-ion configurations
## uses i#-*.* subscripts
# author: Henry Agnew 7/15/2021

if [ $# -eq 0 ]; then
    echo "Usage: $0 ion-ion [ion-ion ...]"
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
    echo "REMOVING OLD FITS!"
    rm -r ttm-nrg_fits/ mb-nrg_fits/
    # convert jupyter notebook into python script and run it for each ion pair
    jupyter nbconvert --to python 2b_${ionpair}_fitting.ipynb
    python3 2b_${ionpair}_fitting.py

    cd $here
done
