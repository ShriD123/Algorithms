# https://coursera.cs.princeton.edu/algs4/assignments/percolation/specification.php
import random
import sys
import matplotlib.pyplot as plt
from typing import Tuple, List
from PercolationUtils import Statistics, Visualizer


class QuickFind:
    '''
    This class contains the functionality for the Weighted Quick-Union Algorithm for the NxN grid Percolation problem.
    A Monte Carlo simulation is then applied to estimate the phase transition point for when percolation is more likely to occur than not.
    '''
    # TODO: Implement Path Compression

    def __init__(self, N: int) -> None:
        '''Contains the ID and Size array for the Weighted Quick-Union Algorithm.
        ID Array -- id[(i,j)] gives index of the parent of (i,j). This creates a tree data structure. Root of tree points to itself.
        ID Array -- sized at N+2 X N to introduce virtual top and bottom site so only one call to connected instead of 2N
        Size Array -- size[(i,j)] gives the number of objects in a tree rooted at (i,j).'''

        self.id = [[(i, j) for j in range(N)] for i in range(N+2)]
        self.size = [[1 for j in range(N)] for i in range(N+2)]
        self.vtop = (0, 0)
        self.vbottom = (N+1, N-1)

        # Adjust virtual top and bottom rows so only (0,0) and (N+1,N-1) <==> (-1,-1) are valid (rest are None)
        self.id[0], self.id[-1] = [None]*N, [None]*N
        self.id[self.vtop[0]][self.vtop[1]] = self.vtop
        self.id[self.vbottom[0]][self.vbottom[1]] = self.vbottom
        self.size[0], self.size[-1] = [None]*N, [None]*N
        self.size[self.vtop[0]][self.vtop[1]] = 1
        self.size[self.vbottom[0]][self.vbottom[1]] = 1

        # Make connections of top and bottom sites to top and bottom rows respectively
        for i in range(N):
            self.union(self.vtop, (1, i))
            self.union(self.vbottom, (N, i))

    def root(self, x: Tuple[int, int]) -> Tuple[int, int]:
        ''' Returns the index corresponding to the root of a connected component.'''
        idx, idy = x
        while ((idx, idy) != self.id[idx][idy]):
            idx, idy = self.id[idx][idy]
            # TODO: Path compression here
        
        return (idx, idy)

    def is_connected(self, a: Tuple[int, int], b: Tuple[int, int]) -> bool:
        '''Two elements are connected if they are in the same connected component. Connected components are in a tree-like structure,
        so two connected elements have the same root.'''
        if type(a) is not tuple or type(b) is not tuple:
            raise TypeError('Inputs to Is_Connected Are Not All Tuples')

        return self.root(a) == self.root(b)

    def union(self, a: Tuple[int, int], b: Tuple[int, int]) -> None:
        ''' Connects two components by changing the root of one to point to the root of the other.'''
        if type(a) is not tuple or type(b) is not tuple:
            raise TypeError('Inputs to Union Are Not All Tuples')
        if self.is_connected(a, b): return

        root_ax, root_ay = self.root(a)
        root_bx, root_by = self.root(b)
        if self.size[root_ax][root_ay] >= self.size[root_bx][root_by]:
            self.id[root_bx][root_by] = (root_ax, root_ay)
            self.size[root_ax][root_ay] += self.size[root_bx][root_by]
        else:
            self.id[root_ax][root_ay] = (root_bx, root_by)
            self.size[root_bx][root_by] += self.size[root_ax][root_ay]


