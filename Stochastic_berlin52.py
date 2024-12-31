# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 11:05:42 2022

@author: Luis Alberto Glaría Silva
"""

import numpy as np
import math


berlin52 = [[565,575], [25, 185], [345, 750],[945, 685], [845,655],
            [880,660], [25,230], [525,1000],[580, 1175], [650, 1130],[1605,620],
            [1220,580],[1465, 200],[1530,5], [845, 680],[725,370],[145,665],
            [415,635], [510,875], [560,365],[300, 465], [520,585], [480,415],
            [835,625], [975,580],[1215,245],[1320,315], [1250, 400],[660,180],
            [410,250],[420,555], [575,665],[1150, 1160],[700,580],[685,595],
            [685,610],[770,610],[795,645],[720,635],[760,650], [475,960],
            [95,250],[875,920],[700,500],[555, 815], [830,485],[1170,65],
            [830,610],[605,625], [595,360],[1340,725],[1740,245]]


def euclidean_distance(x_node, y_node):
    return math.sqrt(sum((xi - yi) ** 2 for xi, yi in zip(x_node, y_node)))

def generate_stochastic_dataset(dataset, stochastic=False):
    berlin52_stochastic = {}
    n = len(dataset)
    
    # Iterate over unique pairs using the upper triangle of the distance matrix
    for i in range(n):
        node_a = str(dataset[i])
        berlin52_stochastic[node_a] = {}
        
        for j in range(i, n):
            node_b = str(dataset[j])
            
            # Calculate Euclidean distance
            distance = euclidean_distance(dataset[i], dataset[j])
            
            # Add stochasticity if required
            if stochastic:
                distance = np.random.lognormal(mean=distance, sigma=0.1)
            
            # Store symmetric distances
            berlin52_stochastic[node_a][node_b] = distance
            berlin52_stochastic.setdefault(node_b, {})[node_a] = distance

    return berlin52_stochastic


# Generate the dataset with optional stochasticity
stochastic_dataset = generate_stochastic_dataset(berlin52, stochastic=False)

# Example: Print the distance between two specific nodes
print("Distance between [565, 575] and [25, 185]:", stochastic_dataset["[565, 575]"]["[25, 185]"])

