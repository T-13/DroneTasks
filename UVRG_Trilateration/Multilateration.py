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
    deltaP = []

    for i in range(1, len(r) + 1):
        deltaP.append(np.array([p[i][0]-p[0][0], p[i][1]-p[0][1], p[i][2]-p[0][2]]))

    deltaP = np.array(deltaP)

    k = 4
    h = len(deltaP)

    Matrix = [[0 for x in range(h+1)] for y in range(h)]
    for i in range(0, len(deltaP)):
        Matrix[i][0] = ((2 * deltaP[i][0])/(r[i])) - ((2 * deltaP[0][0]) / (r[0]))
        Matrix[i][1] = ((2 * deltaP[i][1])/(r[i])) - ((2 * deltaP[0][1]) / (r[0]))
        Matrix[i][2] = ((2 * deltaP[i][2])/(r[i])) - ((2 * deltaP[0][2]) / (r[0]))
        Matrix[i][3] = r[i] - r[0] - (deltaP[i][0] ** 2 + deltaP[i][1] ** 2 + deltaP[i][2] ** 2) / r[i] + (deltaP[0][0] ** 2 + deltaP[0][1] ** 2 + deltaP[0][2] ** 2) / r[0]

    Matrix = np.array(Matrix)
    print(Matrix)
    print(gauss(Matrix))


def gauss(A):
    n = len(A)

    for i in range(0, n):
        # Search for maximum in this column
        maxEl = abs(A[i][i])
        maxRow = i
        for k in range(i+1, n):
            if abs(A[k][i]) > maxEl:
                maxEl = abs(A[k][i])
                maxRow = k

        # Swap maximum row with current row (column by column)
        for k in range(i, n+1):
            tmp = A[maxRow][k]
            A[maxRow][k] = A[i][k]
            A[i][k] = tmp

        # Make all rows below this one 0 in current column
        for k in range(i+1, n):
            c = -A[k][i]/A[i][i]
            for j in range(i, n+1):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]

    # Solve equation Ax=b for an upper triangular matrix A
    x = [0 for i in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = A[i][n]/A[i][i]
        for k in range(i-1, -1, -1):
            A[k][n] -= A[k][i] * x[i]
    return x

if __name__ == "__main__":
    sys.exit(main())

