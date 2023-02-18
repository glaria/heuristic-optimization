# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 11:05:42 2022

@author: Luis Alberto Glaría Silva
"""

#import numpy as np
import math

def euclideanDistance(xNode, yNode):
    sum = 0.0
    
    for xi, yi in zip(xNode, yNode):
        sum += pow((xi-yi), 2)
    return math.sqrt(sum)

berlin52 = [[565,575], [25, 185], [345, 750],[945, 685], [845,655],
            [880,660], [25,230], [525,1000],[580, 1175], [650, 1130],[1605,620],
            [1220,580],[1465, 200],[1530,5], [845, 680],[725,370],[145,665],
            [415,635], [510,875], [560,365],[300, 465], [520,585], [480,415],
            [835,625], [975,580],[1215,245],[1320,315], [1250, 400],[660,180],
            [410,250],[420,555], [575,665],[1150, 1160],[700,580],[685,595],
            [685,610],[770,610],[795,645],[720,635],[760,650], [475,960],
            [95,250],[875,920],[700,500],[555, 815], [830,485],[1170,65],
            [830,610],[605,625], [595,360],[1340,725],[1740,245]]


def generateStochasticDataset(dataset):
    berlin52_stochastic = {}
    berlin52 = dataset
    for node in berlin52:
        berlin52_stochastic[str(node)] = {}
        for node1 in berlin52:
             berlin52_stochastic[str(node)][str(node1)] = ([euclideanDistance(node,node1), euclideanDistance(node,node1)])
         #berlin52_stochastic[str(node)][str(node1)] = (np.random.lognormal(euclideanDistance(node,node1), euclideanDistance(node,node1), 10))
    return berlin52_stochastic

