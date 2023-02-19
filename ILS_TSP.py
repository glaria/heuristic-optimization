# -*- coding: utf-8 -*-
"""

"""

from Shared import berlin52,tourCost, stochasticTwoOpt, constructInitialSolution
import random, time

def perturbation(aSol):
    newSol = doubleBridgeMove(aSol)
    newSolCost = tourCost(newSol)
    return newSol, newSolCost

def doubleBridgeMove(perm):
    sliceLength = len(perm)/4
    p1 = 1 + random.randrange(0, sliceLength)
    p2 = p1 +1 + random.randrange(0, sliceLength)
    p3 = p2 + 1 + random.randrange(0, sliceLength)
    
    return perm[0:p1] + perm[p3:] + perm[p2:p3] + perm[p1:p2]


def localSearch(aSol, aCost, maxIter):
    while maxIter > 0:
        maxIter -= 1
        newSol = stochasticTwoOpt(aSol)
        newCost = tourCost(newSol)
        if newCost < aCost:
            aSol = newSol
            aCost = newCost
    return aSol, aCost
    

''' ALGORITHM FRAMEWORK'''

algorithmName = "ILS"
print("Best Sol by " + algorithmName + "...")

#Problem configuration
inputsTSP = berlin52
maxIterations = 10000
maxNoimprove = 50

start = time.clock()

bestSol = constructInitialSolution(inputsTSP)
bestCost = tourCost(bestSol)

bestSol, bestCost = localSearch(bestSol, bestCost, maxNoimprove)

while maxIterations >0:
    maxIterations -= 1
    newSol, newCost = perturbation(bestSol)
    newSol, newCost = localSearch(newSol, newCost, maxNoimprove)
    if newCost < bestCost:
        bestSol = newSol
        bestCost = newCost
        print(bestCost, maxIterations)
        
stop = time.clock()

print("Cost = ", bestCost, "; Sol = ", bestSol, "; Elapsed = ", stop - start)