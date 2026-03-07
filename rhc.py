from frog import frog
import numpy as np

def get_best_neighbor(curr, z, p):
    best_neighbor = None
    best_neighbor_val = float('inf')

    # Generate random neighbors
    for _ in range(p):
        # Generate random neighbor
        # Using uniform dist so neighbor is within bounds [-z, z]
        distr = np.random.uniform(-z, z, size=curr.shape)
        neighbor = curr + distr

        # Clamp neighbor to bounds
        # .clip() works by setting values smaller than -512 to -512 and values larger than 512 to 512
        neighbor = np.clip(neighbor, -512, 512)

        val = frog(neighbor)

        # Check if new neighbor is smaller than the best so far
        # If so, update the best neighbor + value
        if val < best_neighbor_val:
            best_neighbor_val = val
            best_neighbor = neighbor

    return best_neighbor, best_neighbor_val, p  # p evals were made

def RHC(sp, z, p, prev_sol=None, seed=67):
    # Set seed
    np.random.seed(seed)

    # If a previous solution is provided, use it as the starting point
    # Otherwise, use sp
    start_point = prev_sol if prev_sol is not None else sp

    # Initialize the current point and the value
    # Using dtype to ensure truncated integers aren't stored
    curr = np.array(start_point, dtype=np.float64)
    curr_val = frog(curr)

    # Initialize counter to track function evaluations
    # Start at 1 to account for call to frog() above
    eval_amt = 1

    while True:
        best_neighbor, best_neighbor_val, evals = get_best_neighbor(curr, z, p)
        eval_amt += evals

        # Set the current point to the best neighbor found
        # Or terminate the current solution
        # And return the current point, value, and number of evaluations
        if best_neighbor_val < curr_val:
            curr = best_neighbor
            curr_val = best_neighbor_val
        else:
            return curr, curr_val, eval_amt
        
def RHCR2(sp, z, p, seed=67):
    # Run 1: start with neighborhood size z
    sol1, f_sol1, evals1 = RHC(sp, z, p, seed=seed)

    # Run 2: start from sol1 with neighborhood size z/20
    sol2, f_sol2, evals2 = RHC(sp, z / 20, p, sol1, seed=seed)

    # Run 3: start from sol2 with neighborhood size z/400
    sol3, f_sol3, evals3 = RHC(sp, z / 400, p, sol2, seed=seed)

    # Get total number of evaluations
    total_evals = evals1 + evals2 + evals3

    # Return the best solutions and associated values
    return (
        (sol1, f_sol1),
        (sol2, f_sol2),
        (sol3, f_sol3),
        (evals1, evals2, evals3, total_evals)
    )

