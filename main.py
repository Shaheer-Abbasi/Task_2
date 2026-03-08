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

def write_csv(sp, results, output_dir="results"):
    sp_label = f"({sp[0]}, {sp[1]})"
    filename = os.path.join(output_dir, f"sp_{sp[0]}_{sp[1]}.csv".replace(" ", ""))

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            f"p/z for sp = {sp_label}",
            "Run1", "", "",
            "Run2", "", "",
            "Best (across both runs)", ""
        ])

        writer.writerow([
            "",
            "Evals (r1, r2, r3, total)", "Sol1 / Sol2 / Sol3", "f(sol1) / f(sol2) / f(sol3)",
            "Evals (r1, r2, r3, total)", "Sol1 / Sol2 / Sol3", "f(sol1) / f(sol2) / f(sol3)",
            "Best Sol", "Best f"
        ])

        # One data row per p/z combination
        for p in P_VALUES:
            for z in Z_VALUES:
                run1, run2 = results[(p, z, sp)]

                (sol1_1, f1_1), (sol2_1, f2_1), (sol3_1, f3_1), (e1_1, e2_1, e3_1, tot1) = run1
                (sol1_2, f1_2), (sol2_2, f2_2), (sol3_2, f3_2), (e1_2, e2_2, e3_2, tot2) = run2

                # Find best solution
                best_sol, best_f = sol1_1, f1_1
                for sol, f in [(sol2_1, f2_1), (sol3_1, f3_1), (sol1_2, f1_2), (sol2_2, f2_2), (sol3_2, f3_2)]:
                    if f < best_f:
                        best_sol, best_f = sol, f

                writer.writerow([
                    f"p={p} & z={z}",
                    # Run1
                    f"({e1_1}, {e2_1}, {e3_1}, {tot1})",
                    f"{format_coord(sol1_1)} / {format_coord(sol2_1)} / {format_coord(sol3_1)}",
                    f"{f1_1:.4f} / {f2_1:.4f} / {f3_1:.4f}",
                    # Run2
                    f"({e1_2}, {e2_2}, {e3_2}, {tot2})",
                    f"{format_coord(sol1_2)} / {format_coord(sol2_2)} / {format_coord(sol3_2)}",
                    f"{f1_2:.4f} / {f2_2:.4f} / {f3_2:.4f}",
                    # Best across both runs
                    format_coord(best_sol),
                    f"{best_f:.4f}",
                ])

# Write bonus runs to CSV file
def write_bonus_csv(bonus_runs, output_dir="results"): 
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, "bonus_runs.csv")

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Bonus Runs",
            "Evals (r1, r2, r3, total)", "Sol1 / Sol2 / Sol3", "f(sol1) / f(sol2) / f(sol3)",
            "Best Sol", "Best f"
        ])

        for run_num, (sp, p, z, seed, res) in enumerate(bonus_runs, start=33):
            (sol1, f1), (sol2, f2), (sol3, f3), (e1, e2, e3, total) = res

            best_sol, best_f = sol1, f1
            if f2 < best_f:
                best_sol, best_f = sol2, f2
            if f3 < best_f:
                best_sol, best_f = sol3, f3

            writer.writerow([
                f"Run {run_num}: sp={format_coord(sp)}, p={p}, z={z}, seed={seed}",
                f"({e1}, {e2}, {e3}, {total})",
                f"{format_coord(sol1)} / {format_coord(sol2)} / {format_coord(sol3)}",
                f"{f1:.4f} / {f2:.4f} / {f3:.4f}",
                format_coord(best_sol),
                f"{best_f:.4f}",
            ])

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

    # Write one CSV per starting point into results/
    for sp in START_POINTS:
        write_csv(sp, results)

    # --- Bonus runs 33 & 34 ---
    BONUS_SP_33 = np.array([-510, 400], dtype=np.float64)
    BONUS_P_33  = 800
    BONUS_Z_33  = 120
    BONUS_SEED_33 = 21

    BONUS_SP_34 = np.array([512, 404], dtype=np.float64)
    BONUS_P_34  = 800
    BONUS_Z_34  = 120
    BONUS_SEED_34 = 21

    bonus_runs = [
        (BONUS_SP_33, BONUS_P_33, BONUS_Z_33, BONUS_SEED_33,
         RHCR2(BONUS_SP_33, z=BONUS_Z_33, p=BONUS_P_33, seed=BONUS_SEED_33)),
        (BONUS_SP_34, BONUS_P_34, BONUS_Z_34, BONUS_SEED_34,
         RHCR2(BONUS_SP_34, z=BONUS_Z_34, p=BONUS_P_34, seed=BONUS_SEED_34)),
    ]
    write_bonus_csv(bonus_runs)

if __name__ == "__main__":
    main()

