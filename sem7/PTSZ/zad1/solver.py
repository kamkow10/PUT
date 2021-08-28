import sys


class Job:
    index = None
    durationTime = None
    readyTime = None
    endTime = None
    priority = None

    def __init__(self, index, params):
        self.index = index
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
    orderList = defaultAlgorithm(jobs)
    score = computeScore(jobs, orderList)
    print("defualt: %d" % score)

    orderList = sortingAlgorithm(jobs)
    score = computeScore(jobs, orderList)
    print("sorting: %d" % score)

    orderList = behindJobsToEndAlgorithm(jobs)
    score = computeScore(jobs, orderList)
    print("behind to end: %d" % score)

    orderList = behindJobsToEndWithNewSortingAlgorithm(jobs)
    score = computeScore(jobs, orderList)
    print("behind to end with new sorting: %d" % score)

    orderList = lowPriorityJobsToEndAlgorithm(jobs)
    score = computeScore(jobs, orderList)
    print("low priority to end: %d" % score)

    orderList = lowPriorityJobsToEndWithNewSortingAlgorithm(jobs)
    score = computeScore(jobs, orderList)
    print("low priority to end with new sorting: %d" % score)

    orderList = sortBySumAlgorithm(jobs)
    score = computeScore(jobs, orderList)
    print("sorted by sum: %d" % score)

    orderList = avoidingAlgorithm(jobs)
    score = computeScore(jobs, orderList)
    print("avoiding: %d" % score)

    orderList = avoidingAlgorithmWithNewSorting(jobs)
    score = computeScore(jobs, orderList)
    print("avoiding with new sorting: %d" % score)

    return Solution(score, orderList)


def defaultAlgorithm(jobs):
    return [x for x in range(1, len(jobs) + 1)]


def sortingAlgorithm(jobs):
    orderByReadyTime = [job.index for job in sorted(jobs, key=lambda job: job.readyTime)]
    return orderByReadyTime


def behindJobsToEndAlgorithm(jobs):
    jobsByReadyTime = sorted(jobs, key=lambda job: job.readyTime)
    newJobs = moveBehindJobsToEnd(jobsByReadyTime)
    return [job.index for job in newJobs]


def behindJobsToEndWithNewSortingAlgorithm(jobs):
    jobsByEndTimeMinusDuration = sorted(jobs, key=lambda job: job.endTime - job.durationTime)
    newJobs = moveBehindJobsToEnd(jobsByEndTimeMinusDuration)
    return [job.index for job in newJobs]


def lowPriorityJobsToEndAlgorithm(jobs):
    jobsByReadyTime = sorted(jobs, key=lambda job: job.readyTime)
    newJobs = moveLowPriorityJobsToEnd(jobsByReadyTime)
    return [job.index for job in newJobs]


def lowPriorityJobsToEndWithNewSortingAlgorithm(jobs):
    jobsByEndTimeMinusDuration = sorted(jobs, key=lambda job: job.endTime - job.durationTime)
    newJobs = moveLowPriorityJobsToEnd(jobsByEndTimeMinusDuration)
    return [job.index for job in newJobs]


def avoidingAlgorithm(jobs):
    jobsByReadyTime = sorted(jobs, key=lambda job: job.readyTime)
    newJobs = doAvoiding(jobsByReadyTime)
    return [job.index for job in newJobs]


def avoidingAlgorithmWithNewSorting(jobs):
    jobsByEndTimeMinusDuration = sorted(jobs, key=lambda job:job.readyTime + job.endTime - job.durationTime)
    newJobs = doAvoiding(jobsByEndTimeMinusDuration)
    return [job.index for job in newJobs]


def doAvoiding(jobs):
    time = 0
    doneJobs = []
    behindJobs = []
    for job in jobs:
        if not len(jobs) == (jobs.index(job) + 1):
            nextJob = jobs[jobs.index(job) + 1]
            if isSwapWorth(job, nextJob, time):
                behindJobs.append(job)
            else:
                time = max(time, job.readyTime) + job.durationTime
                doneJobs.append(job)
        else:
            doneJobs.append(job)
    return doneJobs + behindJobs # 117


def isSwapWorth(job, nextJob, time):
    return (max(time, job.readyTime) + job.durationTime > nextJob.endTime - nextJob.durationTime) and (
            job.priority < nextJob.priority) and (job.durationTime > nextJob.durationTime)


def sortBySumAlgorithm(jobs):
    return [job.index for job in sorted(jobs, key=lambda job: job.readyTime + job.endTime + job.durationTime)]


def moveBehindJobsToEnd(jobs):
    time = 0
    doneJobs = []
    behindJobs = []
    for job in jobs:
        if time + job.durationTime > job.endTime:
            behindJobs.append(job)
        else:
            doneJobs.append(job)
            if time < job.readyTime:
                time = job.readyTime
            time += job.durationTime
    return doneJobs + behindJobs


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
    outFile = open(sys.argv[2] + 'out_' + sys.argv[1].split('/')[-1][3:], "w+")
    jobs = getJobsFromFile(inFile)
    solution = solve(jobs)
    solution.saveToFile(outFile)
    inFile.close()
    outFile.close()
