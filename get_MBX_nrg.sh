#!/bin/bash




MBX_HOME="$HOME/software/ion-ion_MBX/MBX-dev"

here=$PWD
for dir in ?????/; do
    cd $here/$dir
    echo "$PWD"
    python3 $MBX_HOME/scripts/format_conversion/xyz2nrg.py input.xyz
    $MBX_HOME/install/bin/single_point $PWD/input.nrg $here/../testMBX/mbx.json | sed 's/Energy= //' | tee energy.dat

    $MBX_HOME/install/bin/single_point $PWD/input.nrg $here/../testMBX/ttm.json | sed 's/Energy= //' > ttm_energy.dat
    cd ..
    wait
done