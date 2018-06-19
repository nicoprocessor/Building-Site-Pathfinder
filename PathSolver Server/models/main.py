import os
import pathlib
import models as pf

if __name__ == '__main__':
    grid = pf.Grid(start_coord=None, end_coord=None, rows=5, cols=5)
    print(grid)
    feasible, path = grid.a_star()
    print("Is feasible? {}".format(feasible))
