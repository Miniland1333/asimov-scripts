# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import scipy.constants as constants

if(len(sys.argv) < 2):
    print("Usage: ./h3-plot_ts.py ion-ion...")

xyzs = [{"pair": x, "file": f"../2b_{x}/training_set.xyz"}
        for x in sys.argv[1:]]
with open("../../ion-pairs.json", "r") as read_file:
    pairs = json.load(read_file)
natoms = 3
contains_attraction = False
contains_repulsion = False


plt.figure(dpi=300)
plt.title('Ion-Ion')
plt.xlabel('Distance (Angstroms)', color='#1C2833')
plt.ylabel('Interaction Energy (kcal/mol)', color='#1C2833') # TODO: Shouldn't this be binding energy?
plt.axhline(y=0, color='b', linestyle='dashed')
for xyz in xyzs:
    with open(xyz["file"], 'r') as f:
        pair = xyz["pair"]
        print(pair)
        if(pairs[pair]["charges"][0] * pairs[pair]["charges"][1] < 0):
            contains_attraction = True
        if(pairs[pair]["charges"][0] * pairs[pair]["charges"][1] > 0):
            contains_repulsion = True

        lines = f.readlines()
        energies = [float(elem.split()[0]) for index,
                    elem in enumerate(lines) if index % (natoms+2) == 1]
        distances = [float(elem.split()[1]) for index,
                     elem in enumerate(lines) if index % (natoms+2) == 3]

        plt.plot(distances, energies, label=xyz["pair"])
        #plt.axvline(x=sigma, color='g', linestyle='dashed', label='sigma = 0.3580nm')

# plot coulomb interaction

if(contains_attraction):
    coulomb = [(-constants.Avogadro / 4184 * constants.e **
            2 * 9e9) / (r * 1e-10) for r in distances] # contains J=>kcal and A=>m conversions
    plt.plot(distances, coulomb, label="Coulomb Attraction", linestyle='dotted')
if(contains_repulsion):
    coulomb = [(constants.Avogadro / 4184 * constants.e **
            2 * 9e9) / (r * 1e-10) for r in distances] # contains J=>kcal and A=>m conversions
    plt.plot(distances, coulomb, label="Coulomb Repulsion", linestyle='dotted')

plt.axis([0, 10, -200, 220])
plt.legend(loc='upper right')
plt.grid()
# plt.show()
plt.savefig('../3b_salts_plot.png')
