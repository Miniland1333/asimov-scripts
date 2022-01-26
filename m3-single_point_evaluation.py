import re
import sys

with open("single_point_test_TTM.txt") as file:
    TTM = file.read()
with open("single_point_test_TTM_MBX.txt") as file:
    TTM_MBX = file.read()
with open("single_point_test_overTTM.txt") as file:
    overTTM = file.read()
with open("single_point_test_overTTM_MBX.txt") as file:
    overTTM_MBX = file.read()


def parse_fit_output(input):
    match = re.search(r" +1 +\d\.\d+e[+-]\d+ +(\d\.\d+e[+-]\d+)", input)  # find calculated value
    return float(match.group(1))


def parse_MBX_output(input):
    return float(input.split("Energy= ")[1])


TTM = parse_fit_output(TTM)
TTM_MBX = parse_MBX_output(TTM_MBX)
overTTM = parse_fit_output(overTTM)
overTTM_MBX = parse_MBX_output(overTTM_MBX)
print(TTM)
print(TTM_MBX)
print(overTTM)
print(overTTM_MBX)

TTM_OK = abs(TTM - TTM_MBX) < abs(TTM / 10000)  # less than 0.01% error
overTTM_OK = abs(overTTM - overTTM_MBX) < abs(overTTM / 10000)
# print (TTM_OK)
# print (overTTM_OK)
if TTM_OK and overTTM_OK:
    print("TTM and MB-nrg seem to be implemented successfully!")
    sys.exit()
else:
    if not TTM_OK:
        print(f"Error: TTM values are divergent {TTM} {TTM_MBX}")
    if not overTTM_OK:
        print(f"Error: overTTM values are divergent {overTTM} {overTTM_MBX}")
    sys.exit("Error: Potential is divergent. Unsuccessfully implemented")
