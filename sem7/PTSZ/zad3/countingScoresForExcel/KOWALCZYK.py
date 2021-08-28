import sys
import os


class Job:
    durationTime1 = None
    durationTime2 = None
    durationTime3 = None
    deadline = None
    priority = None
    index = None

    def __init__(self, params):
        self.durationTime1 = params[0]
        self.durationTime2 = params[1]
        self.durationTime3 = params[2]
        self.deadline = params[3]
        self.priority = params[4]
        self.index = params[5]


class Solution:
    score = None
    orderList = None

    def __init__(self, score, orderList):
        self.score = score
        self.orderList = orderList

    def saveToFile(self, file):
        file.write("%.2f\n" % self.score)
        file.write(self.getOrderListAsString())

    def getOrderListAsString(self):
        listAsString = ''
        for jobId in self.orderList:
            listAsString += jobId.__str__() + ' '
        return listAsString


def getJobsFromFile(file):
    jobsList = []
    lineNr = 1
    index = 0
    for line in file.readlines():
        if lineNr > 1:
            index += 1
            params = [int(param) for param in line.split()]
            params.append(index)
            jobsList.append(Job(params))
            continue
        lineNr += 1
    return jobsList


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
    return penalty / sumOfPriorities


def computePenaltyForNextTwoJobs(firstJob, secondJob, machineTime1, machineTime2, machineTime3):
    penalty = 0
    machineTime1 += firstJob.durationTime1
    machineTime2 = max(machineTime1, machineTime2) + firstJob.durationTime2
    machineTime3 = max(machineTime2, machineTime3) + firstJob.durationTime3
    if machineTime3 > firstJob.deadline:
        penalty += (machineTime3 - firstJob.deadline) * firstJob.priority
    machineTime1 += secondJob.durationTime1
    machineTime2 = max(machineTime1, machineTime2) + secondJob.durationTime2
    machineTime3 = max(machineTime2, machineTime3) + secondJob.durationTime3
    if machineTime3 > secondJob.deadline:
        penalty += (machineTime3 - secondJob.deadline) * secondJob.priority
    return penalty


def algorithmMultipleSwaping(jobs):
    jobsSorted = sorted(jobs, key=lambda job: (job.deadline, -job.priority))
    jobsSwaped = executeSingleSwap(jobsSorted)
    oldOrder = [job.index for job in jobsSorted]
    newOrder = [job.index for job in jobsSwaped]
    while computeScore(jobs, oldOrder) > computeScore(jobs, newOrder):
        jobsSorted = jobsSwaped
        jobsSwaped = executeSingleSwap(jobsSwaped)
        oldOrder = [job.index for job in jobsSorted]
        newOrder = [job.index for job in jobsSwaped]
    return Solution(computeScore(jobs, newOrder), newOrder)


def executeSingleSwap(jobs):
    jobsCopy = jobs.copy()
    machineTime1 = 0
    machineTime2 = 0
    machineTime3 = 0
    mainOrderList = []
    for i in range(len(jobsCopy) - 1):
        defaultOrderPenalty = computePenaltyForNextTwoJobs(jobsCopy[i], jobsCopy[i + 1], machineTime1, machineTime2, machineTime3)
        swapedOrderPenalty = computePenaltyForNextTwoJobs(jobsCopy[i + 1], jobsCopy[i], machineTime1, machineTime2, machineTime3)
        if defaultOrderPenalty > swapedOrderPenalty:
            chosenJob = jobsCopy[i + 1]
            jobsCopy[i], jobsCopy[i + 1] = jobsCopy[i + 1], jobsCopy[i]
        else:
            chosenJob = jobsCopy[i]
        machineTime1 += chosenJob.durationTime1
        machineTime2 = max(machineTime1, machineTime2) + chosenJob.durationTime2
        machineTime3 = max(machineTime2, machineTime3) + chosenJob.durationTime3
        mainOrderList.append(chosenJob)
        if i == len(jobsCopy) - 2:
            mainOrderList.append(jobsCopy[i + 1])
    return mainOrderList


if __name__ == '__main__':
    inFile = open(sys.argv[1], "r")
    filename = os.path.split(sys.argv[1])[-1]
    outFile = open(os.path.join(sys.argv[2], filename.replace('in', 'out')), "w+")
    jobs = getJobsFromFile(inFile)
    solution = algorithmMultipleSwaping(jobs)
    solution.saveToFile(outFile)
    inFile.close()
    outFile.close()
