# this script generates a jupyter notebook for a given ion-ion pair(s)
# author: Henry Agnew 5/7/2021
import json
import os
import sys

with open("../MBX_polarizabilities.json", "r") as read_file:
    polarizabilities = json.load(read_file)
def getPolarizability(monomer):
    # print(monomer, polarizabilities[monomer])
    return polarizabilities[monomer]


if __name__ == "__main__":
    #arguments specify the ion-ion pairs to generate
    if(len(sys.argv) < 2):
        print("Usage: ./i1_generate_fitting.py ion-ion...")

    input_pairs = sys.argv[1:]

    # generate jupyter notebook for each in ion-pairs.json using template
    with open("../ion-pairs.json", "r") as read_file:
        pairs = json.load(read_file)
        for i, key in enumerate(input_pairs):
            try:
                value = pairs[key]
            except KeyError as err:
                print(f"KeyError: {key} does not seem to be defined in ion-pairs.json")
                exit(1)

            # interpolate configuration into jupyter notebook template
            with open("../templates/template_2b_fitting.ipynb", "r") as read_file:

                mon1, mon2 = key.split("-")

                notebook = read_file.read()

                # get c6 from previous c6 calculations
                try:
                    with open(f"../2b_{key}/c6.out") as c6_file:
                        c6 = c6_file.readlines()
                        c6 = c6[-1]
                        c6 = c6.split(',')[1]
                        c6 = float(c6)
                except Exception as err:
                    print(f"Problem with c6: {err}")
                    exit(1)

                if not c6:
                    print(f"Problem with c6: c6 does not seem to be defined for {key}")
                    exit(1)
                
                if mon1 == mon2:
                    symmetries = ["A1", "A1"]
                else:
                    symmetries = ["A1", "B1"]

                # angstrom**6 * kcal/mol = bohr**6 * hartree/mol * (1 angstrom/0.529177249 bohr)**6 * (627.509474 kcal/hartree)
                c6 = c6 * (0.529177249 **6) * 627.509474 # conversion factor equal to 13.779303707
                c6 = "{:.4f}".format(c6)

                # Need escaped double quotes due to ipynb serialization
                notebook = notebook.replace('\\"JSON_NAMES_SUBSTITUTION\\"', str(value.get("names")))
                notebook = notebook.replace('\\"JSON_CHARGES_SUBSTITUTION\\"', str(value.get("charges")))
                notebook = notebook.replace('\\"JSON_SYMMETRY_SUBSTITUTION\\"', str(symmetries))
                notebook = notebook.replace('\\"JSON_distanceRange_SUBSTITUTION\\"', str(value.get("distanceRange")))
                notebook = notebook.replace('\\"JSON_C6_SUBSTITUTION\\"', c6) # in angstroms^6 * kcal/mol
                notebook = notebook.replace('\\"JSON_pol1_SUBSTITUTION\\"', str(getPolarizability(mon1)))
                notebook = notebook.replace('\\"JSON_pol2_SUBSTITUTION\\"', str(getPolarizability(mon2)))

                #substitute in monomers
                notebook = notebook.replace('JSON_monomer1_SUBSTITUTION', mon1)
                notebook = notebook.replace('JSON_monomer2_SUBSTITUTION', mon2)
                notebook = notebook.replace('JSON_MONOMER1_SUBSTITUTION', mon1.capitalize())
                notebook = notebook.replace('JSON_MONOMER2_SUBSTITUTION', mon2.capitalize())

                destinationPath = f"../2b_{key}/notebook"
                os.makedirs(destinationPath, exist_ok=True)
                with open(f"{destinationPath}/2b_{key}_fitting.ipynb", "w") as output_file:
                    output_file.write(notebook)
                    print(f"Generating notebook for {key}")
        # print(pairsArray)
