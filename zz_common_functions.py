import json
import sys
import os

scriptsDir = os.environ.get('scriptsDir')
with open(f"${scriptsDir}/../ion-pairs.json", "r") as read_file:
    pairs = json.load(read_file)
    pair = pairs[sys.argv[1]]
    charges = pair["charges"]
    ionsArray = sys.argv[1].split("-")


def chargedMonomerName(index):
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

    return ionsArray[index] + charge
