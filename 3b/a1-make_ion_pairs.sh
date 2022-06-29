#! /bin/bash
# main script for generating ion-ion configurations
## uses g#-*.* subscripts
# author: Henry Agnew 5/7/2021

if [ $# -eq 0 ]; then
    echo "Usage: $0 ion-ion [ion-ion ...]"
    exit 1
fi


here=$(pwd)

for ionpair in $@; do
    cd ../../3b/3b_${ionpair}/
    
    # prepare calculations for TSCC
    cp ../tscc.job .
    mkdir -p ./calculations
    cp training_v2022-04-04.xyz ./calculations/
    cd ./calculations/
    pwd
    echo "Splitting configurations into directories..."
    $here/g2-split-xyz.pl <training_v2022-04-04.xyz
    echo "Converting configs to molpro inputs..."
    for config in */; do
        cd $config
        tail -n 5 input.xyz > temp.xyz
        cat $here/input_top input.xyz $here/input_bottom > input
        rm temp.xyz
        cd ..
    done 

    cd $here
done
