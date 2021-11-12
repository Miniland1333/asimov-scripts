# converts an xyz config to a molpro config
# author: Henry Agnew 5/7/2021
import os
import sys
import json

if(len(sys.argv) != 2):
    print("Usage: ./g3_generate_inputs.py ionpair")
    exit()

# retrieves ion data from ion-pairs.json
with open("../../ion-pairs.json", "r") as read_file:
    pairs = json.load(read_file)
    pair = pairs[sys.argv[1]]
    charges = pair["charges"]
    ionsArray = sys.argv[1].split("-")

# retrieves basis set assignment for each atom from basis-sets.json
with open("../../basis-sets.json", "r") as read_file:
    basis_sets = json.load(read_file)


cwd_name =  os.path.basename(os.getcwd())
doIndividual = ""
# if in charge_calculations or testset_calculations, auto-generate configurations
if(cwd_name in ["charge_calculations", "testset_calculations"]):

    if(cwd_name == "charge_calculations"):
        if(charges[0] == charges[1]):
            print(f"Skipping charge_calculations: charges should be different")
            exit()
        doIndividual = "pop;\nindividual"

    ii = 1
    for i in range(5, 125, 5): # from 0.5 to 12 angstroms
        scientific_notation = "{:.14e}".format(i / 10.0)
        # print(scientific_notation)

        os.makedirs(f"{ii:05}", exist_ok=True)
        outputxyz = f"""2
{ii:05}
{ionsArray[0].capitalize().ljust(5)}0.00000000000000e+00   0.00000000000000e+00   0.00000000000000e+00
{ionsArray[1].capitalize().ljust(5)}{scientific_notation}   0.00000000000000e+00   0.00000000000000e+00"""

        # write input.xyz file
        with open(f"{ii:05}/input.xyz", "w") as output_file:
            output_file.write(outputxyz)
        ii += 1

# get configuration directories
directories = [i for i in sorted(os.listdir(".")) if (
    os.path.isdir(i) and not i.startswith("."))]


def getCore(input=False):
    if (not "core" in pair):
        return ""

    # print(input)
    if(type(input) == int):
        corevalue = pair["core"][input]
    else:
        corevalue = sum(pair["core"])

    if corevalue == 0:
        return f";core" # TODO behavior needs verification
    if corevalue:
        return f";core,{corevalue}"


def getBasis(key):
    monomers = key.split("-")
    if(monomers[0] == monomers[1]):
        monomers.pop()  # deduplicate monomers

    result = "default=av5z"
    for mon in monomers:
        element = mon.capitalize()
        if (element in basis_sets):
            result += f",{element}={basis_sets[element]}"

    return result


# generate input files
for d in directories:
    # print(d)
    with open(d + "/input.xyz", "r") as f:
        *_, mon1, mon2 = f.readlines()

    # mon1, mon2 = key.split("-")

    with open(d + "/input", "w") as outfile:

        basis = getBasis(sys.argv[1])

        HEADER = f"""memory,256,M

gthresh,zero=1.0e-16,twoint=3.0e-15,energy=1.0e-8,gradient=1.0e-6
gprint,orbitals

SYMMETRY,NOSYM
geomtyp=xyz
geometry={{
{mon1}{mon2}
}}

basis={{
{basis}
}}


CHARGE={charges[0]+charges[1]},SPIN=0
hf
{doIndividual}
{{ccsd(t),THRDEN=1.0e-9,THRVAR=1.0e-11{getCore()}}}

e_AB_AB_5z=energy

SYMMETRY,NOSYM
geomtyp=xyz
geometry={{
{mon1}
}}

basis={{
{basis}
}}


CHARGE={charges[0]},SPIN=0
hf
{{ccsd(t),THRDEN=1.0e-9,THRVAR=1.0e-11{getCore(0)}}}

e_A_A_5z=energy
"""

        FOOTER = f"""

SYMMETRY,NOSYM
geomtyp=xyz
geometry={{
{mon2}
}}

basis={{
{basis}
}}


CHARGE={charges[1]},SPIN=0
hf
{{ccsd(t),THRDEN=1.0e-9,THRVAR=1.0e-11{getCore(1)}}}

e_B_B_5z=energy
IE_tq=(e_AB_AB_5z-e_A_A_5z-e_B_B_5z)*tokcal

"""
        FOOTER_SAME = """
e_B_B_5z=e_A_A_5z
IE_tq=(e_AB_AB_5z-e_A_A_5z-e_B_B_5z)*tokcal

"""
        outfile.write(HEADER)

        # footer portion differs depending on whether ions are equivalent
        if charges[0] == charges[1] and ionsArray[0] == ionsArray[1]:
            outfile.write(FOOTER_SAME)
        else:
            outfile.write(FOOTER)
