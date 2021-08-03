#! /bin/bash
# main script for generating 
## uses h#-*.* subscripts
# author: Henry Agnew 5/17/2021

reuse=0
if [ $1 = "-r" ]; then 
    reuse=1
    shift
fi

if [ $# -eq 0 ]; then
    echo -e "Usage: $0 [-r] ion-ion...\n\t-r reuses previous calculations"
    exit 1
fi
trap "kill 0" EXIT
here=$(pwd)

if [ "$reuse" -ne 1 ]; then
    for ionpair in $@; do
        cd ../2b_${ionpair}
        mkdir -p c6_calculations
        cd c6_calculations

        echo "Setting up Gaussian C6 for ${ionpair}"
        python3 $here/g4-generate_c6_gaussian.py $ionpair

        for i in ?????/; do
            cd $i
            echo "Running gaussian $i"
            g09 < input > input.log
            echo "Extracting c6 $i"
            postg 0.0 0.0 input.wfx lcwpbe > output.postg
            cd ..
        done
        cd $here
    done
fi

for ionpair in $@; do
    cd ../2b_${ionpair}/c6_calculations

    echo "C6 results for ${ionpair}"
    python3 $here/h4-collect_c6_gaussian.py $ionpair

    cd $here
done