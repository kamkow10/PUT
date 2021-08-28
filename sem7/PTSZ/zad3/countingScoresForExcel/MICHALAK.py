import os
import sys
import itertools


def serialize(input_file, output_directory):
    file = open(input_file, "r")
    data = file.read().split('\n')
    file.close()

    n = data.pop(0)
    if data[-1] == '':
        data.pop()

    data_int = []
    for i, task in enumerate(data):
        data_int.append([int(x) for x in task.split(' ')])
        data_int[-1].append(i+1)

    suma_w = 0
    for task in data_int:
        suma_w += task[4]

    data_int.sort(key=sortByDueDate)
    order = []
    lost = 0
    times = [0 for _ in range(3)]

    counter = 0

    helper = []
    while len(data_int) > 0:
        helper.append(data_int.pop(0))
        if len(helper) < 3:
            continue
        if len(helper) == 3:
            # do some stuff
            min_value = calcTasksLost(times, helper)
            for tasks in list(itertools.permutations(helper)):
                tasks = list(tasks)
                current = calcTasksLost(times, tasks)
                if current < min_value:
                    min_value = current
                    helper = tasks
            poped = helper.pop(0)
            lost_tmp = addTask(times, poped)
            if lost_tmp > 0:
                counter += 1
            lost += lost_tmp

            order.append(poped[5])
        if len(helper) == 2 and len(data_int) == 0:
            # last two elements
            min_value = calcTasksLost(times, helper)
            for tasks in list(itertools.permutations(helper)):
                tasks = list(tasks)
                current = calcTasksLost(times, tasks)
                if current < min_value:
                    min_value = current
                    helper = tasks
            poped = helper.pop(0)
            lost += addTask(times, poped)
            order.append(poped[5])

            poped = helper.pop(0)
            lost += addTask(times, poped)
            order.append(poped[5])

    result = [str(round(lost/suma_w, 2)) + '\n', '']
    for task in order:
        result[1] += f"{task} "
    result[1] = result[1][:-1] + '\n'

    output_file = os.path.split(input_file)[-1].replace('in', 'out')
    file_name = os.path.join(output_directory, output_file)
    f = open(file_name, "w")
    f.writelines(result)
    f.close()


def sortByDueDate(elem):
    return elem[3]


def calcTasksLost(times_array, tasks):
    time_0 = times_array[0]
    time_1 = times_array[1]
    time_2 = times_array[2]

    lost = 0
    for task in tasks:
        time_0 += task[0]
        time_1 = max(time_0, time_1) + task[1]
        time_2 = max(time_1, time_2) + task[2]
        lost += task[4] * max(0, time_2 - task[3])
    return lost


def addTask(times_array, task):
    times_array[0] += task[0]
    times_array[1] = max(times_array[0], times_array[1]) + task[1]
    times_array[2] = max(times_array[1], times_array[2]) + task[2]
    return task[4] * max(0, times_array[2] - task[3])


def sortByWP(elem):
    return elem[3] / elem[0]


def calc_lost(input_file, order):
    f = open(input_file, "r")
    tasks = f.read().split('\n')
    f.close()
    n = tasks.pop(0)
    if tasks[-1] == '':
        tasks.pop()

    lost = 0
    time = 0
    for taskId in order:
        current_task = [int(x) for x in tasks[taskId - 1].split(' ')]
        if time < current_task[1]:
            time = current_task[1]
        end_time = time + current_task[0]
        if end_time > current_task[2]:
            lost += current_task[3]
        time = end_time
    return n, lost, True


in_file = sys.argv[1]
out_dir = sys.argv[2]
# in_file = 'data/in_MICHALAK_500.txt'
# out_dir = 'data'
serialize(in_file, out_dir)
