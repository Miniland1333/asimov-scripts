#! /bin/bash
# main script for verifying implementation matches MB-fit energy components
# author: Henry Agnew 2023-02-11

if [ $# -ne 1 ]; then
    echo "Usage: $0 ion-ion"
    exit 1
fi
trap "kill 0" EXIT
set -e # causes script to exit if it encounters a nonzero exit code

ionpair=$1
scriptsDir=$(pwd)
ionDir=~/projects/ion-ion/2b_${ionpair}
echo $MBX_HOME



#recompile MBX
cd "$MBX_HOME"
autoreconf -fi
./configure --enable-verbose --disable-optimization
make -j && make install

cd "$ionDir"
python3 $scriptsDir/p2-plot_MBX.py $ionpair