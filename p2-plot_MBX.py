# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import re
from mbfit.utils import system, files
from multiprocessing import Pool
import subprocess
import scipy.constants as constants

TEST_SET = "test_set.xyz"
# MBX_HOME = "/home/hagnew/software/ion-ion_MBX/DEBUG"
MBX_HOME = "/home/hagnew/software/mbx-6.5-pol100/debug_no_mpi/MBX_DEBUG"

def getMBXEnergy(d, json_file):

    subprocess.run([f"python3", f"{MBX_HOME}/scripts/format_conversion/xyz2nrg.py", "input.xyz"],cwd=d)
    energy = subprocess.run([f"{MBX_HOME}/install/bin/single_point", "input.nrg", f"{json_file}"],cwd=d, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    energy = energy.stdout
    lines = energy.split('\n')

    # MB-nrg
    poly = float(lines[291].split("Output energy: ")[1])
    disp = float(lines[438].split("Dispersion energy = ")[1])
    elec = float(lines[-5].split("Elec tot energy: ")[1])
    perm = float(lines[-4].split("Eperm: ")[1])
    ind = float(lines[-3].split("Eind: ")[1])
    total = float(lines[-2].split("Energy= ")[1])
    return [poly, disp, elec, perm, ind, total]

    # # TTM-nrg
    # rep = float(lines[445].split("Repulsion energy = ")[1])
    # disp = float(lines[415].split("Dispersion energy = ")[1])
    # elec = float(lines[-5].split("Elec tot energy: ")[1])
    # perm = float(lines[-4].split("Eperm: ")[1])
    # ind = float(lines[-3].split("Eind: ")[1])
    # total = float(lines[-2].split("Energy= ")[1])
    # return [rep, disp, elec, perm, ind, total]
        
# meant to be run in ionDir
ionPair = sys.argv[1]
ionsArray = ionPair.split("-")
MBX_ttm = []
MBX_mbnrg = []

plt.figure(1, clear=True, dpi=1000)
plt.title(f'{ionsArray[0].capitalize()}-{ionsArray[1].capitalize()} MB-nrg components')
plt.xlabel('Interatomic Distance (Angstorms)', color='#1C2833')
plt.ylabel('Energy (kcal/mol)', color='#1C2833')
distances = []
reference_energies = []
notebookDirectory = f"./notebook"

tokcal = 627.509
directories = [f"../2b_{ionPair}/testset_calculations/{i}" for i in sorted(os.listdir(
    f"../2b_{ionPair}/testset_calculations")) if (os.path.isdir(f"../2b_{ionPair}/testset_calculations/{i}"))]

for d in directories:
    reference = d + '/reference_energy.dat'
    xyz = d + '/input.xyz'
    if not os.path.isfile(reference):
        print("Config " + d + " has no output...")
        continue
    
    with open(reference) as infile:
        lines = infile.read()
        be = lines

    with open(xyz, 'r') as infile:
        lines = infile.read()
        try:
            distance = re.search(
                f"(?<=\de\+..\n{ionsArray[1].capitalize()})\s+\d\.\d+e[+-]\d+", lines).group()

            distances.append(float(distance))
            reference_energies.append(float(be.split()[0]))
        except Exception as err:
            print(ionPair, xyz, err)
    # MBX_ttm.append(getMBXEnergy(d,f"../../testMBX/ttm.json"))
    MBX_mbnrg.append(getMBXEnergy(d,f"../../testMBX/mbx.json"))
    
    

plt.scatter(distances, reference_energies,
            label="Reference Interaction Energy", marker="x")

# get training_set.xyz distances
training_distances = []
TEST_SET_FILE = f"../2b_{ionPair}/{TEST_SET}"
with open(f"../2b_{ionPair}/{TEST_SET}", 'r') as infile:
    lines = infile.readlines()
    for lindex, line in enumerate(lines):
        if (lindex % 4 != 3):
            continue
        distance = line.split()[1]
        training_distances.append(float(distance))


def getEvaluationEnergies(nrg_type):
    if(nrg_type != "ttm" and nrg_type != "mb" and nrg_type != "overTTM"):
        raise Exception('nrg_type must either be ttm, mb, or overTTM')
    fit_path = f"{notebookDirectory}/{nrg_type}-nrg_fits/best_fit/"
    correlation_file_path = f"{notebookDirectory}/eval_energies.dat"
    with open(correlation_file_path, "w") as correlation_file:
        if nrg_type == "ttm":
            system.call(f"{notebookDirectory}/ttm-nrg_fitting_code/bin/eval-2b-ttm", fit_path +
                    "ttm-nrg_params.dat", TEST_SET_FILE, out_file=correlation_file)
        elif nrg_type == "mb":
            system.call(f"{notebookDirectory}/mb-nrg_fitting_code/bin/eval-2b", fit_path +
                    "mbnrg.nc", TEST_SET_FILE, out_file=correlation_file)
        # elif nrg_type == "overTTM":
        #     fit_path = f"{notebookDirectory}/mb-nrg_fits_overTTM/best_fit/"
        #     system.call(f"{notebookDirectory}/mb-nrg_fitting_code/bin/eval-2b-over-ttm", fit_path +
        #             "mbnrg.nc", TEST_SET_FILE, out_file=correlation_file)
        else:   
            raise Exception('nrg_type must either be [ttm or mb]')
    # frame[...###]=           Calculated         Polynomials          Dispersion    Electrostatics (Permanent + Induced)
    _, calculated, polynomials, dispersion, electrostatics = np.genfromtxt(correlation_file_path, skip_header=1, unpack=True)
    return [calculated, polynomials, dispersion, electrostatics]

# get ttm and mbnrg
# ttm = getEvaluationEnergies("ttm")
# mbnrg = getEvaluationEnergies("mb")

# mbnrg = list(zip(*mbnrg))
# MBX_ttm = list(zip(*MBX_ttm))
MBX_mbnrg = list(zip(*MBX_mbnrg))

# plt.plot(distances, mbnrg[0],  label="MBnrg MB-Fit", linestyle="-.", alpha=0.7)
# plt.plot(distances, mbnrg[1],  label="MBnrg MB-Fit poly", linestyle="-.", alpha=0.7)
# plt.plot(distances, mbnrg[2],  label="MBnrg MB-Fit disp", linestyle="-.", alpha=0.7)
# plt.plot(distances, mbnrg[3],  label="MBnrg MB-Fit elec", linestyle="-.", alpha=0.7)
plt.plot(distances, MBX_mbnrg[5],  label="Interaction energy")
plt.plot(distances, MBX_mbnrg[0],  label="Polynomials", alpha=0.7)
plt.plot(distances, MBX_mbnrg[1],  label="Dispersion", alpha=0.7)
plt.plot(distances, MBX_mbnrg[2],  label="Total Electrostatics", alpha=0.7)
plt.plot(distances, MBX_mbnrg[3],  label="Permanent Electrostatics", linestyle='dashed', alpha=0.7)
plt.plot(distances, MBX_mbnrg[4],  label="Induced Electrostatics", linestyle='dashed', alpha=0.7)

coulomb = [(-constants.Avogadro / 4184 * constants.e **
    2 * 9e9) / (r * 1e-10) for r in distances] # contains J=>kcal and A=>m conversions
plt.plot(distances, coulomb, label="Coulomb Attraction", linestyle='dotted')

plt.legend(loc='upper right')
plt.grid()
plt.savefig(f'{notebookDirectory}/plotting_MBX_energies.png')
print(f"Plotted {ionPair}")


#     # Combined residuals
#     plt.figure(2, dpi=300)
#     plt.scatter(training_distances, Mmbnrg[0] - reference_energies,  label=f"MB-Fit {ionPair} residuals", alpha=0.7)
#     plt.scatter(training_distances, MBX_mbnrg[5] - reference_energies,  label=f"MB-nrg {ionPair} residuals", alpha=0.7)


# plt.legend(loc='upper right')
# plt.ylim(-0.5,0.5)
# plt.title(f'Residuals between mb-nrg fits and reference energies')
# plt.xlabel('Distance (Angstorms)', color='#1C2833')
# plt.ylabel('Energy (kcal/mol)', color='#1C2833')
# plt.grid()
# plt.savefig('../plotting_all_energies_residuals.png')
