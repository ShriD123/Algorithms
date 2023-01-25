import math
from typing import List


class Statistics:
    ''' 
    This class contains the relevant statistics for conducting a Monte Carlo simulation to determine the phase 
    transition threshold probability for the percolation problem.
    '''
    def __init__(self, N: int, T: int) -> None:
        ''' This class contains all the results of the simulations to be interpreted statistically.'''
        self.N = N
        self.T = T
        self.sim_values = []

    def add_sim_result(self, sim_result: float) -> None:
        ''' This adds a result of the simulation to the data for record-keeping and later statistics.'''
        self.sim_values.append(sim_result)

    def mean(self) -> float:
        ''' This returns the sample mean of the percolation threshold based off T trials'''
        return sum(self.sim_values) / self.T

    def stddev(self) -> float:
        ''' This returns the standard deviation of the percolation threshold based off T trials'''
        if self.T == 1: return 0
        
        sum_of_squares = 0
        sample_mean = self.mean()
        for _, trial_value in enumerate(self.sim_values):
            sum_of_squares += (trial_value - sample_mean)**2
        
        return sum_of_squares / (self.T-1)

    def confidenceLow(self) -> float:
        ''' This returns the lower endpoint of the 95% confidence threshold.'''
        return (self.mean() - (1.96 * self.stddev() / math.sqrt(self.T)))

    def confidenceHigh(self) -> float:
        ''' This returns the lower endpoint of the 95% confidence threshold.'''
        return (self.mean() + (1.96 * self.stddev() / math.sqrt(self.T)))
    
    def showSimulationResults(self) -> None:
        ''' This prints all the necessary statistics after completing T trials'''
        # TODO: Make it look nicer and all lined up 
        #print(f"{'Sample Mean = ':<25 + self.mean():<50} )

        print('Sample Mean = ', self.mean())
        print('Standard Deviation = ', self.stddev())
        print('95% Confidence Interval = [' + str(self.confidenceLow()) + ', ' + str(self.confidenceHigh()) + ']')
        print(str(self.N) + ' X ' + str(self.N) + ' Grid')
        print('Number of Trials: ', self.T)