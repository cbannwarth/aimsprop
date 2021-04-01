"""
Written by Ruibin Liang

This script converts from Amber restart format to AIMS Geometry.dat files. It assumes your restart file has velocities.

To run, just give it the paths to your prmtop, restart data and desired output data as below.

main('test_data/parm.prmtop','test_data/','test_data/outs/')

"""

# This script automatically converts a restart file to a Geometry.dat with AIMS runs.
# It assumes that you have velocities in the restart file.

import glob
import os
from pathlib import Path
import numpy as np

def read_prmtop(prmpath):
    namelist = []
    atommass = []
    with open(prmpath) as f:
        for line in f:
            if "ATOM_NAME" in line:
                line = next(f)
                for line in f:
                    if "CHARGE" in line:
                        break
                    else:
                        line = line.strip("\n")
                        for c in range(0, len(line), 4):
                            namelist = namelist + [line[c : c + 3]]
            if "MASS" in line:
                line = next(f)
                for line in f:
                    if "ATOM_TYPE_INDEX" in line:
                        break
                    else:
                        a = line.split()
                        for x in a:
                            atommass.append(float(x))
    return namelist, atommass


def read_rst(rstpath):
    atomcoord = np.array([])
    atomvel = np.array([])
    atomnum = 0
    with open(rstpath) as f:
        f.readline()
        line = f.readline()
        atomnum = int(line.split()[0])
        atomcoord = np.zeros((atomnum, 3))
        atomvel = np.zeros((atomnum, 3))
        for j in range(0, int((atomnum + 1) / 2)):
            line = f.readline()
            a = line.split()
            atomcoord[j * 2] = np.array([float(a[0]), float(a[1]), float(a[2])])
            if len(a) == 6:
                atomcoord[j * 2 + 1] = np.array([float(a[3]), float(a[4]), float(a[5])])
        for j in range(0, int((atomnum + 1) / 2)):
            line = f.readline()
            a = line.split()
            atomvel[j * 2] = np.array([float(a[0]), float(a[1]), float(a[2])])
            if len(a) == 6:
                atomvel[j * 2 + 1] = np.array([float(a[3]), float(a[4]), float(a[5])])
    return atomcoord, atomvel, atomnum


def output_geom(
    namelist, atommass, atomcoord, atomvel, atomnum, outpath, filename,
):
    # Initialize new output directory if it doesn't exist
    os.system("mkdir -p " + outpath)
    # Create directory structure from original files
    newdir = filename.split("/")[:-1]
    if len(newdir) > 1:
        newdir = "-".join(newdir)

    os.system("mkdir -p " + outpath + newdir)
    with open(outpath + newdir + "/Geometry.dat", "w+") as f:
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


def main(
    prmpath: str, 
    rstpath: str, 
    outpath: str,
):

    Prmpath = Path(prmpath)
    Rstpath = Path(rstpath)
#    Outpath = Path(outpath)

    # Get initial information from parmtop
    names, masses = read_prmtop(Prmpath)

    # Find all restart files in test data
    filenames = Rstpath.glob('*/*.rst*')
    print(filenames)
    # Create new dats
    for filename in filenames:
        coords, vel, numats = read_rst(filename)
        output_geom(names, masses, coords, vel, numats, outpath, filename)

main('test_data/parm.prmtop','test_data/','test_data/outs/')
