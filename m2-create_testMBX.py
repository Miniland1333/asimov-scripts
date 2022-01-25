import sys
import json

ionPair = sys.argv[1]

# retrieves ion data from ion-pairs.json
with open("../../ion-pairs.json", "r") as read_file:
    pairs = json.load(read_file)
    pair = pairs[sys.argv[1]]
    charges = pair["charges"]
    ionsArray = sys.argv[1].split("-")


def substitute(filename):
    with open(f"../../scripts/testMBX/{filename}", "r") as read_file:
        result = read_file.read()
        result = result.replace(
            'JSON_monomer1_SUBSTITUTION', chargedMonomerName(0))
        result = result.replace(
            'JSON_monomer2_SUBSTITUTION', chargedMonomerName(1))
    with open(filename, "w") as output_file:
        output_file.write(result)


def chargedMonomerName(index):
    charge = charges[index]
    if (charge == 0):
        charge = ""
    elif (charge == 1):
        charge = "+"
    elif (charge == -1):
        charge = "-"
    elif (charge > 0):
        charge = f"{charge}+"
    elif (charge < 0):
        charge = f"{abs(charge)}-"

    return ionsArray[index] + charge


# create mbx.json
substitute("mbx.json")
substitute("ttm.json")
