# -*- coding: utf-8 -*-

import math, random


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