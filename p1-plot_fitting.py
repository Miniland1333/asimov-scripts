# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import re
from mbfit.utils import system, files

TEST_SET = "test_set.xyz"

# meant to be run in scripts folder
for ionPair in sys.argv[1:]:
    ionsArray = ionPair.split("-")

    plt.figure(1, clear=True, dpi=300)
    plt.title(f'{ionsArray[0].capitalize()}-{ionsArray[1].capitalize()}')
    plt.xlabel('Distance (Angstorms)', color='#1C2833')
    plt.ylabel('Energy (kcal/mol)', color='#1C2833')
    distances = []
    reference_energies = []
    notebookDirectory = f"../2b_{ionPair}/notebook"

    emin1 = 0
    emin2 = 0
    emax = 200.0
    emax_exceeded = False
    tokcal = 627.509
    directories = [f"../2b_{ionPair}/testset_calculations/{i}" for i in sorted(os.listdir(
        f"../2b_{ionPair}/testset_calculations")) if (os.path.isdir(f"../2b_{ionPair}/testset_calculations/{i}"))]

    # find minimum binding energies
    print("Searching for lowest energy in ts...")
    for d in directories:
        log = d + '/input.out'
        xyz = d + '/input.xyz'
        if not os.path.isfile(log):
            print("Config " + d + " has no output...")
            continue
        with open(log, 'r') as ff, open(xyz, 'r') as fx:
            lines = ff.readlines()
            e1 = None
            e2 = None
            eTot = None
            e2b = None
            for line in lines:
                if line.strip().startswith("SETTING E_A_A_5Z"):
                    e1 = float(line.strip().split()[3].replace("D", "E"))
                elif line.strip().startswith("SETTING E_B_B_5Z"):
                    e2 = float(line.strip().split()[3].replace("D", "E"))
                elif line.strip().startswith("SETTING E_AB_AB_5Z"):
                    eTot = float(line.strip().split()[3].replace("D", "E"))
                elif line.strip().startswith("SETTING IE_TQ"):
                    e2b = float(line.strip().split()[3].replace("D", "E"))
            if e1 is None or e2 is None or eTot is None or e2b is None:
                print("Config " + d + " has output but something is messed up..")
                continue

            if e1 < emin1:
                emin1 = e1

            if e2 < emin2:
                emin2 = e2

            edef1 = (e1 - emin1)*tokcal
            edef2 = (e2 - emin2)*tokcal
            ie = e2b
            be = ie + edef1 + edef2

            if be > emax:
                emax_exceeded = True

            # if float(d[-5:].lstrip("0")) % 100 == 0:
                # print(d)

    for d in directories:
        log = d + '/input.out'
        xyz = d + '/input.xyz'
        if not os.path.isfile(log):
            print("Config " + d + " has no output...")
            continue
        with open(log, 'r') as ff, open(xyz, 'r') as fx:
            lines = ff.readlines()
            e1 = None
            e2 = None
            eTot = None
            e2b = None
            for line in lines:
                if line.strip().startswith("SETTING E_A_A_5Z"):
                    e1 = float(line.strip().split()[3].replace("D", "E"))
                elif line.strip().startswith("SETTING E_B_B_5Z"):
                    e2 = float(line.strip().split()[3].replace("D", "E"))
                elif line.strip().startswith("SETTING E_AB_AB_5Z"):
                    eTot = float(line.strip().split()[3].replace("D", "E"))
                elif line.strip().startswith("SETTING IE_TQ"):
                    e2b = float(line.strip().split()[3].replace("D", "E"))
            if e1 is None or e2 is None or eTot is None or e2b is None:
                print("Config " + d + " has output but something is messed up..")
                continue

            edef1 = (e1 - emin1)*tokcal
            edef2 = (e2 - emin2)*tokcal
            ie = e2b
            be = ie + edef1 + edef2

            if be > emax:
                continue

            with open(log, 'r') as infile:
                lines = infile.read()
                try:
                    distance = re.search(
                        f"(?<=\de\+..\n {ionsArray[1].capitalize()})\s+\d\.\d+e[+-]\d+", lines).group()
                    # cation_charge = re.search(f"   1  {ionsArray[0].upper()}.*?\+ (.*)",lines).group(1)
                    # anion_charge = re.search(f"   2  {ionsArray[1].upper()}.*?\- (.*)",lines).group(1)

                    distances.append(float(distance))
                    reference_energies.append(float(be))
                except Exception as err:
                    print(ionPair, xyz, err)
    with open(f'{notebookDirectory}/reference_energies.dat', 'w') as outfile:
        outfile.write('\n'.join([str(elem) for elem in reference_energies]))
    plt.scatter(distances, reference_energies,
                label="Binding Energies", marker="x")

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
            elif nrg_type == "overTTM":
                fit_path = f"{notebookDirectory}/mb-nrg_fits_overTTM/best_fit/"
                system.call(f"{notebookDirectory}/mb-nrg_fitting_code/bin/eval-2b-over-ttm", fit_path +
                        "mbnrg.nc", TEST_SET_FILE, out_file=correlation_file)
            else:   
                raise Exception('nrg_type must either be [ttm, mb, or overTTM]')
        # frame[...###]=           Calculated         Polynomials          Dispersion    Electrostatics (Permanent + Induced)
        _, calculated, polynomials, dispersion, electrostatics = np.genfromtxt(correlation_file_path, skip_header=1, unpack=True)
        return dispersion + electrostatics


    # get ttm and mbnrg
    ttm = getEvaluationEnergies("ttm")
    mbnrg = getEvaluationEnergies("mb")
    # mbnrg_overTTM = getEvaluationEnergies("overTTM")

    plt.plot(training_distances, ttm, label="TTM Disp+Elec", linestyle="--", alpha=0.7)
    plt.plot(training_distances, mbnrg,  label="MBnrg Disp+Elec", alpha=0.7)
    # plt.plot(training_distances, mbnrg_overTTM,  label="MBnrg overTTM Disp+Elec",linestyle="-.", alpha=0.7)
    # plt.axhline(y=0, color='b', linestyle='dashed')
    # plt.axis([0.01* sigma,6 * sigma,-90,5])
    plt.legend(loc='upper right')
    plt.grid()
    plt.savefig(f'{notebookDirectory}/plotting_all_energies.png')
    print(f"Plotted {ionPair}")


    # Combined residuals
    plt.figure(2, dpi=300)
    plt.scatter(training_distances, mbnrg - reference_energies,  label=f"{ionPair} residuals", alpha=0.7)


plt.legend(loc='upper right')
plt.ylim(-0.5,0.5)
plt.title(f'Residuals between mb-nrg fits and reference energies')
plt.xlabel('Distance (Angstorms)', color='#1C2833')
plt.ylabel('Energy (kcal/mol)', color='#1C2833')
plt.grid()
plt.savefig('../plotting_all_energies_residuals.png')
