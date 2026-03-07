import frog
import numpy as np

def RHC(start_point, z, p, seed=67):
    # Set seed
    np.random.seed(seed)

    # Evaulate frog for base line position
    baseline_frog = frog(start_point)

    # Initialize counter to track function evaluations
    eval_amt = 0

    # Generate random neighbors
    for i in range(z):
        # Generate random neighbor
        # Using uniform dist so neighor is within bounds [-z, z]
        distr = np.random.uniform(-z, z, size=start_point.shape)
        neighbor = start_point + distr

        eval_neighbor = eval_neighbor(neighbor)
        eval_amt += 1

        # Check if new neighbor is smaller than baseline
        if eval_neighbor is not None:
            if eval_neighbor < baseline_frog:
                # Update baseline + start point
                baseline_frog = eval_neighbor
                start_point = neighbor

    return baseline_frog, eval_amt

def eval_neighbor(neighbor):
    # Neighbor has z1 and z2 as its coordinates
    z1, z2 = neighbor
    # Check maximum bounds
    if z1 > -512 and z1 < 512 and z2 > -512 and z2 < 512:
        # Evaluate frog at neighbor position
        return frog(neighbor)
    else:
        # Clamp or maybe Discard
        return None