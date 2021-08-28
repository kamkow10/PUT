import random


def generateInstances():
    for instSize in range(50, 501, 50):
        generateInstance(instSize)


def generateInstance(size):
    file = open("output/in_KOWALCZYK_%d.txt" % size, "w+")
    file.write("%d\n" % size)
    for i in range(1, size + 1):
        durationTime = random.randint(10, 50)
        readyTime = i + random.randint(1, 20)
        endTime = readyTime + durationTime + random.randint(0, 10)
        priority = random.randint(1, 10)
        file.write("%d %d %d %d" % (durationTime, readyTime, endTime, priority))
        if i is not size:
            file.write("\n")
    file.close()


if __name__ == '__main__':
    generateInstances()
