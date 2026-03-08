# COSC4368 Task 2

Implementation of **RHCR2** (Randomized Hill Climbing with Resampling), a probabilistic search algorithm that minimizes the `f_Frog` function over the domain $x, y \in [-512, 512]$.

$$f_{Frog}(x,y) = x \cdot \cos(\sqrt{|x+y+1|}) \cdot \sin(\sqrt{|y-x+1|}) + (1+y) \cdot \sin(\sqrt{|x+y+1|}) \cdot \cos(\sqrt{|y-x+1|})$$

---
## Files

frog.py -- Contains ``fFrog(x, y)`` function
rhc.py -- Defined RHC and RHCR2 resampling functions
main.py -- Runs the experiments and generates CSV files summarizing the results

---

## How to Run

```bash
pip install numpy
python main.py
```

---
## Outputs

Results are written to the `results/` directory. One CSV per starting point for the 32 required runs, and `bonus_runs.csv` for runs 33–34.
