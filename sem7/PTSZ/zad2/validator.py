import os
import sys
from time import time

MODE_VALIDATE_INPUT = 1  # validate.py 1 folder_name surname_of_author
# MODE_VALIDATE_INPUT_AND_OUTPUT_FILES = 2  # validate.py 2 Kowalczyk KOWALCZYK Kowalczyk_OUT KOWALCZYK
# MODE_VALIDATE_INPUT_AND_OUTPUT_FILE = 3  # validate.py 3 input.txt output.txt <inputSize>
# MODE_TIME_MEASURING = 4  # validate.py 1 Kowalczyk KOWALCZYK
#
# FILE_TO_TEST = 1


class Job:
    durationTime = None
    readyTime = None

    def __init__(self, params):
        self.durationTime = params[0]
        self.readyTime = params[1]


class Solution:
    score = None
    orderList = None

    def __init__(self, score, orderList):
        self.score = score
        self.orderList = orderList


def getJobsAndMachinesFromFile(file):
    jobsList = []
    machinesList = []
    lineNr = 1
    for line in file.readlines():
        if lineNr == 2:
            machinesList = [float(param) for param in line.split()]
        if lineNr > 2:
            params = [int(param) for param in line.split()]
            jobsList.append(Job(params))
            continue
        lineNr += 1
    return jobsList, machinesList


def getSolutionFromFile(fileLines):
    return Solution(
        float(fileLines[0]),
        [
            [int(jobId) for jobId in fileLines[1].split()],
            [int(jobId) for jobId in fileLines[2].split()],
            [int(jobId) for jobId in fileLines[3].split()],
            [int(jobId) for jobId in fileLines[4].split()],
            [int(jobId) for jobId in fileLines[5].split()]
        ]
    )


def checkInputFileHasIncorrectAmountOfJobs(correctAmount, jobsFromFile):
    if len(jobsFromFile) != correctAmount:
        print('Amount of jobs in input file should be %d, but was %d' % (correctAmount, len(jobsFromFile)))
        return True
    return False


def computeScore(jobs, machines, orderLists):
    score = 0.0
    currentMachineIndex = 0
    for machineSpeed in machines:
        localTime = 0.0
        localScore = 0.0
        currentOrderList = orderLists[currentMachineIndex]
        for jobId in currentOrderList:
            job = jobs[jobId - 1]
            if localTime < job.readyTime:
                localTime = job.readyTime
            localTime += job.durationTime * machineSpeed
            localScore += localTime - job.readyTime
        score += localScore
        currentMachineIndex += 1
    return score/len(jobs)


# def computeScoreForInitialOrder(jobs, machines):
#     machineJobsListSize = len(jobs)/5
#     initialOrder = [
#         [i for i in range(1, int(machineJobsListSize + 1))],
#         [i for i in range(int(machineJobsListSize) + 1, int(machineJobsListSize * 2 + 1))],
#         [i for i in range(int(machineJobsListSize * 2) + 1, int(machineJobsListSize * 3 + 1))],
#         [i for i in range(int(machineJobsListSize * 3) + 1, int(machineJobsListSize * 4 + 1))],
#         [i for i in range(int(machineJobsListSize * 4) + 1, int(machineJobsListSize * 5 + 1))]
#     ]
#     # print(initialOrder)
#     return computeScore(jobs, machines, initialOrder)


# def validateInputFiles(argv):
#     folderName = argv[2]
#     nameInInputFiles = argv[3]
#     for amount in range(50, 500 + 1, 50):
#         inFile = open(folderName + '/in_' + nameInInputFiles + '_' + amount.__str__() + '.txt', "r")
#         jobs, machines = getJobsAndMachinesFromFile(inFile)
#         print(str(round(computeScoreForInitialOrder(jobs, machines), 2)).replace('.', ','))
#         if checkInputFileHasIncorrectAmountOfJobs(amount, jobs): print('^ Invalid input for size = %d\n' % amount)


def validateOutputFile(jobs, machines, solution):
    return len(jobs) != sum([len(machineJobs) for machineJobs in solution.orderList]) or \
           solution.score != round(computeScore(jobs, machines, solution.orderList), 2)


if __name__ == '__main__':
    outputDir = 'instances/Kowalczyk/' + sys.argv[1].split('.')[0]
    times = []
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    for instanceSize in range(50, 501, 50):
        startTime = time()
        os.system(sys.argv[1] + ' instances/Kowalczyk/in_KOWALCZYK_' + instanceSize.__str__()  + '.txt ' + outputDir)
        endTime = time()
        times.append(round(endTime - startTime, 3))
    for instanceSize in range(50, 501, 50):
        inFile = open('instances/Kowalczyk/' + 'in_KOWALCZYK_' + instanceSize.__str__() + '.txt')
        outFile = open('instances/Kowalczyk/' + sys.argv[1].split('.')[0] + '/out_KOWALCZYK_' + instanceSize.__str__() + '.txt')
        outFileLines = outFile.readlines()
        jobs, machines = getJobsAndMachinesFromFile(inFile)
        solution = getSolutionFromFile(outFileLines)
        if validateOutputFile(jobs, machines, solution):
            print('bad output for %d' % instanceSize)
        print('%s' % outFileLines[0].replace('\n', '').replace('.', ','))
    print()
    for time in times:
        print(str(time).replace('.', ','))
