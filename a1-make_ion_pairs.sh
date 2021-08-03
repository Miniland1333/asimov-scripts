#! /bin/bash
# main script for generating ion-ion configurations
## uses g#-*.* subscripts
# author: Henry Agnew 5/7/2021

if [ $# -eq 0 ]; then
    echo "Usage: $0 ion-ion..."
    exit 1
fi

# generate jupyter notebook for each input argument pair
python3 ./g1-generate_notebooks.py $@
if [ $? -ne 0 ]; then
    exit 1
fi

here=$(pwd)

for ionpair in $@; do
    cd ../2b_${ionpair}/notebook

    # convert jupyter notebook into python script and run it for each ion pair
    jupyter nbconvert --to python 2b_${ionpair}_2b_ttm_and_mbnrg.ipynb
    python3 2b_${ionpair}_2b_ttm_and_mbnrg.py

    # prepare ion-charge calculations
    cp $here/../scripts/TSCC/* ..
    mkdir -p ../charge_calculations
    cd ../charge_calculations/
    python3 $here/g3-generate_inputs_5z.py $ionpair
    cd ../notebook/

    # prepare calculations for TSCC
    mkdir -p ../calculations
    cp training_configs.xyz ../calculations/
    cd ../calculations/
    pwd
    echo "Splitting configurations into directories..."
    $here/g2-split-xyz.pl <training_configs.xyz
    echo "Converting configs to molpro inputs..."
    python3 $here/g3-generate_inputs_5z.py $ionpair
    cd ../notebook/

    # generate testset calculations for TSCC
    cp $here/../scripts/TSCC/* ..
    mkdir -p ../testset_calculations
    cd ../testset_calculations/
    python3 $here/g3-generate_inputs_5z.py $ionpair

    cd $here
done
