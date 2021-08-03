#! /bin/bash
# author: Henry Agnew 5/19/2021

if [ $# -eq 0 ]; then
    echo "Usage: $0 ion-ion..."
    exit 1
fi
here=$(pwd)

for ionpair in $@; do
    IFS=- read mon1 mon2 <<< "$ionpair"
    if [ "$mon1" = "$mon2" ]; then
        echo "Skipping since $mon1 == $mon2"
        continue;
    fi
    
    cd ../2b_${ionpair}
    python3 $here/h2-plot_charges.py ${ionpair}

    cd $here
done
