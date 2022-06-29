#! /bin/bash
# main script for generating 
## uses h#-*.* subscripts
# author: Henry Agnew 5/17/2021

if [ $# -eq 0 ]; then
    echo "Usage: $0 ion-ion [ion-ion ...]"
    exit 1
fi
here=$(pwd)

for ionpair in $@; do
    cd ../../3b/3b_${ionpair}/calculations
    echo "Generating training set for ${ionpair}"
    python3 $here/h1-generate_ts.py "full_set.xyz"

    cd ..
    python3 $here/h2-decimate.py "full_set.xyz"
    mv "90_out.xyz" training_set.xyz
    mv "10_out.xyz" test_set.xyz

    cd $here
done

# plot training sets using matplotlib
# python3 $here/h3-plot_ts.py $@
