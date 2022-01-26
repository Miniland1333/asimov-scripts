import sys
import os
import re
import json

scriptsDir = os.environ.get('scriptsDir')

# ionsDir = f"{home}/projects/ion-ion"
with open(f"{scriptsDir}/../ion-pairs.json", "r") as read_file:
    pairs = json.load(read_file)
    pair = pairs[sys.argv[1]]
    charges = pair["charges"]
    ionsArray = sys.argv[1].split("-")

with open("config.ini") as read_file:
    text = read_file.read()
    a = float(re.search(r"a = \[([\d.]*?)\]", text).group(1))
    c6 = float(re.search(r"c6 = \[([\d.]*?)\]", text).group(1))
    d6 = float(re.search(r"d6 = \[([\d.]*?)\]", text).group(1))


def chargedMonomerName(index, escape=False):
    charge = charges[index]
    if charge == 0:
        charge = ""
    elif charge == 1:
        charge = "+"
    elif charge == -1:
        charge = "-"
    elif charge > 0:
        charge = f"{charge}+"
    elif charge < 0:
        charge = f"{abs(charge)}-"
    if escape:
        charge = charge.replace("+", "\\+")

    return ionsArray[index] + charge


with open("single_point.out") as read_file:
    text = read_file.read()
    mon1 = chargedMonomerName(0, True)
    mon2 = chargedMonomerName(1, True)
    # print(rf"Entering get_2b_energy.*?\nDimer {mon1} -- {mon2}:[\s\S]*?\nOutput energy.*\n")
    matches = re.findall(rf"Entering get_2b_energy.*?\nDimer {mon1} -- {mon2}:[\s\S]*?\nOutput energy.*\n", text)

    # print(len(matches))
    if len(matches) >= 1:
        energy_2b = matches[0]  # Only want to first valid dimer
    else:
        sys.exit("Error: No matches found")

    mon1_grad = re.search(rf"Output gradients for \d monomers of type {mon1}:\n(.*) , ", energy_2b).group(1)
    mon2_grad = re.search(rf"Output gradients for \d monomers of type {mon2}:\n(.*) , ", energy_2b).group(1)
    energy = re.search(rf"Output energy: (.*)", energy_2b).group(1)
    # print(energy_2b)
    print(mon1_grad)
    print(mon2_grad)
    print(energy)
