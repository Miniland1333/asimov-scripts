import os,sys

emin1 = 0
emin2 = 0
nat = 2
emax = 200.0
emax_exceeded = False
tokcal = 627.509
directories = [f"./{i}" for i in sorted(os.listdir(".")) if (os.path.isdir(f"./{i}"))]

# find minimum energies
print("Searching for lowest energy in ts...")
for d in directories:
    log = d + '/input.out'
    xyz = d + '/input.xyz'
    if not os.path.isfile(log):
        print("Config " + d + " has no output...")
        continue
    with open(log,'r') as ff , open(xyz,'r') as fx:
        lines = ff.readlines()
        e1 = None
        e2 = None
        eTot = None
        e2b = None
        for line in lines:
            if line.strip().startswith("SETTING E_A_A_5Z"):
                e1 = float(line.strip().split()[3].replace("D","E"))
            elif line.strip().startswith("SETTING E_B_B_5Z"):
                e2 = float(line.strip().split()[3].replace("D","E"))
            elif line.strip().startswith("SETTING E_AB_AB_5Z"):
                eTot = float(line.strip().split()[3].replace("D","E"))
            elif line.strip().startswith("SETTING IE_TQ"):
                e2b = float(line.strip().split()[3].replace("D","E"))
        if e1 is None or e2 is None or eTot is None or e2b is None:
            print("Config " + d + " has output but something is messed up..")
            continue

        if e1 < emin1:
            emin1 = e1

        if e2 < emin2:
            emin2 = e2

        edef1 = (e1 - emin1)*tokcal
        edef2 = (e2 - emin2)*tokcal
        ie = e2b
        be = ie + edef1 + edef2

        if be > emax:
            emax_exceeded = True

        # if float(d[-5:].lstrip("0")) % 100 == 0:
            # print(d)

with open("min_energies.energies",'w') as fen:
   fen.write("Min Mon 1 = {}\nMin Mon 2 = {}\n".format(emin1,emin2))

if(emax_exceeded):
    print(f"Binding energies above emax {emax} kcal/mol will be silently discarded")

outfile = sys.argv[1]
with open(f"../{outfile}",'w') as ts:
    for d in directories:
        log = d + '/input.out'
        xyz = d + '/input.xyz'
        if not os.path.isfile(log):
            print("Config " + d + " has no output...")
            continue
        with open(log,'r') as ff , open(xyz,'r') as fx:
            lines = ff.readlines()
            e1 = None
            e2 = None
            eTot = None
            e2b = None
            for line in lines:
                if line.strip().startswith("SETTING E_A_A_5Z"):
                    e1 = float(line.strip().split()[3].replace("D","E"))
                elif line.strip().startswith("SETTING E_B_B_5Z"):
                    e2 = float(line.strip().split()[3].replace("D","E"))
                elif line.strip().startswith("SETTING E_AB_AB_5Z"):
                    eTot = float(line.strip().split()[3].replace("D","E"))
                elif line.strip().startswith("SETTING IE_TQ"):
                    e2b = float(line.strip().split()[3].replace("D","E"))
            if e1 is None or e2 is None or eTot is None or e2b is None:
                print("Config " + d + " has output but something is messed up..")
                continue

            edef1 = (e1 - emin1)*tokcal
            edef2 = (e2 - emin2)*tokcal
            ie = e2b
            be = ie + edef1 + edef2

            if be > emax:
                continue

            a = fx.readlines()

            ts.write("{}\n".format(nat))
            ts.write("{} {}\n".format(be, e2b))
            for i in range(nat):
                ts.write(a[i+2])
            if not "\n" in a[nat+1]: # if does not already have trailing newline
                ts.write("\n")

            if float(d[-5:].lstrip("0")) % 100 == 0:
                print(d)


            with open(f"{d}/reference_energy.dat","w") as energyfile:
                energyfile.write(f"{be} {e2b}")
# print(lowestE1, lowestE2)