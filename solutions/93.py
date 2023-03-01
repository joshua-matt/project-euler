"""
Problem 93: Arithmetic Expressions

By using each of the digits from the set, {1, 2, 3, 4}, exactly once, and making use of the four arithmetic operations
(+, −, *, /) and brackets/parentheses, it is possible to form different positive integer targets.

For example,

8 = (4 * (1 + 3)) / 2
14 = 4 * (3 + 1 / 2)
19 = 4 * (2 + 3) − 1
36 = 3 * 4 * (2 + 1)

Note that concatenations of the digits, like 12 + 34, are not allowed.

Using the set, {1, 2, 3, 4}, it is possible to obtain thirty-one different target numbers of which 36 is the maximum,
and each of the numbers 1 to 28 can be obtained before encountering the first non-expressible number.

Find the set of four distinct digits, a < b < c < d, for which the longest set of consecutive positive integers, 1 to n,
can be obtained, giving your answer as a string: abcd.
"""

import re
import numpy as np
from itertools import permutations

def generate_prefix_formats(n):
    if n == 1:
        return ["+ 1 2", "- 1 2", "* 1 2", "/ 1 2"]
    else:
        smaller = generate_prefix_formats(n-1)
        bigger = []
        for formats in smaller:
            bigger += ["+ " + formats + " " + str(n + 1), "+ " + str(n + 1) + " " + formats]
            bigger += ["- " + formats + " " + str(n + 1), "- " + str(n + 1) + " " + formats]
            bigger += ["* " + formats + " " + str(n + 1), "* " + str(n + 1) + " " + formats]
            bigger += ["/ " + formats + " " + str(n + 1), "/ " + str(n + 1) + " " + formats]
        return bigger

formats = generate_prefix_formats(3)

def generate_prefix(nums): # len(nums) = 4, len(ops) = 3
    prefixes = []
    orderings = [''.join(p) for p in permutations('1234')]
    exprs = "|".join(formats)
    for o in orderings:
        expr = exprs.replace(o[0], str(nums[0]))
        expr = expr.replace(o[1], str(nums[1]))
        expr = expr.replace(o[2], str(nums[2]))
        expr = expr.replace(o[3], str(nums[3]))
        expr = expr.split("|")
        prefixes += expr
    return list(set(prefixes))

def evaluate_prefix(expr):
    original_expr = expr

    ops = {'+': np.add,
           '-': np.subtract,
           '*': np.multiply,
           '/': np.divide}

    for _ in range(3): # Three operations will be evaluated
        subexpr = re.findall(r'(([/\*\+-]) (-?\d+(\.\d+)?) (-?\d+(\.\d+)?))', expr)
        for e in subexpr:
            el = [e[1], e[2], e[4]]
            if el[0] == "/" and float(el[2]) == 0.0:
                return np.inf
            ans = ops[el[0]](float(el[1]), float(el[2]))
            expr = expr.replace(e[0], str(ans))
    return (float(expr), original_expr)

def evaluate_prefixes(exprs):
    return set(
        filter(
            lambda x: not np.isinf(x[0]) and x[0]-int(x[0])==0 and x[0] > 0,
            [evaluate_prefix(e) for e in exprs])
    )

print(evaluate_prefixes(generate_prefix([1,1,1,1]))) # TODO: left off here. Some expression is causing issues. evaluate_prefix seems to work, as does generate_prefix and generate_prefix_formats

