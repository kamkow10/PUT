import os
import sys


def calc_crit_simple(tasks):
    cur_time = [0, 0, 0]
    weight_sum = 0
    criterion = 0
    for task in tasks:
        for i in range(len(cur_time)):
            if i > 0:
                cur_time[i] = max(cur_time[i], cur_time[i - 1])
            cur_time[i] += task[i]
        criterion += task[4] * max(0, cur_time[2] - task[3])
        weight_sum += task[4]
    result = criterion / weight_sum if weight_sum else 0
    return round(result, 2)


def calc_crit(in_file_path, tasks):
    in_size, in_tasks = read_input_file(in_file_path)
    cur_time = [0, 0, 0]
    weight_sum = 0
    criterion = 0
    for task in tasks:
        for i in range(len(cur_time)):
            if i > 0:
                cur_time[i] = max(cur_time[i], cur_time[i - 1])
            cur_time[i] += in_tasks[int(task) - 1][i]
        criterion += in_tasks[int(task) - 1][4] * max(0, cur_time[2] - in_tasks[int(task) - 1][3])
        weight_sum += in_tasks[int(task) - 1][4]
    result = criterion / weight_sum if weight_sum else 0
    return round(result, 2)


def write_to_file_instance(direction, tasks, n, calc, lastname, path):
    dir_path = path
    with open(os.path.join(dir_path, f"{direction}_{lastname}_{n}.txt"), "w") as file:
        file.write("%s\n" % calc)
        for task in tasks:
            task = str(task)
            task = task.replace('[', '')
            task = task.replace(']', '')
            task = task.replace(',', '')
            file.write("%s " % task)
    return


def read_input_file(path):
    final_tasks = []
    file_in = open(path, "r")
    content_in = file_in.readlines()
    content_in = [x.strip() for x in content_in]
    content_in = [x.split(' ') for x in content_in]
    tasks = content_in
    crit = tasks.pop(0)
    for task in tasks:
        ints = [int(x) for x in task]
        final_tasks.append(ints)
    size = int(crit[0])
    return size, final_tasks


def simple_scheduling(tasks):
    s_tasks = tasks.copy()
    s_tasks.sort(key=lambda x: x[3]/x[4] + (x[0]+x[1]+x[2]))
    return s_tasks


def choose_task(tasks, cur_times):
    chosen = tasks[0]
    before_check = sys.maxsize
    for task in tasks:
        temp1 = cur_times[0] + task[0]
        temp2 = max(temp1, cur_times[1]) + task[1]
        temp3 = max(temp2, cur_times[2]) + task[2]
        crit = max(0, temp3 - task[3]) * task[4]
        check = task[4] / (crit + 1) * ((task[0] + task[1] + task[2]) / (task[3] * task[4] + 1))
        if check < before_check:
            before_check = check
            chosen = task
    tasks.remove(chosen)
    return chosen


def update_cur_timing(cur_time, chosen):
    cur_time[0] += chosen[0]
    cur_time[1] = max(cur_time[0], cur_time[1]) + chosen[1]
    cur_time[2] = max(cur_time[1], cur_time[2]) + chosen[2]
    return cur_time


def scheduling(tasks):
    tasks = simple_scheduling(tasks)
    task_to_schedule = tasks.copy()
    cur_time = [0, 0, 0]
    scheduled = []
    while len(task_to_schedule) > 0:
        tasks = simple_scheduling(tasks)
        chosen = choose_task(task_to_schedule, cur_time)
        cur_time = update_cur_timing(cur_time, chosen)
        scheduled.append(chosen)
    return scheduled


def prepare(lastname, size, path_in, path_out):
    scheduled_ind = []
    size, tasks = read_input_file(path_in)
    indexes = dict(i for i in enumerate(tasks))

    sort_tasks = simple_scheduling(tasks)
    before_crit = calc_crit_simple(sort_tasks)
    scheduled = scheduling(tasks)
    after_crit = calc_crit_simple(scheduled)

    if before_crit < after_crit:
        scheduled = sort_tasks.copy()
    for i in range(len(scheduled)):
        for m in indexes:
            if indexes[m] == scheduled[i]:
                scheduled_ind.append(m + 1)
                indexes.pop(m)
                break
    crit = calc_crit(path_in, scheduled_ind)
    write_to_file_instance('out', scheduled_ind, size, crit, lastname, path_out)


if __name__ == '__main__':
    in_path_file = sys.argv[1]
    out_path_directory = sys.argv[2]
    path = in_path_file.split('_')
    lastname = path[1]
    instance_size = path[2].split('.')
    instance_size = instance_size[0]
    if os.path.exists(in_path_file):
        prepare(lastname, instance_size, in_path_file, out_path_directory)
