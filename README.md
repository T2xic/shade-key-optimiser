# Gold Shade Key Trip Optimiser

Uses integer linear programming via PuLP to find the optimal way to use gold shade keys from the Shades of Mort'ton minigame in Old School RuneScape.

## Problem Overview

When cremating Urium remains, keys are obtained in approximately the following ratio:
- **Crimson:** 225
- **Red:** 100
- **Brown:** 100
- **Black:** 50
- **Purple:** 30

Each key opens one chest, and chests are found in fixed pairs.
- **Crimson & Red**
- **Crimson & Black**
- **Brown & Purple**
- **Brown & Red**

With 27 inventory slots, it is most time-efficient to take 14 of one colour and 13 of another that matches a chest pair. This script decides the optimal combination of trips to minimise leftover keys.

## General Solution

If the keys you have are in the ratio you obtain them:
1. Do trips of **14 Crimson, 13 Red** until you run out of **Red** keys
2. Do trips of **14 Crimson, 13 Black** until you run out of **Black** keys
3. Do trips of **14 Brown, 13 Purple** until you run out of **Purple** keys

This leaves ~28% of your Crimson keys and ~68% of your Brown keys. Leftover keys should still be used by doing trips of 27 of a single key, but these trips are less time-efficient.

If the keys you have are not in the ratio they are obtained in, the optimal combination of trips will be different.

## Usage
```
python3 shade_key_optimiser.py <crimson> <red> <brown> <black> <purple>
```
Each argument should be a non-negative integer representing the number of keys you have of that colour.

## Example
```bash
python3 shade_key_optimiser.py 2250 1000 1000 500 300
🔑 Optimal trips:
76 inventories of 14 crimson, 13 red
38 inventories of 14 crimson, 13 black
23 inventories of 14 brown, 13 purple

🔑 Leftover keys:
Crimson: 654
Red:     12
Brown:   678
Black:   6
Purple:  1

Total Leftover: 1351 (26.75%)
```

## Requirements

- Python 3
- [PuLP](https://pypi.org/project/PuLP/) library