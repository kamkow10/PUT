import random


def generateInstances():
    for instSize in range(50, 501, 50):
        generateInstance(instSize)


def generateInstance(size):
    file = open("KOWALCZYK/in_KOWALCZYK_%d.txt" % size, "w+")
    file.write("%d\n" % size)
    for i in range(1, size + 1):
        durationTime1 = random.randint(1, 10)
        durationTime2 = random.randint(1, 10)
        durationTime3 = random.randint(1, 10)
        deadline = durationTime1 + durationTime2 + durationTime3 + random.randint(0, size * 2)
        priority = random.randint(1, 10)
        file.write("%d %d %d %d %d" % (durationTime1, durationTime2, durationTime3, deadline, priority))
        if i is not size:
            file.write("\n")
    file.close()


if __name__ == '__main__':
    generateInstances()