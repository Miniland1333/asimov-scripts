import os,sys

emina = 0
eminb = 0
eminc = 0
nat = 5
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
        try:
            lines = ff.readlines()
        except Exception as e:
            print(f"Config {d} has error {e}")
        eabc = None
        eab = None
        eac = None
        ebc = None
        ea = None
        eb = None
        ec = None
        for line in lines:
            if line.strip().startswith("SETTING E_A_B_C"):
                eabc = float(line.strip().split()[3].replace("D","E"))*tokcal
            elif line.strip().startswith("SETTING E_A_B"):
                eab = float(line.strip().split()[3].replace("D","E"))*tokcal
            elif line.strip().startswith("SETTING E_A_C"):
                eac = float(line.strip().split()[3].replace("D","E"))*tokcal
            elif line.strip().startswith("SETTING E_B_C"):
                ebc = float(line.strip().split()[3].replace("D","E"))*tokcal
            elif line.strip().startswith("SETTING E_A"):
                ea = float(line.strip().split()[3].replace("D","E"))*tokcal
            elif line.strip().startswith("SETTING E_B"):
                eb = float(line.strip().split()[3].replace("D","E"))*tokcal
            elif line.strip().startswith("SETTING E_C"):
                ec = float(line.strip().split()[3].replace("D","E"))*tokcal
        if eabc is None:
            print("Config " + d + " has output but trimer is messed up..")
            continue
        elif eab is None or eac is None or ebc is None:
            print("Config " + d + " has output but dimer is messed up..")
            continue
        elif ea is None or eb is None or ec is None:
            print("Config " + d + " has output but monomer is messed up..")
            continue

        if ea < emina:
            emina = ea

        if eb < eminb:
            eminb = eb

        if ec < eminc:
            eminc = ec

        edefa = (ea - emina)
        edefb = (eb - eminb)
        edefc = (ec - eminc)


        ie = eabc - ea - eb - ec
        be = ie + edefa + edefb + edefc
        three_body = eabc - eab - eac - ebc + ea + eb + ec

        if be > emax:
            emax_exceeded = True

        # if float(d[-5:].lstrip("0")) % 100 == 0:
            # print(d)

with open("min_energies.energies",'w') as fen:
   fen.write(f"Min Mon 1 = {ea}\nMin Mon 2 = {eb}\nMin Mon 3 = {ec}\n")

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
            try:
                lines = ff.readlines()
            except Exception as e:
                print(f"Config {d} has error {e}")
            eabc = None
            eab = None
            eac = None
            ebc = None
            ea = None
            eb = None
            ec = None
            for line in lines:
                if line.strip().startswith("SETTING E_A_B_C"):
                    eabc = float(line.strip().split()[3].replace("D","E"))*tokcal
                elif line.strip().startswith("SETTING E_A_B"):
                    eab = float(line.strip().split()[3].replace("D","E"))*tokcal
                elif line.strip().startswith("SETTING E_A_C"):
                    eac = float(line.strip().split()[3].replace("D","E"))*tokcal
                elif line.strip().startswith("SETTING E_B_C"):
                    ebc = float(line.strip().split()[3].replace("D","E"))*tokcal
                elif line.strip().startswith("SETTING E_A"):
                    ea = float(line.strip().split()[3].replace("D","E"))*tokcal
                elif line.strip().startswith("SETTING E_B"):
                    eb = float(line.strip().split()[3].replace("D","E"))*tokcal
                elif line.strip().startswith("SETTING E_C"):
                    ec = float(line.strip().split()[3].replace("D","E"))*tokcal
            if eabc is None:
                print("Config " + d + " has output but trimer is messed up..")
                continue
            elif eab is None or eac is None or ebc is None:
                print("Config " + d + " has output but dimer is messed up..")
                continue
            elif ea is None or eb is None or ec is None:
                print("Config " + d + " has output but monomer is messed up..")
                continue



            edefa = (ea - emina)
            edefb = (eb - eminb)
            edefc = (ec - eminc)


            ie = eabc - ea - eb - ec
            be = ie + edefa + edefb + edefc
            three_body = eabc - eab - eac - ebc + ea + eb + ec

            if be > emax:
                continue

            a = fx.readlines()

            ts.write("{}\n".format(nat))
            ts.write("{} {}\n".format(be, three_body))
            for i in range(nat):
                ts.write(a[i+2])
            if not "\n" in a[nat+1]: # if does not already have trailing newline
                ts.write("\n")

            if float(d[-5:].lstrip("0")) % 100 == 0:
                print(d)
# print(lowestE1, lowestE2)