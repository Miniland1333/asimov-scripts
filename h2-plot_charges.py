# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import re


directories = [f"./charge_calculations/{i}" for i in sorted(os.listdir("./charge_calculations")) if (os.path.isdir(f"./charge_calculations/{i}"))]
natoms = 2

ionsArray = sys.argv[1].split("-")

plt.figure(dpi=300)
plt.title(f'{ionsArray[0].capitalize()}-{ionsArray[1].capitalize()} charges')
plt.xlabel('Distance (Angstorms)', color='#1C2833')
plt.ylabel('Charge', color='#1C2833')
distances = []
cation = []
anion = []
print(ionsArray)
for xyz in directories:
    with open(f"{xyz}/input.out", 'r') as infile:
        lines = infile.read()
        try:
            distance = re.search(f"(?<=\n {ionsArray[1].capitalize()})\s+\d\.\d+e[+-]\d+",lines).group()
            cation_charge = re.search(f"   1  {ionsArray[0].upper()}.*?\+ (.*)",lines).group(1)
            anion_charge = re.search(f"   2  {ionsArray[1].upper()}.*?\- (.*)",lines).group(1)

            distances.append(float(distance))
            cation.append(float(cation_charge))
            anion.append(float(f"-{anion_charge}"))
        except Exception as err:
            print(sys.argv[1], xyz, err)

plt.plot(distances, cation, label=f"{ionsArray[0].capitalize()}+")
plt.plot(distances, anion, label=f"{ionsArray[1].capitalize()}-")
# plt.axhline(y=0, color='b', linestyle='dashed')
# plt.axis([0.01* sigma,6 * sigma,-90,5])
plt.legend(loc='upper right')
plt.grid()
# plt.show()
plt.savefig('charge_configs.png')
print(f"Plotted {sys.argv[1]}")
