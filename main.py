from rhc import RHCR2
import numpy as np
import csv
import os

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

# Format a coordinate pair for CSV output
def format_coord(arr):
    return f"({arr[0]:.2f}, {arr[1]:.2f})"

def write_csv(p, z, results, output_dir="results"):
    # Ensure output directory exists
    # Write the results into a CSV file for readability
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"p{p}_z{z}.csv")

    headers = [
        "sp", "Run",
        "Evals r1", "Evals r2", "Evals r3", "Evals total",
        "Sol1", "Sol2", "Sol3",
        "f(sol1)", "f(sol2)", "f(sol3)",
        "Best Sol", "Best f"
    ]

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for sp in START_POINTS:
            run1, run2 = results[(p, z, sp)]
            for run_num, res in enumerate([run1, run2], start=1):
                (sol1, f1), (sol2, f2), (sol3, f3), (e1, e2, e3, total) = res

                # Determine best solution across 3 runs by comparing f values
                best_sol, best_f = sol1, f1
                if f2 < best_f:
                    best_sol, best_f = sol2, f2
                if f3 < best_f:
                    best_sol, best_f = sol3, f3

                writer.writerow([
                    str(sp) if run_num == 1 else "",
                    f"Run{run_num}",
                    e1, e2, e3, total,
                    format_coord(sol1),
                    format_coord(sol2),
                    format_coord(sol3),
                    f"{f1:.4f}",
                    f"{f2:.4f}",
                    f"{f3:.4f}",
                    format_coord(best_sol),
                    f"{best_f:.4f}",
                ])
            writer.writerow([])  # blank separator row between each start point

    print(f"Wrote {filename}")

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

    # Write one CSV per p/z combination into results/
    for p in P_VALUES:
        for z in Z_VALUES:
            write_csv(p, z, results)

if __name__ == "__main__":
    main()

