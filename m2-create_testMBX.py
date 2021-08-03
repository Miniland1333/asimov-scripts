import sys

ionPair = sys.argv[1]
mon_ids = ionPair.split("-")

def substitute(filename):
    with open(f"../../scripts/testMBX/{filename}", "r") as read_file:
        result = read_file.read()
        result = result.replace('JSON_monomer1_SUBSTITUTION', mon_ids[0])
        result = result.replace('JSON_monomer2_SUBSTITUTION', mon_ids[1])
    with open(filename, "w") as output_file:
        output_file.write(result)

#create mbx.json
substitute("mbx.json")
substitute("ttm.json")
