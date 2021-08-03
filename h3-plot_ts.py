# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
import numpy as np
import sys

if(len(sys.argv) < 2):
    print("Usage: ./h2-plot_ts.py ion-ion...")

xyzs = [{"pair": x, "file": f"../2b_{x}/training_set.xyz"} for x in sys.argv[1:]]
natoms = 2

plt.figure(dpi=300)
plt.title('Ion-Ion')
plt.xlabel('Distance (Angstorms)', color='#1C2833')
plt.ylabel('Interaction Energy (kcal/mol)', color='#1C2833')
plt.axhline(y=0, color='b', linestyle='dashed')
for xyz in xyzs:
    with open(xyz["file"], 'r') as f:
        print(xyz["pair"])
        lines = f.readlines()
        energies=[float(elem.split()[0]) for index, elem in enumerate(lines) if index % (natoms+2)==1]
        distances=[float(elem.split()[1]) for index, elem in enumerate(lines) if index % (natoms+2)==3]
        
        plt.plot(distances,energies, label=xyz["pair"])
        #plt.axvline(x=sigma, color='g', linestyle='dashed', label='sigma = 0.3580nm')

# plt.axis([0.01* sigma,6 * sigma,-90,5])
plt.legend(loc='upper right')
plt.grid()
# plt.show()
plt.savefig('../salts_plot.png')
