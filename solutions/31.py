"""
Author: Joshua Turner (https://github.com/joshua-matt)

Problem 31 (projecteuler.net/problem=31)
========================================

Problem Statement:
-----------------

In the United Kingdom the currency is made up of pound (£) and pence (p). There are eight coins in general circulation:

    1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).

It is possible to make £2 in the following way:

    1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p

How many different ways can £2 be made using any number of coins?

Approach:
--------

Recursively break the problem of finding the number of combinations to make `total` into finding the number of combinations
that use the last coin in the given list and the number of combinations that don't use the last coin. Naive recursion ends up
performing redundant computation by repeatedly solving subproblems from scratch, so we use memoization to significantly
speed up the program.
"""

import numpy as np
import time

def coin_sum_recursive(total, coins):
    if total == 0: # Base case: there is one combination which sums to zero, which is: don't use any coins
        return 1
    if total < 0 or len(coins) == 0: # Base case: there are no combinations for negative totals or nonzero totals with no coins
        return 0
    return coin_sum_recursive(total, coins[:-1]) + coin_sum_recursive(total - coins[-1], coins)

def coin_sum_dynamic(total, coins):
    table = np.zeros((total+1, len(coins))) # Memoization table, where table[i,j] = # of ways to make i using the first j coins
    table[0,:] = 1 # Base case: there is one combination which sums to zero, which is: don't use any coins
    for i in range(1,total+1):
        for j in range(len(coins)):
            table[i,j] = (table[i, j-1] if j >= 1 else 0) + (table[i-coins[j], j] if i-coins[j] >= 0 else 0)
    return int(table[-1,-1])

t1 = time.time()
print(coin_sum_recursive(200,[1,2,5,10,20,50,100,200]))
print("Recursive solution took %.5f seconds" % (time.time()-t1))

t1 = time.time()
print(coin_sum_dynamic(200,[1,2,5,10,20,50,100,200]))
print("DP solution took %.5f seconds" % (time.time()-t1))