import random


def generateInstances():
    for instSize in range(50, 501, 50):
        generateInstance(instSize)


def generateInstance(size):
    file = open("output/in_KOWALCZYK_%d.txt" % size, "w+")
    file.write("%d\n" % size)
    machines = getMachines()
    file.write("%.2f %.2f %.2f %.2f %.2f\n" % (machines[0], machines[1], machines[2], machines[3], machines[4]))
    for i in range(1, size + 1):
        durationTime = random.randint(1, 10)
        readyTime = random.randint(1, size * 2)
        file.write("%d %d" % (durationTime, readyTime))
        if i is not size:
            file.write("\n")
    file.close()


def getMachines():
    neededSum = 10
    machine1 = 1
    machine2 = random.uniform(1, neededSum - 4)
    machine3 = random.uniform(1, neededSum - 4 - (machine2 - 1))
    machine4 = random.uniform(1, neededSum - 4 - ((machine2 - 1) + (machine3 - 1)))
    machine5 = random.uniform(1, neededSum - 4 - ((machine2 - 1) + (machine3 - 1) + (machine4 - 1)))
    return [machine1, machine2, machine3, machine4, machine5]


if __name__ == '__main__':
    generateInstances()
