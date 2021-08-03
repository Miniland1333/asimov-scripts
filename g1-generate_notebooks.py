# this script generates a jupyter notebook for a given ion-ion pair(s)
# author: Henry Agnew 5/7/2021
import json
import os
import sys

if __name__ == "__main__":
    #arguments specify the ion-ion pairs to generate
    if(len(sys.argv) < 2):
        print("Usage: ./g1_generate_notebooks.py ion-ion...")

    input_paris = sys.argv[1:]

    # generate jupyter notebook for each in ion-pairs.json using template
    with open("../ion-pairs.json", "r") as read_file:
        pairs = json.load(read_file)
        for i, key in enumerate(input_paris):
            try:
                value = pairs[key]
            except KeyError as err:
                print(f"KeyError: {key} does not seem to be defined in ion-pairs.json")
                exit(1)

            # interpolate configuration into jupyter notebook template
            with open("../templates/template_2b_ttm_and_mbnrg.ipynb", "r") as read_file:

                mon1, mon2 = key.split("-")

                notebook = read_file.read()

                if mon1 == mon2:
                    symmetries = ["A1", "A1"]
                else:
                    symmetries = ["A1", "B1"]

                # Need escaped double quotes due to ipynb serialization
                notebook = notebook.replace('\\"JSON_NAMES_SUBSTITUTION\\"', str(value.get("names")))
                notebook = notebook.replace('\\"JSON_CHARGES_SUBSTITUTION\\"', str(value.get("charges")))
                notebook = notebook.replace('\\"JSON_SYMMETRY_SUBSTITUTION\\"', str(symmetries))
                notebook = notebook.replace('\\"JSON_distanceRange_SUBSTITUTION\\"', str(value.get("distanceRange")))

                #substitute in monomers
                notebook = notebook.replace('JSON_monomer1_SUBSTITUTION', mon1)
                notebook = notebook.replace('JSON_monomer2_SUBSTITUTION', mon2)
                notebook = notebook.replace('JSON_MONOMER1_SUBSTITUTION', mon1.capitalize())
                notebook = notebook.replace('JSON_MONOMER2_SUBSTITUTION', mon2.capitalize())

                destinationPath = f"../2b_{key}/notebook"
                os.makedirs(destinationPath, exist_ok=True)
                with open(f"{destinationPath}/2b_{key}_2b_ttm_and_mbnrg.ipynb", "w") as output_file:
                    output_file.write(notebook)
                    print(f"Generating notebook for {key}")
        # print(pairsArray)
