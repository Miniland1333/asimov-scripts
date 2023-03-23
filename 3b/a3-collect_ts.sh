#! /bin/bash
# main script for generating 
## uses h#-*.* subscripts
# author: Henry Agnew 5/17/2021

here=$(pwd)
scriptsDir=~/projects/ion-ion/scripts/3b

# for ionpair in $@; do
#     cd ../../3b/3b_${ionpair}/calculations
#     echo "Generating training set for ${ionpair}"

if [[ -d calculations/ ]]
then
    cd ./calculations/ || exit
    python3 $scriptsDir/h1-generate_ts.py "full_set.xyz"
    cd ..
else
    echo "Can't find ./calculations/ directory"
    exit 1
fi


python3 $scriptsDir/h2-decimate.py "full_set.xyz"
mv "90_out.xyz" training_set.xyz
mv "10_out.xyz" test_set.xyz

#     cd $here
# done

# plot training sets using matplotlib
# python3 $here/h3-plot_ts.py $@
