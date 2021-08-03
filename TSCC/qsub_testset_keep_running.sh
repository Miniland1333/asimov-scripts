#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Usage: $0 <N_initial> <last>"
  exit
fi

nin=$1

NQMAX=300
sysname=`basename $PWD`

if [ ! -d "testset_calculations" ]; then
  echo "Run in the main folder!"
  exit
fi

if [ ! -s "tscc.job" ]; then
  echo "tscc.job script not present!"
  exit
fi

WDIR=$PWD

nq=`qstat -u $USER | grep $USER | grep " Q " | grep "glean" | wc -l`
nq2=`qstat -u $USER | grep $USER | grep " R " | grep "glean" | wc -l`
nqtot=$(($nq + $nq2))

i2=$1
while [ $i2 -le $2 ]; do
  printf -v i "%05d" $i2
  if [ $nqtot -lt $NQMAX ]; then
    cd testset_calculations/$i
    if [ -f input.out ]; then
      last=`tail -n 1 input.out`
      if [ "$last" != " Molpro calculation terminated" ]; then
        if [ -f jobid.dat ]; then
          id=`cat jobid.dat`
          id="${id%.*}"
          qstat -u $USER > qq.out
          if grep "$id" qq.out | grep -q " C " || ! grep -q "$id" qq.out ; then
            echo "$i not finished. Relaunching it."
            cat $WDIR/tscc.job | sed "s/XXXXXX/test-$i-$sysname/g" > tscc.job
            qsub tscc.job > jobid.dat
          else
            echo "$i is still running or in the queue"
          fi
        else
          echo "$i has never been run. Submitting it."
          cat $WDIR/tscc.job | sed "s/XXXXXX/test-$i-$sysname/g" > tscc.job
          qsub tscc.job > jobid.dat
        fi
      else
        echo "$i is completed"
      fi
    else
      if [ -f jobid.dat ]; then
        id=`cat jobid.dat`
        id="${id%.*}"
        qstat -u $USER > qq.out
        if grep "$id" qq.out | grep -q " C " || ! grep -q "$id" qq.out ; then
          echo "$i not finished. Relaunching it."
          cat $WDIR/tscc.job | sed "s/XXXXXX/test-$i-$sysname/g" > tscc.job
          qsub tscc.job > jobid.dat
        else
          echo "$i is still running or in the queue"
        fi
      else
        echo "$i has never been run. Submitting it."
        cat $WDIR/tscc.job | sed "s/XXXXXX/test-$i-$sysname/g" > tscc.job
        qsub tscc.job > jobid.dat
      fi
    fi
    cd ../../
    i2=$(($i2 + 1)) 
  else
    sleep 301
  fi
  nq=`qstat -u $USER | grep $USER | grep " Q " | grep "glean" | wc -l`
  nq2=`qstat -u $USER | grep $USER | grep " R " | grep "glean" | wc -l`
  nqtot=$(($nq + $nq2))
  
done 

