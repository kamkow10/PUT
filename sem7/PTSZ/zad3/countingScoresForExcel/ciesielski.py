import sys
import os
import time


class Task:

    def __init__(self, *args):
        if len(args) >= 6:

            self.taskId = args[0]
            self.p1Time = args[1]
            self.p2Time = args[2]
            self.p3Time = args[3]
            self.dTime = args[4]
            self.w = args[5]

    def __str__(self, separator = " "):
        result = ""
        return result + f"{self.p1Time}{separator}{self.p2Time}{separator}{self.p3Time}{separator}{self.dTime}{separator}{self.w}"

def main(argv):
    print(f"Running alg for {argv[0]}.")
    tasks = GetTasks(argv[0])
    w, result = RunAlgorythm(tasks)
    WriteToFile(w, result, argv[1], argv[0])

def RunAlgorythm(tasks):
    currentTimes = [0,0,0]
    leftTasks = tasks.copy()
    scheduled = []
    _sum = 0
    while leftTasks:
        choosenTask, leftTasks = GetNextTask(leftTasks, currentTimes)
        scheduled.append(choosenTask)
        currentTimes[0] += choosenTask.p1Time
        currentTimes[1] = max(
            currentTimes[0], currentTimes[1]) + choosenTask.p2Time
        currentTimes[2] = max(
            currentTimes[1], currentTimes[2]) + choosenTask.p3Time
        _sum += max(0, currentTimes[2] - choosenTask.dTime) * choosenTask.w

    score = round(_sum / sum([task.w for task in scheduled]), 2)
    return score, scheduled


def calculatePenalty(task, currentTimes):
    t1 = currentTimes[0] + task.p1Time
    t2 = max(t1, currentTimes[1]) + task.p2Time
    t3 = max(t2, currentTimes[2]) + task.p3Time

    return max(0, t3 - task.dTime) * task.w


def GetNextTask(tasks, currentTimes):
    tasks = sorted(tasks, key=lambda x: (-calculatePenalty(x, currentTimes), x.dTime ))
    choosenTask = tasks[0]
    leftTasks = tasks[1:]
    
    return choosenTask, leftTasks
    
def GetTasks(instanceFilePath):
    f = open(instanceFilePath, "r")
    n = int(f.readline())
    tasks = []
    for idx in range(1, n + 1):
        taskLineList = f.readline().strip().split()
        newTask = Task(idx, int(taskLineList[0]), int(taskLineList[1]), int(taskLineList[2]), int(taskLineList[3]), int(taskLineList[4]))
        tasks.append(newTask)
    return tasks

def WriteToFile(w, taskOrder, outputDir, inputFile):
    testFile = f"{w}\n"
    size = 0
    print(len(taskOrder))
    for j in taskOrder:
        testFile = testFile + f"{j.taskId} "
        size = size+1
    testFile = testFile.strip()
    testFile = testFile
    output = os.path.join(outputDir, f"out_{inputFile.split('_')[1]}_{size}.txt")
    with open(output, "w") as file:
        file.write(testFile)
    print(f'file saved to {output}')

if __name__ == "__main__":
   main(sys.argv[1:])