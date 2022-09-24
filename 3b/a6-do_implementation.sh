#! /bin/bash
# main script for implementing fit into MBX-tmp
## uses m#-*.* subscripts
# author: Henry Agnew 8/3/2021

if [ $# -ne 1 ]; then
    echo "Usage: $0 ion-ion"
    exit 1
fi
trap "kill 0" EXIT
set -e # causes script to exit if it encounters a nonzero exit code

ionpair=$1
scriptsDir=$(pwd)
# ionDir=~/projects/ion-ion/2b_${ionpair}
ionDir=~/projects/ion-ion/3b/na_cl/no_to_cutoff
echo $MBX_HOME

# add potential into MBX
module load gcc
# cd "$ionDir/notebook"
cd $ionDir
python3 $scriptsDir/m1-implement_potential.py $ionpair # || exit 1


#recompile MBX
cd "$MBX_HOME"
autoreconf -fi
./configure
make && make install

# # create test files
# mkdir -p "$ionDir/testMBX/"
# cd "$ionDir/testMBX"
# python3 $scriptsDir/m2-create_testMBX.py $ionpair
# head -4 ../training_set.xyz >input.xyz
# python3 $MBX_HOME/scripts/format_conversion/xyz2nrg.py input.xyz

# #running single-point tests and comparing to individual terms
# clear
# echo "Running $ionpair test TTM"
# $MBX_HOME/install/bin/single_point input.nrg ttm.json | tee single_point_test_TTM_MBX.txt
# # $MBX_HOME/install/bin/single_point input.nrg ttm.json
# head -2 ../notebook/ttm-nrg_fits/best_fit/individual_terms.dat | tee single_point_test_TTM.txt
# echo "Running $ionpair test for mb-nrg"
# $MBX_HOME/install/bin/single_point input.nrg mbx.json | tee single_point_test_MBX.txt
# # $MBX_HOME/install/bin/tests/test_single_point input.nrg mbx.json
# head -2 ../notebook/mb-nrg_fits/best_fit/individual_terms.dat | tee single_point_test.txt

# python3 $scriptsDir/m3-single_point_evaluation.py
# # rm single_point_test*.txt