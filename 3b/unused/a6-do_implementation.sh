#! /bin/bash
# main script for implementing fit into MBX-dev
## uses m#-*.* subscripts
# author: Henry Agnew 8/3/2021

if [ $# -ne 2 ]; then
    echo "Usage: $0 ion-ion subdirectory"
    exit 1
fi
trap "kill 0" EXIT
set -e # causes script to exit if it encounters a nonzero exit code

ionpair=$1
subdirectory=$2
scriptsDir=~/projects/ion-ion/scripts/3b
export scriptsDir
# ionDir=~/projects/ion-ion/2b_${ionpair}
ionDir=~/projects/ion-ion/3b/${ionpair}/${subdirectory}
echo $MBX_HOME

# add potential into MBX
module load gcc
# cd "$ionDir/notebook"
cd $ionDir
python3 $scriptsDir/m1-implement_potential.py $ionpair # || exit 1


#recompile MBX
cd "$MBX_HOME"
autoreconf -fi
./configure --disable-optimization 
make && make install

# create test files
mkdir -p "$ionDir/testMBX/"
cd "$ionDir/testMBX"
python3 $scriptsDir/m2-create_testMBX.py $ionpair
head -7 ../test_set_v2022-09-24.xyz >input.xyz
python3 $MBX_HOME/scripts/format_conversion/xyz2nrg.py input.xyz

#running single-point tests and comparing to individual terms
clear
echo "Running $ionpair test for mb-nrg"
$MBX_HOME/install/bin/single_point input.nrg mbx.json | tee single_point_test_MBX.txt
head -2 ../mb-nrg_fits/best_fit/individual_terms.dat | tee single_point_test.txt

python3 $scriptsDir/m3-single_point_evaluation.py
# rm single_point_test*.txt