import re
import sys

with open("single_point_test_TTM.txt") as file:
    TTM = file.read()
with open("single_point_test_TTM_MBX.txt") as file:
    TTM_MBX = file.read()
with open("single_point_test.txt") as file:
    mb = file.read()
with open("single_point_test_MBX.txt") as file:
    MBX = file.read()


def parse_fit_output(input):
    match = re.search(r" +1 +-?\d\.\d+e[+-]\d+ +(-?\d\.\d+e[+-]\d+)", input)  # find calculated value
    return float(match.group(1))


def parse_MBX_output(input):
    return float(input.split("Energy= ")[1])


TTM = parse_fit_output(TTM)
TTM_MBX = parse_MBX_output(TTM_MBX)
mb = parse_fit_output(mb)
MBX = parse_MBX_output(MBX)
print(TTM)
print(TTM_MBX)
print(mb)
print(MBX)

epsilon=0.005 # kcal/mol
TTM_OK = abs(TTM - TTM_MBX) < abs(TTM / 10000)  # less than 0.01% error
TTM_OK = (TTM_OK) or (abs(TTM - TTM_MBX) < epsilon) # less than 0.05kcal/mol error
overTTM_OK = abs(mb - MBX) < abs(mb / 10000)
overTTM_OK = (overTTM_OK) or abs(mb - MBX) < epsilon # less than 0.05kcal/mol error
# print (TTM_OK)
# print (overTTM_OK)
if TTM_OK and overTTM_OK:
    print("TTM and MB-nrg seem to be implemented successfully!")
    sys.exit()
else:
    if not TTM_OK:
        print(f"Error: TTM values are divergent {TTM} {TTM_MBX}")
    if not overTTM_OK:
        print(f"Error: MB-nrg values are divergent {mb} {MBX}")
    sys.exit("Error: Potential is divergent. Unsuccessfully implemented")
