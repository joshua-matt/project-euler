"""
Author: Joshua Turner (https://github.com/joshua-matt)

Problem 79 (projecteuler.net/problem=79)
========================================

Problem Statement:
-----------------
A common security method used for online banking is to ask the user for three random characters from a passcode.
For example, if the passcode was 531278, they may ask for the 2nd, 3rd, and 5th characters; the expected reply would be: 317.
The text file, keylog.txt, contains fifty successful login attempts.

Given that the three characters are always asked for in order, analyse the file so as to determine the shortest possible secret passcode of unknown length.

Approach:
--------
To deduce the passcode, we leverage three observations:
    1. Successful entries preserve the order of the characters in the original passcode.
    2. A successful entry of length k implies k! pairwise orderings between its characters, since order is transitive.
    3. We can use a directed graph to represent these ordered pairwise relations.

Thus, in order to deduce the shortest possible passcode, we must find the optimal Hamiltonian path on the graph implied
by the given attempts. However, since there is only one Hamiltonian path on the graph induced by the given data, we do
not need to compute the optimum in this case. Additionally, this passcode happened to have no repeated digits, so we
did not need to account for that possibility. However, in an actual application, this would be very important to consider.
"""

import time
import networkx as nx

logins = set(map(lambda s: s[0:-1],open("data/p079_keylog.txt","r").readlines())) # Preprocess data

def extract_relations(attempts): # Extract directed edges from attempts
    return set([(a[i],a[j]) for a in attempts for i in range(len(a)-1) for j in range(i+1,len(a))])

def shortest_passcode(attempts):
    G = nx.DiGraph()
    G.add_edges_from(extract_relations(attempts)) # Load data into graph
    for v in G.nodes: # To reduce the graph to a Hamiltonian path (assuming only one exists), we remove all edges (a,c) such that (a,b) and (b,c) exist
        neighs = set(G.neighbors(v))
        for n in neighs:
            for s in neighs.intersection(G.neighbors(n)):
                if G.has_edge(v,s):
                    G.remove_edge(v,s)

    node = sorted(list(G.nodes),key=lambda v: G.in_degree(v))[0]
    code = ""
    while G.out_degree(node) != 0: # Start at node with no incoming edges and traverse path
        code += node
        node = list(G.neighbors(node))[0]
    code += node
    return code

t1 = time.time()
print(shortest_passcode(logins))
print("%s seconds elapsed" % (time.time()-t1))
