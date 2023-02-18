# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 10:51:39 2022

@author: Luis Alberto Glaría Silva
"""

import random, time, math
import pandas as pd

berlin52 = [[565,575], [25, 185], [345, 750],[945, 685], [845,655],
            [880,660], [25,230], [525,1000],[580, 1175], [650, 1130],[1605,620],
            [1220,580],[1465, 200],[1530,5], [845, 680],[725,370],[145,665],
            [415,635], [510,875], [560,365],[300, 465], [520,585], [480,415],
            [835,625], [975,580],[1215,245],[1320,315], [1250, 400],[660,180],
            [410,250],[420,555], [575,665],[1150, 1160],[700,580],[685,595],
            [685,610],[770,610],[795,645],[720,635],[760,650], [475,960],
            [95,250],[875,920],[700,500],[555, 815], [830,485],[1170,65],
            [830,610],[605,625], [595,360],[1340,725],[1740,245]]

# Function that deletes two edges and reverses the sequence in between the deleted edges
def stochasticTwoOpt(perm):
    result = perm[:] # make a copy
    size = len(result)
    # select indices of two random points in the tour
    p1, p2 = random.randrange(0,size), random.randrange(0,size)
    # do this so as not to overshoot tour boundaries
    exclude = set([p1])
    
    if p1 == 0:
        exclude.add(size-1)
    else:
        exclude.add(p1-1)
    if p1 == size-1:
        exclude.add(0)
    else:
        exclude.add(p1+1)                       
    while p2 in exclude:
        p2 = random.randrange(0,size)

    # to ensure we always have p1<p2        
    if p2<p1:
        p1, p2 = p2, p1
        
    # now reverse the tour segment between p1 and p2   
    result[p1:p2] = reversed(result[p1:p2])
    
    return result


#evaluates total length of TSP solution
def tourCost(perm):
    # Here tour cost refers to the sum of the euclidean distance between consecutive points starting from first element
    totalDistance =0.0
    size = len(perm)
    for index in range(size):
        # select the consecutive point for calculating the segment length
        if index == size-1 : 
            # This is because in order to complete the 'tour' we need to reach the starting point
            point2 = perm[0] 
        else: # select the next point
            point2 = perm[index+1]
            
        totalDistance +=  euclideanDistance(perm[index], point2)
    
    return totalDistance   

def euclideanDistance(xNode, yNode):
    sum = 0.0
    
    for xi, yi in zip(xNode, yNode):
        sum += pow((xi-yi), 2)
    return math.sqrt(sum)

def constructInitialSolution(initPerm):
    permutation = initPerm[:]
    size = len(permutation)
    for index in range(size):
        shuffleIndex = random.randrange(index, size)
        permutation[shuffleIndex], permutation[shuffleIndex]
    return permutation

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

results = []

for i in range(100):
    print ("In execution: ", i)
    start = time.clock()
    
    bestSol = constructInitialSolution(inputsTSP)
    bestCost = tourCost(bestSol)
    
    bestSol, bestCost = localSearch(bestSol, bestCost, maxNoimprove)
    maxIterations_mod = maxIterations

    while maxIterations_mod >0:
        maxIterations_mod -= 1
        newSol, newCost = perturbation(bestSol)
        newSol, newCost = localSearch(newSol, newCost, maxNoimprove)
        if newCost < bestCost:
            bestSol = newSol
            bestCost = newCost
            
    stop = time.clock()
    results.append([bestCost,  stop - start])

results = (pd.DataFrame(results, columns=["bestCost", "Execution Time"]))  
results.to_csv('results_ILS.csv')
print(results.describe())  
#print("Cost = ", bestCost, "; Sol = ", bestSol, "; Elapsed = ", stop - start)

#print("Cost = ", bestCost, "; Sol = ", bestSol, "; Elapsed = ", stop - start)