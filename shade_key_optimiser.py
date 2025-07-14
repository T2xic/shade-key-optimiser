#!/bin/python3
import argparse
from pulp import LpProblem, LpVariable, LpMinimize, LpInteger, lpSum, value, PULP_CBC_CMD

def non_negative_int(n):
    # Used to enforce type for input
    i_n = int(n)
    if i_n < 0:
        raise argparse.ArgumentTypeError(f"invalid non_negative_int value: '{n}'")
    return i_n

def main():
    parser = argparse.ArgumentParser(description="Determine optimal gold shade key trips, minimising leftover keys")
    parser.add_argument("crimson", type=non_negative_int, help="Number of crimson keys")
    parser.add_argument("red", type=non_negative_int, help="Number of red keys")
    parser.add_argument("brown", type=non_negative_int, help="Number of brown keys")
    parser.add_argument("black", type=non_negative_int, help="Number of black keys")
    parser.add_argument("purple", type=non_negative_int, help="Number of purple keys")

    args = parser.parse_args()

    # Key stock
    keys = {
        "crimson": args.crimson,
        "red": args.red,
        "brown": args.brown,
        "black": args.black,
        "purple": args.purple,
    }

    # Create problem
    prob = LpProblem("Minimal_Leftover_Keys", LpMinimize)

    # Decision variables
    # Each variable is one 'trip', 14 keys of first colour in the variable name then 13 keys of the second colour
    red_crimson = LpVariable("red_crimson", lowBound=0, cat=LpInteger)
    crimson_red = LpVariable("crimson_red", lowBound=0, cat=LpInteger)
    black_crimson = LpVariable("black_crimson", lowBound=0, cat=LpInteger)
    crimson_black = LpVariable("crimson_black", lowBound=0, cat=LpInteger)
    purple_brown = LpVariable("purple_brown", lowBound=0, cat=LpInteger)
    brown_purple = LpVariable("brown_purple", lowBound=0, cat=LpInteger)
    red_brown = LpVariable("red_brown", lowBound=0, cat=LpInteger)
    brown_red = LpVariable("brown_red", lowBound=0, cat=LpInteger)

    trip_descriptions = {
        red_crimson:   "14 red, 13 crimson",
        crimson_red:   "14 crimson, 13 red",
        black_crimson: "14 black, 13 crimson",
        crimson_black: "14 crimson, 13 black",
        purple_brown:  "14 purple, 13 brown",
        brown_purple:  "14 brown, 13 purple",
        red_brown:     "14 red, 13 brown",
        brown_red:     "14 brown, 13 red",
    }

    # Calculate leftover keys
    crimson_left = keys["crimson"] - red_crimson * 13 - crimson_red * 14 - black_crimson * 13 - crimson_black * 14
    red_left     = keys["red"]     - red_crimson * 14 - crimson_red * 13 - red_brown * 14 - brown_red * 13
    brown_left   = keys["brown"]   - purple_brown * 13 - brown_purple * 14 - red_brown * 13 - brown_red * 14
    black_left   = keys["black"]   - black_crimson * 14 - crimson_black * 13
    purple_left  = keys["purple"]  - purple_brown * 14 - brown_purple * 13

    # Objective: minimise total leftover keys
    total_leftover = crimson_left + red_left + brown_left + black_left + purple_left
    prob += total_leftover

    # Constraints: leftovers must be >= 0 (don't use more than available)
    prob += crimson_left >= 0
    prob += red_left >= 0
    prob += brown_left >= 0
    prob += black_left >= 0
    prob += purple_left >= 0

    # Solve
    prob.solve(PULP_CBC_CMD(msg=False))

    # Print results
    print("🔑 Optimal trips:")
    for var, description in trip_descriptions.items():
        if var.varValue > 0:
            print(f"{int(var.varValue)} inventor{'y' if var.varValue == 1 else 'ies'} of {description}")

    print("\n🔑 Leftover keys:")
    print(f"Crimson: {int(value(crimson_left))}")
    print(f"Red:     {int(value(red_left))}")
    print(f"Brown:   {int(value(brown_left))}")
    print(f"Black:   {int(value(black_left))}")
    print(f"Purple:  {int(value(purple_left))}")

    try:
        percentage_left = round((value(prob.objective) / sum(keys.values())) * 100, 2)
    except ZeroDivisionError:
        percentage_left = 0

    print(f"\nTotal Leftover: {int(value(prob.objective))} ({percentage_left:.2f}%)")

if __name__ == '__main__':
    main()