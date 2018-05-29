#!/usr/bin/env python3

import sys
import argparse
import math
import numpy as np
import random


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
    
    # Convert to planar coordinate system (all points on z = 0)
    v1 = p[1] - p[0]  # Vector from p1 to p2 (p2 is shifted to our coordinate system)
    v2 = p[2] - p[0]  # Vector from p1 to p3 (p3 is shifted to our coordinate system)
    # p1 is center of our coordinate system (0, 0, 0)

    # Create orthogonal axes of our coordinate system (simplified Gram-Schmidt process)
    v1xv2 = np.cross(v1, v2)
    xn = v1 / np.linalg.norm(v1)

    if np.linalg.norm(v1xv2) == 0:
        print("V1 and V2 are collinear")
        quit()

    zn = v1xv2 / np.linalg.norm(v1xv2)
    yn = np.cross(xn, zn)
    
    # Calculate a,b and c from p4 and others locations
    a = np.dot((p[3] - p[0]), xn)
    b = np.dot((p[3] - p[0]), yn)
    c = np.dot((p[3] - p[0]), zn)
    #p4 = np.array([a, b, c])
    #print(a)
    #print(b)
    #print(c)
    d = np.dot(xn, v1)  # p1 = [0, 0, 0]
    i = np.dot(xn, v2)  # p2 = [d, 0, 0]
    j = np.dot(yn, v2)  # p3 = [i, j, 0]

    # Calculate target's position
    x = (r[0]**2 - r[1]**2 + d**2) / (2 * d)
    y = (r[0]**2 - r[2]**2 + i**2 + j**2) / (2 * j) - (i / j) * x

    if almost_equal(c, 0):
        z = np.zeros(3)
    else:
        z = (r[0]**2 - r[3]**2 + a**2 + b**2 + c**2) / (2 * c) - (a / c) * x - (b / c) * y
    
    r0 = x**2 + y**2 + z**2
    
    deltaR = []
    deltaP = []
    
    for i in range(1, len(r)):
        deltaR.append((r[i]-r[0]))
        deltaP.append(np.array([p[i][0]-p[0][0], p[i][1]-p[0][1], p[i][2]-p[0][2]]))
        
    r = np.array(deltaR)
    deltaP = np.array(deltaP)


def almost_equal(a, b):
    return np.abs(a - b) < 0.000001

if __name__ == "__main__":
    sys.exit(main())
    
