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
        file.write("%d\n" % self.score)
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


def computeScoreForInitialOrder(jobs, machines):
    machineJobsListSize = len(jobs) / 5
    initialOrder = [
        [i for i in range(1, int(machineJobsListSize + 1))],
        [i for i in range(int(machineJobsListSize) + 1, int(machineJobsListSize * 2 + 1))],
        [i for i in range(int(machineJobsListSize * 2) + 1, int(machineJobsListSize * 3 + 1))],
        [i for i in range(int(machineJobsListSize * 3) + 1, int(machineJobsListSize * 4 + 1))],
        [i for i in range(int(machineJobsListSize * 4) + 1, int(machineJobsListSize * 5 + 1))]
    ]
    return computeScore(jobs, machines, initialOrder)


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
    results = []

    score = computeScoreForInitialOrder(jobs, machines)
    results.append(['Initial', score])

    orderList = shortToFastAlgorithm(jobs, machines)
    score = computeScore(jobs, machines, orderList)
    results.append(['Short to fast', score])

    orderList = longToFastAlgorithm(jobs, machines)
    score = computeScore(jobs, machines, orderList)
    results.append(['Long to fast', score])

    orderList = asapAlgorithm(jobs, machines)
    score = computeScore(jobs, machines, orderList)
    results.append(['ASAP', score])

    printResults(results)

    return Solution(0, [[1], [2], [3], [4], [5]])


def solveForDirectory(directory):
    results = [
        ['Initial', 0],
        ['Short to fast', 0],
        ['Long to fast', 0],
        ['ASAP', 0]
    ]
    for filename in os.listdir(directory):
        inFile = open(directory + filename, 'r')
        jobs, machines = getJobsAndMachinesFromFile(inFile)

        score = computeScoreForInitialOrder(jobs, machines)
        results[0][1] += score

        orderList = shortToFastAlgorithm(jobs, machines)
        score = computeScore(jobs, machines, orderList)
        results[1][1] += score

        orderList = longToFastAlgorithm(jobs, machines)
        score = computeScore(jobs, machines, orderList)
        results[2][1] += score

        orderList = asapAlgorithm(jobs, machines)
        score = computeScore(jobs, machines, orderList)
        results[3][1] += score

    printResults(results)


def printResults(results):
    print("{:<15} {:>20}".format('Algorithm', 'Score'))
    print("{:<15} {:>20}".format('===============', '===================='))
    for result in results:
        print("{:<15} {:>20.2f}".format(result[0], result[1]))


def shortToFastAlgorithm(jobs, machines):
    jobsByReadyTime = [job for job in sorted(jobs, key=lambda job: job.readyTime)]
    orderList = [[], [], [], [], []]
    for jobId in range(0, len(jobs), 5):
        topFiveJobs = sorted(jobsByReadyTime[jobId:jobId + 5], key=lambda job: job.durationTime)
        for topJobId in range(0, len(topFiveJobs)):
            orderList[machines.index(sorted(machines)[topJobId])].append(topFiveJobs[topJobId].index)
    return orderList


def longToFastAlgorithm(jobs, machines):
    jobsByReadyTime = [job for job in sorted(jobs, key=lambda job: job.readyTime)]
    orderList = [[], [], [], [], []]
    for jobId in range(0, len(jobs), 5):
        topFiveJobs = sorted(jobsByReadyTime[jobId:jobId + 5], key=lambda job: job.durationTime)
        for topJobId in range(0, len(topFiveJobs)):
            orderList[machines.index(sorted(machines, reverse=True)[topJobId])].append(topFiveJobs[topJobId].index)
    return orderList


def asapAlgorithm(jobs, machines):
    jobsByReadyTime = [job for job in sorted(jobs, key=lambda job: job.readyTime)]
    orderList = [[], [], [], [], []]
    for i in range(0, len(machines)):
        time = 0.0
        machine = sorted(machines)[i]
        machineIndex = machines.index(machine)
        copyJobs = jobsByReadyTime
        if machineIndex == 4:
            for job in copyJobs:
                orderList[machineIndex].append(job.index)
        else:
            for job in copyJobs:
                if job.readyTime < time:
                    continue
                else:
                    time = job.readyTime + (job.durationTime * machine)
                    orderList[machineIndex].append(job.index)
                    jobsByReadyTime.pop(jobsByReadyTime.index(job))
    return orderList


if __name__ == '__main__':
    solveForDirectory(sys.argv[1])

    # inFile = open(sys.argv[1], "r")
    # filename = os.path.split(sys.argv[1])[-1]
    # outFile = open(os.path.join(sys.argv[2], filename.replace('in', 'out')), "w+")
    # jobs, machines = getJobsAndMachinesFromFile(inFile)
    # solution = solve(jobs, machines)
    # solution.saveToFile(outFile)
    # inFile.close()
    # outFile.close()
