# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Algorithm framework
"""

from Shared import berlin52, stochasticTwoOpt, tourCost, euclideanDistance
import random, time


def localSearch(aSol, aCost, maxIter):
    count = 0            
    while count < maxIter:
        newSol = stochasticTwoOpt(aSol)
        newCost = tourCost(newSol)
        if newCost < aCost:
            aSol = newSol
            aCost = newCost
            count = 0
        else:
            count += 1
    return aSol, aCost

def constructGreedySolution(perm, alpha):
    # Select one node randomly and incorporate it to the emerging sol
    emergingSol = [] # permutation (list) of nodes
    problemSize = len(perm)
    emergingSol = [perm[random.randrange(0 , problemSize)]]
     # While sol size is not equal to the original permutation size

    while len(emergingSol) < problemSize:

         # Get all nodes not already in the emerging sol

        notInSolNodes = [node for node in perm if node not in emergingSol]

        # For each node not in emergingsol, compute distance w.r.t. last element

        costs = []

        emergingSolSize = len(emergingSol)

        for node in notInSolNodes:

            costs.append(euclideanDistance(emergingSol[emergingSolSize-1], node))

        # Determining the max cost and min cost from the feature set
        maxCost, minCost = max(costs), min(costs)

        # Build the RCL by adding the nodes satisfying the condition

        rcl = []

        for index, cost in enumerate(costs): # get both the index and the item

            if cost <= minCost + alpha * (maxCost-minCost):

                # Add it to the RCL
                rcl.append(notInSolNodes[index])

            #Select random feature from RCL and add it to the solution

        emergingSol.append(rcl[random.randrange(0, len(rcl))])
        # calculate the final tour cost before returning the new solution
    newCost = tourCost(emergingSol)
    # return solution and cost
    return emergingSol, newCost


#classify nodes respect position of a center
def clasify_node(center, node):
    val = [node[0]-center[0], node[1]-center[1]]
    if val[0] > 0 and val[1] >= 0:
        return 1
    elif val[0] <= 0 and val[1] > 0:
        return 2
    elif val[0] < 0 and val[1] <= 0:
        return 3
    elif val[0] >= 0 and val[1] < 0:
        return 4
    else: 
        return 0

#sort nodes in descending order with respect to euclidean distance to certain point
def sort_nodes(center, nodes):
    aux_list= nodes
    list_val = [[val,euclideanDistance(center, val)] for val in aux_list]
    list_val.sort(key=lambda x: x[1], reverse=True)
    new_list = [x[0] for x in list_val]
    newtCost = tourCost(new_list)
    
    return new_list, newtCost
    
algorithmName = "GRASP"
print("Best Sol by " + algorithmName + "... ")

#Problem configuration
inputsTSP = berlin52
maxIterations = 100
maxNoImprove = 500
greedinessFactor = 0.1 # 0 is more greedy and 1 is less
start = time.clock()


#initial solution
aux_list = inputsTSP
start_node = [aux_list[random.randrange(0 , len(aux_list))]]

#Main loop
bestCost = float("inf")
while maxIterations > 0:

    maxIterations -=1
    #construct greedy solution
    newSol, newCost = constructGreedySolution(inputsTSP, greedinessFactor)
    
    #refine it using local search heuristic
    newSol, newCost = localSearch(newSol, newCost, maxNoImprove)
    if newCost < bestCost:
        bestSol = newSol
        bestCost = newCost
        print("Cost = %.2f ; Iter = %d" % (bestCost, maxIterations))
        
#stop clock
stop = time.clock()

print("BestCost =  %.2f ; Elapsed = %.2f" % (bestCost, stop - start))
print("BestSol = %s " % bestSol)


