import sys
import os


class Task:
    def __init__(self, idx, p1, p2, p3, d, w):
        self.idx = idx
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.d = d
        self.w = w

    def __repr__(self):
        return f"{self.p1} {self.p2} {self.p3} {self.d} {self.w}"


def read_tasks(input_file):
    tasks = []

    with open(input_file, "r") as f:
        no_tasks = int(f.readline())

        for index, line in enumerate(f):
            line = line.strip()
            parameters = line.split(' ')
            parameters = list(map(int, parameters))
            p1, p2, p3, d, w = parameters
            tasks.append(Task(index + 1, p1, p2, p3, d, w))
    return tasks


def get_next_task(tasks, times):
    # tasks.sort(key=lambda t: t.d/t.w)
    next_task = tasks[0]
    tmp_factor = sys.maxsize

    for task in tasks:
        # hypothetically add task and check the punishment
        t1 = times[0] + task.p1
        t2 = max(t1, times[1]) + task.p2
        t3 = max(t2, times[2]) + task.p3

        D = max(0, t3 - task.d) * task.w
        p = task.p1 + task.p2 + task.p3
        factor = 1/(D + 1) * (p/(task.d * task.w))

        if factor < tmp_factor:
            tmp_factor = factor
            next_task = task
            

    tasks.remove(next_task)
    return next_task


def write_to_file(input_file, output_folder, score, scheduled_sequence):
    output_file = os.path.basename(
        os.path.normpath(input_file)).replace('in', 'out')
    output_path = os.path.join(output_folder, output_file)
    with open(output_path, 'w') as f:
        output = f"{score}\n"
        output = output + scheduled_sequence
        f.write(output)


def schedule(input_file, output_folder):
    tasks = read_tasks(input_file)

    remaining_tasks = tasks.copy()
    machine_times = [0, 0, 0]
    scheduled = []

    sum_ = 0
    while len(remaining_tasks) > 0:
        next_task = get_next_task(remaining_tasks, machine_times)
        machine_times[0] += next_task.p1
        machine_times[1] = max(
            machine_times[0], machine_times[1]) + next_task.p2
        machine_times[2] = max(
            machine_times[1], machine_times[2]) + next_task.p3
        scheduled.append(next_task)

        sum_ += max(0, machine_times[2] - next_task.d) * next_task.w

    score = round(sum_ / sum([task.w for task in scheduled]), 2)
    scheduled_sequence = " ".join([str(task.idx) for task in scheduled])
    write_to_file(input_file, output_folder, score, scheduled_sequence)


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_folder = sys.argv[2]

    schedule(input_file, output_folder)
