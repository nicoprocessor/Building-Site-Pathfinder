import pathfinder as pf
import path_converter as pc

if __name__ == '__main__':
    grid = pf.Grid(start_coord=None, end_coord=None, rows=5, cols=5)
    feasible, path = grid.a_star()
    print("Is feasible? {}".format(feasible))
