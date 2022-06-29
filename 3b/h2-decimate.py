import os
import sys

if not len(sys.argv) == 2:
    print(f"./{sys.argv[0]} full_set.xyz")
    sys.exit(1)
inputfile = sys.argv[1]
natoms = 0

with open(inputfile) as infile:
    lines = infile.readlines()
    natoms = int(lines[0])
    numlines = len(lines)
    print(numlines)
    configlength = natoms + 2

    if not numlines % (configlength)  == 0:
        print(f"{inputfile} does not seem to have equal sized configs. Check the file.\n")
        print(f"numlines % (configlength) = {numlines % (configlength)}")
        sys.exit(1)

training = ""
test = ""

for i in range(0, numlines//(natoms+2) ):
    start = configlength * i
    end = configlength * (i + 1)
    config = lines[start:end]
    if not int(config[0]) == natoms:
        print(f"config {i} has uneven length")
        sys.exit(1)
    config = "".join(config)
    if i % 10:
        training += config # 90% of configs
    else:
        test += config # 10% of configs

with open("90_out.xyz","w") as outfile:
    outfile.write(training)
with open("10_out.xyz","w") as outfile:
    outfile.write(test)