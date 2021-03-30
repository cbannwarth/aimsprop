import numpy as np

# This script automatically converts a restart file to a Geometry.dat with AIMS runs.
# It assumes that you have velocities in the restart file.

list = [x for x in range(1)]
for i in list:
    atomnum = 0
    atomcoord = np.array([])
    atomvel = np.array([])
    namelist = []
    atommass = np.array([])
    with open("./" + str(i) + "coors.rst7", "r") as f:
        line = f.readline()
        line = f.readline()
        atomnum = int(line.split()[0])
        atomcoord = np.zeros((atomnum, 3))
        atomvel = np.zeros((atomnum, 3))
        for j in range(0, (atomnum + 1) / 2):
            line = f.readline()
            a = line.split()
            atomcoord[j * 2] = np.array([float(a[0]), float(a[1]), float(a[2])])
            if len(a) == 6:
                atomcoord[j * 2 + 1] = np.array([float(a[3]), float(a[4]), float(a[5])])
        for j in range(0, (atomnum + 1) / 2):
            line = f.readline()
            a = line.split()
            atomvel[j * 2] = np.array([float(a[0]), float(a[1]), float(a[2])])
            if len(a) == 6:
                atomvel[j * 2 + 1] = np.array([float(a[3]), float(a[4]), float(a[5])])

    with open("./" + str(i) + "snap.10685.fap_wt.prmtop", "r") as f:
        for line in f:
            if "ATOM_NAME" in line:
                line = next(f)
                for line in f:
                    if "CHARGE" in line:
                        break
                    else:
                        line = line.strip("\n")
                        for c in range(0, len(line), 4):
                            #                           print line[c:c+4]
                            namelist = namelist + [line[c : c + 3]]
            if "MASS" in line:
                line = next(f)
                for line in f:
                    if "ATOM_TYPE_INDEX" in line:
                        break
                    else:
                        a = line.split()
                        a = np.array(map(float, a))
                        atommass = np.hstack((atommass, a))

    with open("Geometry-" + str(i) + ".dat", "w") as f:
        f.write("UNITS=BOHR\n")
        f.write(str(atomnum) + "\n")
        for j in range(0, atomnum):
            if namelist[j] == "Cl-":
                f.write(
                    "{0:<10s}".format(namelist[j][0:2])
                    + "".join(
                        "{0:>22.16f}".format(x / 0.52917724924) for x in atomcoord[j]
                    )
                    + "\n"
                )
            else:
                f.write(
                    "{0:<10s}".format(namelist[j][0])
                    + "".join(
                        "{0:>22.16f}".format(x / 0.52917724924) for x in atomcoord[j]
                    )
                    + "\n"
                )
        f.write("# momenta\n")
        for j in range(0, atomnum):
            for x in atomvel[j]:
                p = x * atommass[j] * 9.3499611711905144e-04 * 1.8228884855409500e03
                f.write(
                    "{0:>22.16f}".format(p)
                )  # time unit in rst7: 1/20.455 ps   length unit in rst7: angstrom    mass unit in amber: atomic mass unit
            f.write("\n")
