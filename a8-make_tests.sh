#! /bin/bash
# main script for implementing testcases for new potentials
## uses n#-*.* subscripts
# author: Henry Agnew 1/4/2022

if [ $# -ne 1 ]; then
    echo "Usage: $0 ion-ion"
    exit 1
fi
trap "kill 0" EXIT

ionpair=$1
scriptsDir=$(pwd)
ionDir=~/projects/ion-ion/2b_${ionpair}
echo $MBX_HOME
export scriptsDir

#recompile MBX
cd "$MBX_HOME"
module load gcc
./configure --enable-verbose --disable-optimization
make -j && make install

# create test files
echo "creating test files"
mkdir -p "$ionDir/testMBX/unittest"
cd "$ionDir/testMBX/unittest"
python3 $scriptsDir/n1-create_unittestXYZ.py $ionpair

python3 $MBX_HOME/scripts/format_conversion/xyz2nrg.py input.xyz

# running single-point debug output
echo "Generating debug single_point output for $ionpair"
$MBX_HOME/install/bin/single_point input.nrg ../mbx.json &>single_point.out

ln -s ../../notebook/config.ini .

# insert into disptools, bucktools, energy2b, and poly-holder-2b
python3 $scriptsDir/n2-implement_tests.py $ionpair

#recompile MBX
cd "$MBX_HOME"
module load gcc
./configure --disable-optimization 
make check
