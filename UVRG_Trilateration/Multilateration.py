#!/usr/bin/env python3

import sys
import argparse
import math
import numpy as np
import random
from scipy.linalg import lu

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Multilateration")
    for i in range(1, 6):
        parser.add_argument(
            "-p{}".format(i), type=float, nargs=3, metavar=("x", "y", "z"),
            help="{}. base station position".format(i), required=i < 4)
        parser.add_argument(
            "-t{}".format(i), type=float, metavar=("r"),
            help="distance to {}. base station".format(i), required=i < 4)
    args = parser.parse_args()

    # Positions
    p = [np.array(args.p1), np.array(args.p2), np.array(args.p3), np.array(args.p4), np.array(args.p5)]

    # Time
    t = [args.t1, args.t2, args.t3, args.t4, args.t5]

    sf = 343.0
    r = []
    for i in range(1, len(p)):
        distance = sf * (t[i] - t[0])
        r.append(distance)

    r = np.array(r)

    print("R: " + str(r) + "\n")

    deltaP = []

    for i in range(1, len(p)):
        deltaP.append(np.array([p[i][0]-p[0][0], p[i][1]-p[0][1], p[i][2]-p[0][2]]))

    deltaP = np.array(deltaP)

    h = len(deltaP)

    A = [[0 for x in range(h - 1)] for y in range(h - 1)]
    b = [[0 for x in range(1)] for y in range(h - 1)]

    print("deltaP :\n" + str(deltaP) + "\n")
    print("r: " +str(r) + "\n")

    for i in range(1, len(deltaP)):
        A[i-1][0] = ((2 * deltaP[i][0])/(r[i])) - ((2 * deltaP[0][0]) / (r[0]))
        A[i-1][1] = ((2 * deltaP[i][1])/(r[i])) - ((2 * deltaP[0][1]) / (r[0]))
        A[i-1][2] = ((2 * deltaP[i][2])/(r[i])) - ((2 * deltaP[0][2]) / (r[0]))
        b[i-1][0] = r[i] - r[0] - (deltaP[i][0] ** 2 + deltaP[i][1] ** 2 + deltaP[i][2] ** 2) / r[i] + (deltaP[0][0] ** 2 + deltaP[0][1] ** 2 + deltaP[0][2] ** 2) / r[0]

    A = np.array(A)

    print("P: " + str(p[0]) + "\n") 

    gauss = np.linalg.lstsq(A, b)[0].flatten()
    
    res = gauss+ p[0]

    print("Gauss: " + str(gauss)  + "\n")
    print("RES: " + str(res)  + "\n")

if __name__ == "__main__":
    sys.exit(main())
