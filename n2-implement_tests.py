import sys
import os
import re
import json

scriptsDir = os.environ.get('scriptsDir')
mbxDir = os.environ.get('MBX_HOME')

# ionsDir = f"{home}/projects/ion-ion"
with open(f"{scriptsDir}/../ion-pairs.json", "r") as read_file:
    pairs = json.load(read_file)
    pair = pairs[sys.argv[1]]
    charges = pair["charges"]
    ionsArray = sys.argv[1].split("-")

with open("config.ini") as read_file:
    text = read_file.read()
    a = float(re.search(r"a = \[([\d.]*?)\]", text).group(1))
    c6 = float(re.search(r"c6 = \[([\d.]*?)\]", text).group(1))
    d6 = float(re.search(r"d6 = \[([\d.]*?)\]", text).group(1))


def chargedMonomerName(index, escape=False):
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
    if escape:
        charge = charge.replace("+", "\\+")

    return ionsArray[index] + charge


with open("single_point.out") as read_file:
    text = read_file.read()
    mon1E = chargedMonomerName(0, True)
    mon2E = chargedMonomerName(1, True)
    # print(rf"Entering get_2b_energy.*?\nDimer {mon1} -- {mon2}:[\s\S]*?\nOutput energy.*\n")
    matches = re.findall(rf"Entering get_2b_energy.*?\nDimer {mon1E} -- {mon2E}:[\s\S]*?\nOutput energy.*\n", text)

    # print(len(matches))
    if len(matches) >= 1:
        energy_2b = matches[0]  # Only want to first valid dimer
    else:
        sys.exit("Error: No matches found")

    mon1_grad = re.search(rf"Output gradients for \d monomers of type {mon1E}:\n(.*) , ", energy_2b).group(1)
    mon2_grad = re.search(rf"Output gradients for \d monomers of type {mon2E}:\n(.*) , ", energy_2b).group(1)
    energy = re.search(rf"Output energy: (.*)", energy_2b).group(1)
    # print(energy_2b)
    print(mon1_grad)
    print(mon2_grad)
    print(energy)

    unittest_dir = f"{mbxDir}/src/tests/unittests_v0.3.0a"
    mon1 = chargedMonomerName(0)
    mon2 = chargedMonomerName(1)


    def read_unittest(name):
        with open(f"{unittest_dir}/unittest-{name}.cpp") as infile:
            return infile.read()


    def write_unittest(name, text):
        with open(f"{unittest_dir}/unittest-{name}.cpp", "w") as outfile:
            outfile.write(text)


    def spaces(n):  # create a string of spaces for formatting
        return " " * n


    ion_pair = f"{{\"{mon1}\",\"{mon2}\"}}"


    def implement_bucktools():
        unittest = read_unittest("bucktools")
        # append monomer into pairs
        unittest = re.sub(r"(std::vector<std::pair<std::string, std::string> > pairs =[\s\S]+?)(};)",
                          rf"\1,\n{spaces(63)}{ion_pair}\2", unittest)
        # append monomer into buck_pairs
        unittest = re.sub(r"(std::vector<std::pair<std::string, std::string> > buck_pairs =[\s\S]+?)(};)",
                          rf"\1,\n{spaces(68)}{ion_pair}\2", unittest)
        # append a_expected
        unittest = re.sub(r"(std::vector<std::vector<double> > a_expected =[\s\S]+?)(\n\s*};)",
                          rf"\1\n{spaces(8)}{{{a}}},{spaces(74)}// {ion_pair}\2", unittest)
        # append b_expected
        unittest = re.sub(r"(std::vector<std::vector<double> > b_expected =[\s\S]+?)(\n\s*};)",
                          rf"\1\n{spaces(8)}{{{d6}}},{spaces(74)}// {ion_pair}\2", unittest)
        # append ntypes2
        unittest = re.sub(r"(std::vector<size_t> ntypes2 = {.+?)(};)", r"\1, 1\2", unittest)
        # append types1
        unittest = re.sub(r"(std::vector<std::vector<size_t> > types1 = {[\s\S]+?)(\n\s*?};)",
                          rf"\1\n{spaces(48)}{{0}},{spaces(20)}// {ion_pair}\2", unittest)
        # append types2
        unittest = re.sub(r"(std::vector<std::vector<size_t> > types2 = {[\s\S]+?)(\n\s*?};)",
                          rf"\1\n{spaces(48)}{{0}},{spaces(20)}// {ion_pair}\2", unittest)
        # print(unittest)
        write_unittest("bucktools", unittest)
        print("Implemented unittest-bucktools.cpp")
        pass


    def implement_disptools():
        unittest = read_unittest("disptools")
        # append monomer into mon1
        unittest = re.sub(r"(std::vector<std::string> mon1 = {[\s\S]+?)(};)", rf'\1,\n{spaces(37)}"{mon1}"\2', unittest)
        # append monomer into mon2
        unittest = re.sub(r"(std::vector<std::string> mon2 = {[\s\S]+?)(};)", rf'\1,\n{spaces(37)}"{mon2}"\2', unittest)
        # append index1
        unittest = re.sub(r"(std::vector<size_t> index1 = {[\s\S]+?)(};)", rf"\1, 0\2", unittest)
        # append index2
        unittest = re.sub(r"(std::vector<size_t> index2 = {[\s\S]+?)(};)", rf"\1, 0\2", unittest)
        # append c6
        unittest = re.sub(r"(std::vector<double> expected_out_c6 = {[\s\S]+?)(\n\s*?};)",
                          rf"\1\n{spaces(43)}{c6},   // {ion_pair}\2", unittest)
        # append c6
        unittest = re.sub(r"(std::vector<double> expected_out_d6 = {[\s\S]+?)(\n\s*?};)",
                          rf"\1\n{spaces(43)}{d6},   // {ion_pair}\2", unittest)
        # print(unittest)
        write_unittest("disptools", unittest)
        print("Implemented unittest-disptools.cpp")


    implement_bucktools()
    implement_disptools()
