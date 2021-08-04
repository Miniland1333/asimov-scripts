#! /bin/bash
# main script for implementing fit into MBX-tmp
## uses m#-*.* subscripts
# author: Henry Agnew 8/3/2021

if [ $# -ne 1 ]; then
    echo "Usage: $0 ion-ion"
    exit 1
fi
trap "kill 0" EXIT

ionpair=$1
scriptsDir=$(pwd)
ionDir=~/projects/ion-ion/2b_${ionpair}
MBX_Dir=~/codes/MBX-tmp

# add potential into MBX
module load gcc
cd "$ionDir/notebook"
python3 $scriptsDir/m1-implement_potential.py $ionpair

#recompile MBX
cd "$MBX_Dir/build"
make install

# create test files
mkdir -p "$ionDir/testMBX/"
cd "$ionDir/testMBX"
python3 $scriptsDir/m2-create_testMBX.py $ionpair
head -4 ../training_set.xyz >input.xyz
python3 ~/codes/MBX-tmp/scripts/format_conversion/xyz2nrg.py input.xyz

#running single-point tests and comparing to individual terms
clear
echo "Running test for mb-nrg_overTTM"
$MBX_Dir/install/bin/tests/test_single_point input.nrg mbx.json
head -2 ../notebook/mb-nrg_fits_overTTM/best_fit/individual_terms.dat
$MBX_Dir/install/bin/tests/test_single_point input.nrg ttm.json
head -2 ../notebook/ttm-nrg_fits/best_fit/individual_terms.dat