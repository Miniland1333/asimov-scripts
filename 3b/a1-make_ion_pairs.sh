#! /bin/bash
# main script for generating ion-ion configurations
## uses g#-*.* subscripts
# author: Henry Agnew 5/7/2021

if [ $# -ne 1 ]; then
    echo "Usage: $0 training_configs.xyz"
    exit 1
fi


here=$(pwd)
scriptsDir=~/projects/ion-ion/scripts/3b

# for ionpair in $@; do
#     cd ../../3b/3b_${ionpair}/
    
    # prepare calculations for TSCC
cp ../tscc.job .
mkdir -p ./calculations
cp $1 ./calculations/
cd ./calculations/
pwd
echo "Splitting configurations into directories..."
$scriptsDir/g2-split-xyz.pl < $1
echo "Converting configs to molpro inputs..."
for config in */; do
    cd $config
    tail -n 5 input.xyz > temp.xyz
    cat $scriptsDir/input_top input.xyz $scriptsDir/input_bottom > input
    rm temp.xyz
    cd ..
done 

    # cd $here
# done
