#!/usr/bin/env python3

import sys
import os
import argparse
import math
import numpy as np

ROUND_TO = 5


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Trilateration based on time from data in file.")
    parser.add_argument("-f", type=str, metavar=("file"), help="file with data", required=True)
    parser.add_argument("-v", type=str, default="", metavar=("validation file"),
                        help="file with solutions for validation", required=True)
    parser.add_argument("-s", type=float, default=343.0, metavar=("sos"),
                        help="speed of sound (default: 343.0)", required=False)
    args = parser.parse_args()

    # Check if files exists
    if not os.path.isfile(args.f):
        print("Error! Given data file does not exist!")
        return 1

    if not os.path.isfile(args.v):
        print("Error! Given validation file does not exist!")

    # Get solutions for validation
    with open(args.v, "r") as file:
        solutions = [[float(x) for x in x.split()] for x in file.read().split('\n')]

    # Read data from givne file
    with open(args.f, "r") as file:
        # Read amount of stations
        all_amount = int(file.readline())

        # Read station positions
        all_positions = []
        for i in range(all_amount):
            pos = [float(x) for x in file.readline().split()]
            all_positions.append(np.array(pos))

        # Read all measurement snapshots and perform trilateration
        all_err = 0
        amount_snapshots = 0
        while True:
            # Read amount of stations in current snapshot (exit if EOF)
            snapshot = file.readline()
            if not snapshot:
                break

            amount = int(snapshot)

            # Read current snapshot position indexes and times
            p = []
            t = []
            for i in range(amount):
                line = file.readline().split()
                all_positions_i, time = int(line[0]), float(line[1])

                p.append(all_positions[all_positions_i])
                t.append(time)

            # Convert into NumPy array for unison shuffling
            p, t = np.array(p), np.array(t)

            # Calculate trilateration
            if amount < 5:
                print("Error! Less than 5 stations given!")
            elif amount == 5:
                # Calculate distances from main station to other stations given times and speed of sound
                r = [args.s * (t[i] - t[0]) for i in range(1, amount)]

                res = trilaterate_sync(p, r)
                print([round(i, ROUND_TO) for i in res])
            else:
                # Pick random unique combinations of stations
                rand = np.arange(amount)
                rand_p, rand_r = [], []

                while len(rand_p) < amount:
                    # Randomize and pick first 5
                    np.random.shuffle(rand)
                    p, t = p[rand], t[rand]

                    # Calculate distances from main station to other stations given times and speed of sound
                    r = [args.s * (t[i] - t[0]) for i in range(1, amount)]

                    # Always pick different set of stations
                    if not already_used_stations(p[0:5], rand_p):
                        rand_p.append(p[0:5])
                        rand_r.append(r[0:5])

                P = np.array([0.0, 0.0, 0.0])  # End result

                # Calculate for all randomly selected position combinations
                for pos, r_pos in zip(rand_p, rand_r):
                    P += trilaterate_sync(pos, r_pos)

                # Average
                P /= amount

                # Add to global error
                all_err += np.linalg.norm(P - solutions[amount_snapshots])**2
                amount_snapshots += 1

                print([round(i, ROUND_TO) for i in P])

        # Trajectory error
        all_err = math.sqrt(all_err / amount_snapshots)
        print("RMSE: {}".format(round(all_err, ROUND_TO)))

    return 0


def already_used_stations(current, previous):
    # Check if current 5 stations had already been used
    for p in previous:
        match = 0
        for point in p:
            all_0 = (point == current[0]).all()
            all_1 = (point == current[1]).all()
            all_2 = (point == current[2]).all()
            all_3 = (point == current[3]).all()
            all_4 = (point == current[4]).all()
            if all_0 or all_1 or all_2 or all_3 or all_4:
                match += 1
        if match == 5:
            return True

    return False


def trilaterate_sync(p, r):
    p1, r1 = p[0], r[0]

    # Calculate positional differences
    dp = []
    for pos in p[1:]:
        dp.append(np.array([pos[0] - p1[0], pos[1] - p1[1], pos[2] - p1[2]]))

    h = len(dp)

    # Create linear system
    a = [[0 for x in range(h - 1)] for y in range(h - 1)]
    b = [[0 for x in range(1)] for y in range(h - 1)]

    for i in range(1, len(dp)):
        a[i - 1][0] = ((2 * dp[i][0]) / r[i]) - ((2 * dp[0][0]) / r1)
        a[i - 1][1] = ((2 * dp[i][1]) / r[i]) - ((2 * dp[0][1]) / r1)
        a[i - 1][2] = ((2 * dp[i][2]) / r[i]) - ((2 * dp[0][2]) / r1)

        bi = dp[i][0] ** 2 + dp[i][1] ** 2 + dp[i][2] ** 2
        b0 = dp[0][0] ** 2 + dp[0][1] ** 2 + dp[0][2] ** 2
        b[i - 1][0] = r[i] - r[0] - bi / r[i] + b0 / r[0]

    # Perform Gaussian elimination
    gauss = np.linalg.lstsq(a, b, rcond=None)[0].flatten()

    # Base result off of original position
    return p[0] - gauss


if __name__ == "__main__":
    sys.exit(main())
