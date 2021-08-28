import sys
import os


class Job:
    index = None
    durationTime = None
    readyTime = None
    endTime = None
    priority = None

    def __init__(self, imdex, params):
        self.index = imdex
        self.durationTime = params[0]
        self.readyTime = params[1]
        self.endTime = params[2]
        self.priority = params[3]


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
        for jobId in self.orderList:
            listAsString += jobId.__str__() + ' '
        return listAsString


def getJobsFromFile(file):
    jobsList = []
    index = -1
    for line in file.readlines():
        index += 1
        params = [int(param) for param in line.split()]
        if len(params) is 1:
            continue
        jobsList.append(Job(index, params))
    return jobsList


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


def solve(jobs):
    orderList = runAlgorithmLowPriorityJobsToEnd(jobs)
    score = computeScore(jobs, orderList)
    return Solution(score, orderList)


def runAlgorithmLowPriorityJobsToEnd(jobs):
    jobsByReadyTime = sorted(jobs, key=lambda job: job.readyTime)
    newJobs = moveLowPriorityJobsToEnd(jobsByReadyTime)
    return [job.index for job in newJobs]


def moveLowPriorityJobsToEnd(jobs):
    # v v v X v v
    time = 0
    doneJobs = []
    behindJobs = []
    for job in jobs:
        if time + job.durationTime > job.endTime:
            if checkIfSwapIsWorth(job, doneJobs[-1], time):
                time -= doneJobs[-1].durationTime
                behindJobs.append(doneJobs[-1])
                doneJobs.pop()
                doneJobs.append(job)
                time += job.durationTime
            else:
                behindJobs.append(job)
        else:
            doneJobs.append(job)
            if time < job.readyTime:
                time = job.readyTime
            time += job.durationTime
    return doneJobs + behindJobs


def checkIfSwapIsWorth(currentJob, beforeJob, time):
    timeBefore = time - beforeJob.durationTime
    return (timeBefore + currentJob.durationTime <= currentJob.endTime) and (currentJob.priority > beforeJob.priority)


if __name__ == '__main__':
    inFile = open(sys.argv[1], "r")
    filename = os.path.split(sys.argv[1])[-1]
    outFile = open(os.path.join(sys.argv[2], filename.replace('in', 'out')), "w+")
    jobs = getJobsFromFile(inFile)
    solution = solve(jobs)
    solution.saveToFile(outFile)
    inFile.close()
    outFile.close()
