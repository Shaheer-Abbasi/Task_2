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

def RHC(start_point, z, p, seed=67):
    # Set seed
    np.random.seed(seed)

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

