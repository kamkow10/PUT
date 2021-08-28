import os
import shutil
import random
import sys

DIRECTORY = "output"

def take4th(elem):
    return elem[3]


def readInputFile(fileName):
    file = open(fileName, "r", encoding='utf-8-sig')
    data = []
    for line in file:
        line = line.replace("\n", "")
        data.append([int(number) for number in line.split(" ")])
    instance = data[0][0]
    values = data[1:]
    if values[-1] == "":
        values = values[:-1]
    return instance, values


def sortData(instance, data):

    for i in range(instance):
        data[i].append(i + 1)

    sortedList = data.copy()
    sortedList.sort(key=take4th)

    for test in range(15):

        outputValues = []
        outputData = []
        time1 = 0
        time2 = 0
        time3 = 0
        taskEnds = []

        for task in sortedList:

            endingTime1 = time1 + task[0]
            endingTime2 = max(time2, endingTime1) + task[1]
            endingTime3 = max(time3, endingTime2) + task[2]

            if endingTime3 <= task[3] or len(outputValues) == 0:
                outputValues.append(task[5])
                outputData.append(task)
                taskEnds.append([time1, time2, time3])
                time1 = endingTime1
                time2 = endingTime2
                time3 = endingTime3

            else:
                cost1 = max(0, time3 - outputData[-1][3]) * outputData[-1][4] + max(0, endingTime3 - task[3]) * task[4]

                tmpTime1 = taskEnds[-1][0] + task[0]
                tmpTime2 = max(taskEnds[-1][1], tmpTime1) + task[1]
                tmpTime3 = max(taskEnds[-1][2], tmpTime2) + task[2]

                oldTmpTime1 = tmpTime1 + outputData[-1][0]
                oldTmpTime2 = max(tmpTime2, oldTmpTime1) + outputData[-1][1]
                oldTmpTime3 = max(tmpTime3, oldTmpTime2) + outputData[-1][2]

                cost2 = max(0, tmpTime3 - task[3]) * task[4] + max(0, oldTmpTime3 - outputData[-1][3]) * outputData[-1][4]

                if cost2 < cost1:
                    outputValues.pop()
                    prevData = outputData.pop()

                    outputValues.append(task[5])
                    outputData.append(task)

                    time1 = tmpTime1
                    time2 = tmpTime2
                    time3 = tmpTime3

                    taskEnds.append([time1, time2, time3])

                    outputValues.append(prevData[5])
                    outputData.append(prevData)

                    time1 = oldTmpTime1
                    time2 = oldTmpTime2
                    time3 = oldTmpTime3

                else:
                    outputValues.append(task[5])
                    outputData.append(task)

                    taskEnds.append([time1, time2, time3])

                    time1 += task[0]
                    time2 = max(time1, time2) + task[1]
                    time3 = max(time2, time3) + task[2]

        sortedList = outputData

    time1 = 0
    time2 = 0
    time3 = 0
    points = 0
    weight = 0

    tmp = 0#

    for i in outputValues:
        tmp += 1
        time1 += data[i - 1][0]
        time2 = max(time1, time2) + data[i - 1][1]
        time3 = max(time2, time3) + data[i - 1][2]
        points += max(0, (time3 - data[i - 1][3]) * data[i - 1][4])
        weight += data[i - 1][4]

    return round(points / weight, 2), outputValues

def saveOutputFile(fileName, points, sortedData):
    file = open(fileName, "w+")
    file.write(str(points) + "\n")
    output = ''
    for task in sortedData:
        output += str(task) + " "
    output = output[:-1]
    file.write(output)
    file.close()
    

def main():
    if len(sys.argv) != 3:
        print("Usage details: FRAS.py <input_file> <output_directory>")
        if len(sys.argv) > 3:
            print("Too many arguments!")
    else:
        instance, data = readInputFile(sys.argv[1])
        points, outputValues = sortData(instance, data)
        outputFileName = os.path.join(sys.argv[2], os.path.split(sys.argv[1])[-1].replace("in", "out"))
        saveOutputFile(outputFileName, points, outputValues)

if __name__ == "__main__":
    main()