#Experimental. Might need revision.

import re

def parse_orca_homo_lumo(filename):
    homo = None
    lumo = None
    in_block = False

    with open(filename) as f:
        for line in f:
            # Detect beginning of the orbital block
            if "ORBITAL ENERGIES" in line:
                in_block = True
                # skip next 3 header lines
                for _ in range(3):
                    next(f)
                continue

            if in_block:
                line = line.strip()

                # If line stops being numeric → end of block
                if not re.match(r"^\d+", line):
                    break

                parts = line.split()
                # Expected: NO, OCC, E(Eh), E(eV)
                occ = float(parts[1])
                energy_ev = float(parts[3])  # E(eV)

                if occ > 0:    # occupied → homo candidate
                    homo = energy_ev
                elif occ == 0 and lumo is None:  # first unoccupied → LUMO
                    lumo = energy_ev
                    break

    return homo, lumo, (lumo - homo if homo is not None and lumo is not None else None)


homo, lumo, gap = parse_orca_homo_lumo("inpu.txt")

print("HOMO (eV):", homo)
print("LUMO (eV):", lumo)
print("Gap (eV):", gap)


print("LUMO: "+str(LUMO))
print("HOMO: "+str(HOMO))
print("GAP: "+str(LUMO-HOMO))
