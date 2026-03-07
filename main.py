from rhc import RHCR2
import numpy as np

# Starting points, p/z combos, and seeds as specified in the docx
START_POINTS = [
    (-300, -500),
    (0, 0),
    (-222, -222),
    (-510, 400),
]
P_VALUES = [150, 400]
Z_VALUES = [12, 60]
SEEDS = [67, 1738] # Two seeds for the two runs per combo

def main():
    # Store the results in a dictionary 
    # The keys are tuple of (p, z, sp)
    results = {}

    # Loop through all the combos of p, z, and starting points
    for p in P_VALUES:
        for z in Z_VALUES:
            for sp in START_POINTS:
                sp_arr = np.array(sp, dtype=np.float64)
                run1 = RHCR2(sp_arr, z=z, p=p, seed=SEEDS[0])
                run2 = RHCR2(sp_arr, z=z, p=p, seed=SEEDS[1])
                results[(p, z, sp)] = (run1, run2)

if __name__ == "__main__":
    main()
