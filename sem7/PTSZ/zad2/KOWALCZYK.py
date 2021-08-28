import sys
import os


class Job:
    index = None
    durationTime = None
    readyTime = None

    def __init__(self, index, params):
        self.index = index
        self.durationTime = params[0]
        self.readyTime = params[1]


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
        for machineId in range(0, 5):
            for jobId in self.orderList[machineId]:
                listAsString += jobId.__str__() + ' '
            listAsString += '\n'
        return listAsString


def getJobsAndMachinesFromFile(file):
    jobsList = []
    machinesList = []
    lineNr = 1
    jobIndex = 0
    for line in file.readlines():
        if lineNr == 2:
            machinesList = [float(param) for param in line.split()]
        if lineNr > 2:
            jobIndex += 1
            params = [int(param) for param in line.split()]
            jobsList.append(Job(jobIndex, params))
            continue
        lineNr += 1
    return jobsList, machinesList


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
    return score / len(jobs)


def solve(jobs, machines):
    orderList = longToFastAlgorithm(jobs, machines)
    score = computeScore(jobs, machines, orderList)
    return Solution(score, orderList)


def longToFastAlgorithm(jobs, machines):
    jobsByReadyTime = [job for job in sorted(jobs, key=lambda job: job.readyTime)]
    orderList = [[], [], [], [], []]
    for jobId in range(0, len(jobs), 5):
        topFiveJobs = sorted(jobsByReadyTime[jobId:jobId + 5], key=lambda job: job.durationTime)
        for topJobId in range(0, len(topFiveJobs)):
            orderList[machines.index(sorted(machines, reverse=True)[topJobId])].append(topFiveJobs[topJobId].index)
    return orderList


if __name__ == '__main__':
    inFile = open(sys.argv[1], "r")
    filename = os.path.split(sys.argv[1])[-1]
    outFile = open(os.path.join(sys.argv[2], filename.replace('in', 'out')), "w+")
    jobs, machines = getJobsAndMachinesFromFile(inFile)
    solution = solve(jobs, machines)
    solution.saveToFile(outFile)
    inFile.close()
    outFile.close()
