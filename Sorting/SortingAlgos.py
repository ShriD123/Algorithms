# This file contains various practice sorting algorithms for implementation practice.
# Other sorts to examine : https://en.wikipedia.org/wiki/Sorting_algorithm

import math

class SortingAlgos:

    def __init__(self, data: list[int]) -> None:
        # Data is to be sorted
        self.data = data

    def merge_sort(self) -> None:
        # TODO
        pass

    def quicksort(self) -> None:
        # TODO
        pass

    def timsort(self) -> None:
        # TODO
        pass
    
    def cocktail_shaker_sort(self) -> None:
        swap = True
        # Checks if the array is sorted
        while swap:
            swap = False
            start = 0; end = len(self.data)-1

            # Restart once pointers meet in the middle
            while start <= end:
                for i in range(start, end):
                    # Traversal down the array
                    if self.data[i] > self.data[i+1]:
                        self.data[i], self.data[i+1] = self.data[i+1], self.data[i]
                        swap = True
                # Decrement the end value (placed nth largest at nth from end pos)
                end =- 1

                # If no swaps in first forward pass, array is sorted 
                if start == 0:
                    if not swap:
                        break

                for j in range(end, start-1, -1):
                    # Traversal back up the array
                    if self.data[j] < self.data[j-1]:
                        self.data[j], self.data[j-1] = self.data[j-1], self.data[j]
                        swap = True
                # Increment the start value (placed nth smallest at nth from start pos)
                start += 1


    def bubble_sort(self) -> None:
        # Test if a swap occurs or not
        swap = True
        while swap:
            swap = False
            for i in range(len(self.data)-1):
                # Note: Unoptimized bubble sort (otherwise, end point is n-i)
                if self.data[i] > self.data[i+1]:
                    self.data[i], self.data[i+1] = self.data[i+1], self.data[i]
                    swap = True


    def insertion_sort(self) -> None:
        # Skip first element
        for i in range(1, len(self.data)):
            if self.data[i] < self.data[i-1]:
                curr_value = self.data[i]

                # Iterate backwards and move up values until position found
                for j in range(i, 0, -1):
                    if curr_value < self.data[j-1]:
                        self.data[j] = self.data[j-1]
                        if j == 1:
                            # curr value is the smallest value in the array
                            self.data[0] = curr_value
                    if curr_value > self.data[j-1]:
                        self.data[j] = curr_value
                    # THIS MAY HAVE ISSUE OF CONTINUING PAST THE POINT WHERE CURR VALUE SHOULD BE KEPT
                    # BASICALLY IF CURR VALUE GOES TO 3 SPOT, SPOTS 1, 2, 3 BECOME CURR VALUE


    def selection_sort(self) -> None:
        for i in range(len(self.data)):
            # Start from index i
            min_index = self.data.index(min(self.data), i)
            self.data[i], self.data[min_index] = self.data[min_index], self.data[i]


if __name__ == '__main__':
    print('test')