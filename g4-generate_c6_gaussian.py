# converts an xyz config to a molpro config
# author: Henry Agnew 5/7/2021
import os
import sys
import json
import glob

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

# get basis set from filesystem. Data from https://grant-hill.group.shef.ac.uk/ccrepo/
def getBasis(atom):
    PP = None
    built_in = False

    if atom in basis_sets:
        atom_basis = basis_sets[atom]
        with open(f"../../gaussian_basis_sets/{atom}_{atom_basis}.txt", "r") as basis_file:
            implementation = basis_file.readlines()
            implementation = implementation[2:]
            # implementation = [line.lstrip() for line in implementation]
            implementation = ''.join(implementation)

        if atom_basis.endswith("-PP"):  # get matching pseudopotential
            potential_file = glob.glob(f"../../gaussian_basis_sets/pseudopotentials/{atom}_*.txt")
            # print(potential_file)
            with open(potential_file[0], "r") as potential_file:
                PP = potential_file.read()
    else:
        atom_basis = basis_sets["default"]
        implementation = f"{atom}  0\n{atom_basis}\n****"
        built_in = True
    result = {"atom": atom, "basis": atom_basis, "implementation": implementation, "PP": PP, "built_in":built_in}
    # print(result)
    return result


# generate input files
ii = 1
for i in range(6, 17):
    # print(d)
    d = f"{ii:05}"

    distance = "{:2}".format(i)
    os.makedirs(d, exist_ok=True)
    mon1, mon2 = sys.argv[1].split("-")
    mon1 = mon1.capitalize()
    mon2 = mon2.capitalize()

    if mon1 == mon2:
        basis_implementations = [getBasis(mon1)]
    else:
        basis_implementations = [getBasis(mon1), getBasis(mon2)]
    pseudopotentials = [basis["PP"]
                        for basis in basis_implementations if basis["PP"]]

    # determine gaussian basis mode
    basis_mode = "gen"
    if (len(pseudopotentials)):
        basis_mode = "genECP"  # use pseudopotential mode
    elif(all(basis["built_in"] for basis in basis_implementations)):
        basis_mode = "aug-cc-pv5z"  # all basis are prepackaged with gaussian
        basis_implementations = ""  # implementations are already in gaussian

    if (len(basis_implementations)):  # format basis_potentials
        implementations = [basis["implementation"] for basis in basis_implementations]
        basis_implementations = "\n" + "\n".join(implementations) + "\n"

    if(len(pseudopotentials)): # format pseudopotentials
        basis_implementations += "\n\n" + "\n".join(pseudopotentials) + "\n"

    # begin writting the output file
    TEMPLATE = f"""%nprocshared=4
%mem=4GB
%chk=tmp.chk
#p hf/{basis_mode} scf(xqc,MaxCycle=120)

Initial guess

{sum(charges)} 1
{mon1}  0.00000000   0.00000000    0.00000000
{mon2}  0.00000000   0.00000000   {distance}.00000000
{basis_implementations}
--Link1--
%nprocshared=4
%mem=4GB
%chk=tmp.chk
# lc-wpbe/{basis_mode} output=wfx scf(xqc,MaxCycle=150) geom=check guess=(read) 

postg calculation

{sum(charges)} 1
{basis_implementations}
input.wfx

"""
    with open(d + "/input", "w") as outfile:
        outfile.write(TEMPLATE)
    ii += 1
