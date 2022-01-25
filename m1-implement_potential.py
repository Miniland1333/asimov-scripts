import mbfit
import sys
import json
import os


dim_settings = "dimer_settings.ini"
config = "config.ini"
ionPair = sys.argv[1]
mon_ids = ionPair.split("-")

# retrieves ion data from ion-pairs.json
with open("../../ion-pairs.json", "r") as read_file:
    pairs = json.load(read_file)
    pair = pairs[sys.argv[1]]
    charges = pair["charges"]
    ionsArray = sys.argv[1].split("-")

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

mon_ids = [chargedMonomerName(0), chargedMonomerName(1)]
print(mon_ids)

mbnrg_fits_directory = "mb-nrg_fits_overTTM"
# MBX_path = os.environ.get('MBX_HOME') TODO re-enable this
MBX_path = "/home/hagnew/software/ion-ion_MBX/MBX-dev"

# print(MBX_path)
mbfit.generate_MBX_files(dim_settings, config, mon_ids, 0,
                                     do_ttmnrg=True,
                                     MBX_HOME = MBX_path, version = "v1")

mbfit.generate_MBX_files(dim_settings, config, mon_ids, 9,
                                     do_ttmnrg=False, mbnrg_fits_path=mbnrg_fits_directory,  
                                     MBX_HOME = MBX_path, version = "v1")

# Check if manual implementation required (due to the file being formatted)
with open("./MBX_files/MBX_cpp_code.txt") as cpp_code:
    cpp_text = cpp_code.read()

#grab CPP code from MBX_cpp_code.txt, and grab the mbnrg section
import re
match = re.search("^\/\/ SECTION CONSTRUCTOR\n\/\/ mbnrg_2b_(.*?)\n([\s\S]*?    } \/\/ end if mon1.*\n)",cpp_text)
destination_file = f"mbnrg_2b_{match.group(1)}"
destination_file_path = f"{MBX_path}/src/potential/2b/{destination_file}"
code_to_insert = match.group(2)
# print(destination_file)
with open(destination_file_path, "r") as cpp_code:
    intext = cpp_code.read()

def contains_potential():
    with open(destination_file_path, "r") as cpp_code:
        text = cpp_code.read()
        contains = f"if (mon1 == \"{mon_ids[0]}\" and mon2 == \"{mon_ids[1]}\") {{" in text
        print(contains)
        return contains

if contains_potential():
    # print(match.group())
    sys.exit()
else:
    print(f"Attempting to forcefully add [{mon_ids[0]},{mon_ids[1]}] to {destination_file}")
    outtext = re.sub(r"([\s\S]*\"\n)(\s*?\/\/ =====>> END SECTION CONSTRUCTOR <<=====[\s\S]*)",rf"\1{code_to_insert}\2",intext)
    # print(outtext)
    with open(destination_file_path, "w") as cpp_code:
        cpp_code.write(outtext)
        pass
    if not contains_potential():
        sys.exit(f"Potential was unable to be implemented! Check {MBX_path}/src/potential/2b/{destination_file}")


