import sys
import os
from os.path import expanduser

home = expanduser("~")

ionsDir = f"{home}/projects/ion-ion"
scriptsDir = os.environ.get('scriptsDir')

with open(f"{ionsDir}/ion-pairs.json", "r") as read_file:
    ionsArray = sys.argv[1].split("-")
    print(ionsArray[0], ionsArray[1])

    if ionsArray[0] == ionsArray[1]:
        filename = "unittest_single.xyz"
    else:
        filename = "unittest.xyz"
    print(filename)

    with open(f"{scriptsDir}/testMBX/{filename}", "r") as read_file:
        result = read_file.read()
        result = result.replace('A ', ionsArray[0].capitalize() + " ")
        result = result.replace('B ', ionsArray[1].capitalize() + " ")
        print(result)
    with open("input.xyz", "w") as output_file:
        output_file.write(result)
