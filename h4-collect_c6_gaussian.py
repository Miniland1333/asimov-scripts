
import sys
import os
import re


directories = [f"./{i}" for i in sorted(os.listdir(".")) if os.path.isdir(f"./{i}")]

result = ""
for xyz in directories:
    with open(f"{xyz}/input", 'r') as infile:
        lines = infile.read()
        try:
            distance = re.search(f"0\.00000000   0\.00000000[\s\S]*0\.00000000   0\.00000000(.*)\.00000000",lines).group(1)
        except Exception as err:
            print(sys.argv[1], xyz, err)
    with open(f"{xyz}/output.postg", 'r') as infile:
        lines = infile.read()
        try:
            c6 = re.search(f"\n  1   2  \d+\..+?  (\d+\..+?)  ",lines).group(1)
        except Exception as err:
            print(sys.argv[1], xyz, err)
            continue
    print(distance, c6)
    result += f"{distance},{c6}\n"

with open(f"./c6.out", 'w') as outfile:
    outfile.write(result)
with open(f"../c6.out", 'w') as outfile:
    outfile.write(result)
