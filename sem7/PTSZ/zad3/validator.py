import os
import sys
from time import time

MODE_VALIDATE_INPUT = 1  # validate.py 1 folder_name surname_of_author


class Job:
    durationTime1 = None
    durationTime2 = None
    durationTime3 = None
    deadline = None
    priority = None

    def __init__(self, params):
        self.durationTime1 = params[0]
        self.durationTime2 = params[1]
        self.durationTime3 = params[2]
        self.deadline = params[3]
        self.priority = params[4]


class Solution:
    score = None
    orderList = None

    def __init__(self, score, orderList):
        self.score = score
        self.orderList = orderList


def getJobsFromFile(file):
    jobsList = []
    lineNr = 1
    for line in file.readlines():
        if lineNr > 1:
            params = [int(param) for param in line.split()]
            jobsList.append(Job(params))
            continue
        lineNr += 1
    return jobsList


def getSolutionFromFile(fileLines):
    return Solution(
        float(fileLines[0]),
        [int(index) for index in fileLines[1].split()]
    )


def checkInputFileHasIncorrectAmountOfJobs(correctAmount, jobsFromFile):
    if len(jobsFromFile) != correctAmount:
        print('Amount of jobs in input file should be %d, but was %d' % (correctAmount, len(jobsFromFile)))
        return True
    return False


def computeScore(jobs, orderLists):
    penalty = 0
    machineTime1 = 0
    machineTime2 = 0
    machineTime3 = 0
    for jobId in orderLists:
        job = jobs[jobId - 1]
        machineTime1 += job.durationTime1
        machineTime2 = max(machineTime1, machineTime2) + job.durationTime2
        machineTime3 = max(machineTime2, machineTime3) + job.durationTime3
        if machineTime3 > job.deadline:
            penalty += (machineTime3 - job.deadline) * job.priority
    sumOfPriorities = sum([job.priority for job in jobs])
    return penalty/sumOfPriorities


def computeScoreForInitialOrder(jobs):
    return computeScore(jobs, [i for i in range(1, len(jobs) + 1)])


def validateOutputFile(jobs, solution):
    return len(jobs) != len(solution.orderList) or \
           solution.score != round(computeScore(jobs, solution.orderList), 2)


if __name__ == '__main__':
    outputDir = 'countingScoresForExcel/results/' + sys.argv[1].split('.')[0]
    times = []
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    for instanceSize in range(50, 501, 50):
        startTime = time()
        os.system(sys.argv[1] + ' countingScoresForExcel/instances/KOWALCZYK/in_KOWALCZYK_' + instanceSize.__str__()  + '.txt ' + outputDir)
        endTime = time()
        times.append(round(endTime - startTime, 3))
    for instanceSize in range(50, 501, 50):
        inFile = open('countingScoresForExcel/instances/KOWALCZYK/in_KOWALCZYK_' + instanceSize.__str__() + '.txt')
        outFile = open(outputDir + '/out_KOWALCZYK_' + instanceSize.__str__() + '.txt')
        outFileLines = outFile.readlines()
        jobs = getJobsFromFile(inFile)
        solution = getSolutionFromFile(outFileLines)
        if validateOutputFile(jobs, solution):
            print('bad output for %d' % instanceSize)
        print('%s' % outFileLines[0].replace('\n', '').replace('.', ','))
    print()
    for time in times:
        print(str(time).replace('.', ','))