class Percolation:
    '''This class contains the functionality for running a trial and determining when a NxN grid percolates.'''

    CLOSED = 0
    OPEN = 1
    #FULL = 2            # TODO: Only for visualization purposes

    def __init__(self, N: int) -> None:
        '''Contains the data structures for percolation and visualization of the simulation.
        Grid array -- Initializes with all slots blocked. This is used to help with visualization of the simulation.
        QF object -- Initializes the algorithm used to solve the dynamic connectivity problem. '''
        self.N = N
        self.qf = QuickFind(self.N)

        # To match indices with the quick find implementation for avoiding confusion
        self.grid = [[self.CLOSED for j in range(N)] for i in range(N+2)]
        self.grid[0] = [None]*N; self.grid[-1] = [None]*N

        # TODO: Purely for visualization purposes
        # self.declare_vis_params()

    def open_cell(self, row: int, col: int) -> None:
        '''This function opens a given cell and connects the adjacent open cells using the QuickFind object. Valid Indices: Row is 1...N and Col is 0...N-1'''
        if not (type(row) is int and type(col) is int):
            raise TypeError('Only integer values permitted for Row/Col.')
        if not (0 < row <= self.N and 0 <= col < self.N):
            raise ValueError('Row/Col values are out of bounds.')

        if self.grid[row][col] == self.OPEN: return
        self.grid[row][col] = self.OPEN

        # Connect four adjacent spots, if open, in QF (not diagonals)
        if row-1 >= 1:
            if self.grid[row-1][col] == self.OPEN:
                self.qf.union((row, col), (row-1, col))
        if row+1 <= self.N:
            if self.grid[row+1][col] == self.OPEN:
                self.qf.union((row, col), (row+1, col))
        if col-1 >= 0:
            if self.grid[row][col-1] == self.OPEN:
                self.qf.union((row, col), (row, col-1))
        if col+1 <= self.N-1:
            if self.grid[row][col+1] == self.OPEN:
                self.qf.union((row, col), (row, col+1))

    def frac_open_sites(self) -> float:
        ''' This function determines the number of open sites at time of percolation.'''
        return (sum(row.count(self.OPEN) for row in self.grid)) / (self.N**2)
        
    def percolates(self) -> bool:
        ''' This function determines if the system percolates top to bottom.'''
        return self.qf.is_connected(self.qf.vbottom, self.qf.vtop)

    def is_full(self, row: int, col: int) -> bool:
        ''' This function determines if a particular site is full (connects to top row)'''
        if not (type(row) is int and type(col) is int):
            raise TypeError('Only integer values permitted for Row/Col.')
        if not (0 < row <= self.N and 0 <= col < self.N):
            raise ValueError('Row/Col values are out of bounds.')
        
        return self.qf.is_connected(self.qf.vtop, (row, col))

    def declare_vis_params(self) -> None:
        self.vis = [[self.CLOSED for j in range(N)] for i in range(N)]
        self.fig, self.ax = plt.subplots()

        self.ax.set_title('Percolation Simulation')
        # May need to set the ticks to get the grid as desired
        self.ax.grid(True, color='k')

        # TODO

    def update_vis_grid(self) -> List[List[int]]:
        ''' This function updates the previous state of the visualization 2D array to account for
        the incremental change in the Monte Carlo simulation.'''
        for i in range(self.N):
            for j in range(self.N):
                # Skip the closed and already full locations
                if self.grid[i+1][j] == self.CLOSED:
                    continue
                if self.vis[i][j] == self.FULL:
                    continue
                
                if self.is_full(i+1, j):
                    self.vis[i][j] = self.FULL
                else:
                    self.vis[i][j] = self.OPEN
        
    def draw_vis_grid(self) -> None:
        ''' This function draws the current state of the visualization with Matplotlib.'''
        # TODO: Implement later
        pass


if __name__ == '__main__':
    # From command line, submit two values: N & T & visualize (boolean)
    N = int(sys.argv[1])
    T = int(sys.argv[2])
    visualize = bool(sys.argv[3])

    if visualize:
        pass
    else:
        stats = Statistics(N, T)

        for trialInd in range(T):
            curr_trial = Percolation(N)
            print('Trial ' + str(trialInd) + ' Complete', end='\r')

            while not curr_trial.percolates():
                rand_x = random.randint(1, N)
                rand_y  = random.randint(0, N-1)
                curr_trial.open_cell(rand_x, rand_y)
            stats.add_sim_result(curr_trial.frac_open_sites())
        stats.showSimulationResults()