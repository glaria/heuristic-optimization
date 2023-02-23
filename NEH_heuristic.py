# -*- coding: utf-8 -*-

"""
 
Employs Taillard's accelerations to compute the best position for a job,

and returns makespan without directly using the calcMakespan function """

from PFSP_elements import Job, Solution

import operator
import time     

def improveByShiftingJobToLeft(aSol, k):
    #implements Taillard's acceleration, where k is the position of the job
    # on the right extreme; it also updates makespan if k == nJobs - 1
    bestPosition = k
    minMakespan = float('inf')
    eMatrix = calcEMatrix(aSol, k)
    qMatrix = calcQMatrix(aSol, k)
    fMatrix = calcFMatrix(aSol, k, eMatrix)
    # compute bestPosition (0...k) and minMakespan (mVector)
    for i in range (k, -1, -1):
        maxSum = 0.0
        for j in range(aSol.nMachines) :
            newSum = fMatrix[i][j] + qMatrix[i][j]
            if newSum > maxSum: maxSum = newSum
        newMakespan = maxSum
        # TIE ISSUE No.2 - In case of tie, do swap (it might affect the final result)
        if newMakespan <= minMakespan:
            minMakespan = newMakespan
            bestPosition = i
    # update solution with bestPosition and minMakespan
    if bestPosition < k: # if i == k do nothing
        auxJob = aSol.jobs[k]
        for i in range(k, bestPosition, -1):
            aSol.jobs[i] = aSol.jobs[i - 1]
        aSol.jobs[bestPosition] = auxJob
    if k == aSol.nJobs - 1:
        aSol.makespan = minMakespan
    return aSol

def calcEMatrix(aSol, k):
    nRows = k
    nCols = nMachines
    e = [[0 for j in range(nCols)] for i in range(nRows)]

    for i in range(k):     

        for j in range(nMachines): 
            if i == 0 and j == 0: e[0][0] = aSol.jobs[0].processingTimes[0]
            elif j == 0: e[i][0] = e[i-1][0] + aSol.jobs[i].processingTimes[0]
            elif i == 0: e[0][j] = e[0][j-1] + aSol.jobs[0].processingTimes[j]
            else:
                maxTime = max(e[i-1][j], e[i][j-1])
                e[i][j] = maxTime + aSol.jobs[i].processingTimes[j]
    return e


def calcQMatrix(aSol, k):
    nRows = k+1
    nCols = nMachines
    q = [[0 for j in range(nCols)] for i in range(nRows)]

    for i in range(k, -1, -1):
        for j in range(nMachines-1, -1, -1):
            if i == k:
                q[k][j] = 0
            elif i == k-1 and j == nMachines -1:
                q[k-1][nMachines -1] = aSol.jobs[k-1].processingTimes[nMachines-1]
                
            elif j == nMachines - 1: 

                q[i][nMachines-1] = q[i+1][nMachines-1] + aSol.jobs[i].processingTimes[nMachines - 1]
            elif i == k -1:

                q[k-1][j] = q[k-1][j+1] + aSol.jobs[k-1].processingTimes[j]
            else:

                maxTime = max(q[i + 1][j], q[i][j + 1])

                q[i][j] = maxTime + aSol.jobs[i].processingTimes[j]

    return q

 
def calcFMatrix(aSol, k, e):
    nRows = k + 1
    nCols = nMachines
    f= [[0 for j in range(nCols)] for i in range(nRows)]
    for i in range(k+1):
        for j in range(nMachines):
            if i == 0 and j == 0:
                f[0][0] = aSol.jobs[k].processingTimes[0]
            elif j == 0:
                f[i][0] = e[i-1][0] + aSol.jobs[k].processingTimes[0]
            elif i == 0:
                f[0][j] = f[0][j-1] + aSol.jobs[k] .processingTimes[j]
            else:
                maxTime = max(e[i-1][j], f[i][j-1])
                f[i][j] = maxTime +aSol.jobs[k].processingTimes[j]

 
    return f
 

""" NEH HEURISTIC FOR THE PERMUTATION FLOW-SHOP PROBLEM (PFSP)"""


""" Read instance data from txt file """

instanceName = 'tai109_200_20' # name of the instance
#txt file with the instance

fileName = 'data/' + instanceName + '_inputs.txt'

with open(fileName) as instance:
    i = -3 # we start at -3 so that the first job is job 0
    jobs = []
    for line in instance:
        if i == -3: pass # line 0 contains a symbol #
        elif i == -2:
            nJobs = int(line.split()[0])
            nMachines = int(line.split()[1])
        elif i == -1: pass
        else:
            # array data with processint time of job i in machine j
            data = [float(x) for x in line.split('\t')]
            TPT = sum(data) # total processing time of this job in the system
            aJob = Job(i, data, TPT)
            jobs.append(aJob)
        i+= 1

 

tStart = time.time()
# generate sorted jobs list (TIE ISSUE No.1, it might affect the final result)
jobs.sort(key = operator.attrgetter('TPT'), reverse = True)

# insert the first job in the solution (not an empty solution anymore)
sol = Solution(nJobs, nMachines)

index = 5 # greedy behavior (can be changed by a biased-rand behavior)
sol.jobs.append (jobs [index] )

# complete the solution with the remaining jobs

for i in range(1, nJobs):
# add nextJob to the end of current sol (partial solution)
    index = i # greedy behavior (can be changed by a biased-rand behavior)
    sol. jobs.append(jobs[index])
    # try to improve current sol by shifting job in position i to its left
    sol = improveByShiftingJobToLeft(sol, i)

tEnd = time.time()

""" Print Solution """

print('Instance:', instanceName, 'with', nJobs, 'jobs and', nMachines, 'machines')
print('NEH makespan with Taillard acceleration =', "{:.{}f}".format(sol.makespan, 2))
print('NEH verification with traditional method:', "{:.{}f}".format(sol.calcMakespan(),2))
print('Computational time:', "{:.{}f}".format(tEnd - tStart, 1), "sec.")
permutation = '('
for job in jobs:

    permutation = permutation + str(job.ID) +" "

print('Sol:', permutation, ')') 
     

  
 



