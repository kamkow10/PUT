import os
import sys
from time import time

MODE_VALIDATE_INPUT = 1             # validate.py 1 Kowalczyk KOWALCZYK
MODE_VALIDATE_INPUT_AND_OUTPUT_FILES = 2  # validate.py 2 Kowalczyk KOWALCZYK Kowalczyk_OUT KOWALCZYK
MODE_VALIDATE_INPUT_AND_OUTPUT_FILE = 3             # validate.py 3 input.txt output.txt <inputSize>
MODE_TIME_MEASURING = 4             # validate.py 1 Kowalczyk KOWALCZYK

FILE_TO_TEST = 1

DEBUG = False


class Job:
    durationTime = None
    readyTime = None
    endTime = None
    priority = None

    def __init__(self, params):
        self.durationTime = params[0]
        self.readyTime = params[1]
        self.endTime = params[2]
        self.priority = params[3]

    def hasTooSmallEndTime(self):
        return (self.readyTime + self.durationTime) > self.endTime

    def hasAnyParamWithIncorrectMinimumValue(self):
        return self.durationTime < 1 or self.endTime < 1 or self.readyTime < 0 or self.priority < 0


class Solution:
    score = None
    orderList = None

    def __init__(self, score, orderList):
        self.score = score
        self.orderList = orderList


def getJobsFromFile(file):
    jobsList = []
    for line in file.readlines():
        params = [int(param) for param in line.split()]
        if len(params) is 1:
            continue
        jobsList.append(Job(params))
    return jobsList


def getSolutionFromFile(file):
    lines = file.readlines()
    return Solution(int(lines[0].split()[0]), [int(jobId) for jobId in lines[1].split()])


def checkInputFileHasIncorrectAmountOfJobs(correctAmount, jobsFromFile):
    if len(jobsFromFile) != correctAmount:
        print('Amount of jobs in input file should be %d, but was %d' % (correctAmount, len(jobsFromFile)))
        return True
    return False


def checkInstanceHasAnyIncorrectJob(jobs):
    for job in jobs:
        if job.hasTooSmallEndTime() or job.hasAnyParamWithIncorrectMinimumValue():
            print(
                "Job #%d with params: (%d %d %d %d) is incorrect"
                % (jobs.index(job), job.durationTime, job.readyTime, job.endTime, job.priority)
            )
            return True
    return False


def computeScoreForInitialOrder(jobs):
    time = 0
    score = 0
    for jobId in range(1, len(jobs) + 1):
        job = jobs[jobId - 1]
        if time < job.readyTime:
            time = job.readyTime
        time += job.durationTime
        if time > job.endTime:
            score += job.priority
    return score


def computeScore(jobs, orderList):
    time = 0
    score = 0
    for jobId in orderList:
        job = jobs[jobId - 1]
        if time < job.readyTime:
            time = job.readyTime
        time += job.durationTime
        if time > job.endTime:
            score += job.priority
    return score


def validateInputFiles(argv):
    folderName = argv[2]
    nameInInputFiles = argv[3]
    for amount in range(50, FILE_TO_TEST * 50 + 1, 50):
        inFile = open(folderName + '/in_' + nameInInputFiles + '_' + amount.__str__() + '.txt', "r")
        jobs = getJobsFromFile(inFile)
        print(int(amount / 50))
        print(computeScoreForInitialOrder(jobs))
        print('Incorrect\n' if validateInputFile(jobs, amount) else 'Correct\n')


def validateInputFile(jobs, expectedAmountOfJobs):
    return checkInstanceHasAnyIncorrectJob(jobs) or checkInputFileHasIncorrectAmountOfJobs(expectedAmountOfJobs, jobs)


def validateOutputFile(jobs, solution):
    return len(jobs) != len(solution.orderList) or solution.score != computeScore(jobs, solution.orderList)


def validateInputAndOutputFiles():
    print('\n Validation:\n')
    for instanceSize in range(50, 501, 50):
        inFile = open('instances/Kowalczyk/in_KOWALCZYK_' + instanceSize.__str__() + '.txt', 'r')
        outFile = open('instances/Kowalczyk/out_KOWALCZYK_' + instanceSize.__str__() + '.txt', 'r')
        jobs = getJobsFromFile(inFile)
        solution = getSolutionFromFile(outFile)
        print(instanceSize.__str__() + '\t: ' + ('Incorrect input file. ' if validateInputFile(jobs, instanceSize) else 'Correct input file. ')
            + ('Incorrect output file.' if validateOutputFile(jobs, solution) else 'Correct output file.'))


def validateInputAndOutputFile(argv):
    inFile = argv[2]
    outFile = argv[3]
    inputSize = int(argv[4])
    inFile = open(inFile, "r")
    outFile = open(outFile, "r")
    jobs = getJobsFromFile(inFile)
    solution = getSolutionFromFile(outFile)
    print('Incorrect input file' if validateInputFile(jobs, inputSize) else 'Correct input file')
    print('Incorrect output file\n' if validateOutputFile(jobs, solution) else 'Correct output file\n')


def measureTimeForAlgorithm(argv):
    print('\n Times:\n')
    for instanceSize in range(50, 501, 50):
        startTime = time()
        os.system(argv[2] + ' instances/Kowalczyk/in_KOWALCZYK_' + instanceSize.__str__() + '.txt instances/Kowalczyk/')
        endTime = time()
        result = round(endTime - startTime, 3)
        print(str(result).replace('.', ','))


def printResults():
    print('\n Scores:\n')
    for instanceSize in range(50, 501, 50):
        outFile = open('instances/Kowalczyk/out_KOWALCZYK_' + instanceSize.__str__() + '.txt', 'r')
        print(outFile.readline().split('\n')[0])


if __name__ == '__main__':
    argv = sys.argv
    MODE = int(argv[1])
    if MODE is MODE_VALIDATE_INPUT:
        validateInputFiles(argv)
    elif MODE is MODE_VALIDATE_INPUT_AND_OUTPUT_FILE:
        validateInputAndOutputFile(argv)
    elif MODE is MODE_TIME_MEASURING:
        measureTimeForAlgorithm(argv)
        validateInputAndOutputFiles()
        printResults()