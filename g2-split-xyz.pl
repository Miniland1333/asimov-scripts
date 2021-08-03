#! /usr/bin/perl
# This code splits a xyz with multiple h2o-cl dimer configurations into 
# individual xyz files and stores them in individual directories. 

use strict;
use warnings;

use POSIX('floor');

my @lines = (<STDIN>);

my $nat = 2;
my $nlxf = $nat + 2;

die unless (scalar @lines)%$nlxf == 0;

my $nc = (scalar @lines)/$nlxf;
my $nn = 5;
#my $nn = 1 + floor(log($nc)/log(10.0));
my $fmt = "%$nn.$nn" . 'd';

for (my $id = 0; $id < $nc; ++$id) {
    my $i0 = $nlxf*$id;
    my $fn = sprintf "$fmt", ($id + 1);
    mkdir "$fn" unless -d "$fn";
    open FH, ">$fn/input.xyz" or die;
        print FH $lines[$i0];
        printf FH "$fmt\n", ($id + 1);
        for (my $k = 2; $k < $nlxf; ++$k) {
            print FH $lines[$i0 + $k];
        }
    close FH;
}
