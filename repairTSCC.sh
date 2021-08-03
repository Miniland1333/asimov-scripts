#! /bin/bash
# main script for generating ion-ion configurations
## uses g#-*.* subscripts
# author: Henry Agnew 5/7/2021

if [ $# -eq 0 ]; then
    echo "Usage: $0 ion-ion..."
    exit 1
fi

here=$(pwd)

for ionpair in $@; do
    cd ../2b_${ionpair}/notebook

    # prepare ion-charge calculations
    cp $here/../scripts/TSCC/* ..
    pwd
    cd $here
done
