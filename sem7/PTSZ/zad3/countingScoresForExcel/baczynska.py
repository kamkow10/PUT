import sys
import os


def machines_add_task(machines, task):
    for i in range(3):
        machines[i].add_task(machines, task)
    if machines[2].cur_time > task.d_time:
        return (machines[2].cur_time - task.d_time) * task.w
    else:
        return 0


class Solver:

    def __init__(self, tasks, machines=None):
        self.tasks = tasks
        self.machines = machines

        self.instance_size = len(tasks)
        self.cur_time = 0
        self.order = []
        self.result = 0

    def run(self):
        self.result = 0
        self.order = []
        self.late = []
        self.not_late = []

        # zainicjuj zawartość tablic late i not_late
        for task in self.tasks:
            if sum(task.p_times) >= task.d_time:
                self.late.append(task)
            else:
                self.not_late.append(task)

        while len(self.tasks) > len(self.order):

            if not self.late:
                sorted_by_d_time = sorted(self.not_late,
                                          key=lambda x: [x.d_time, sum(x.p_times)])
                self.order.append(sorted_by_d_time[0].task_id)
                self.result += machines_add_task(machines=self.machines, task=sorted_by_d_time[0])
                self.not_late.remove(sorted_by_d_time[0])

            elif len(self.late) == 1:
                self.order.append(self.late[0].task_id)
                self.result += machines_add_task(machines=self.machines, task=self.late[0])
                self.late = []

            else:

                # wybieramy z self.late
                sorted_by_cost = sorted(self.late,
                                        # koszt jaki placimy teraz za opoznienie. malejąco (-)
                                        key=lambda x: [-((self.find_finish_time(x) - x.d_time) * x.w), sum(
                                            x.p_times)])  # [211.2, 474.45, 516.7, 681.33, 1190.96, 1012.28, 1792.91, 1417.1, 1555.97, 1654.77]
                # finish time. rosnąco (+)
                # key = lambda x: [self.find_finish_time(x), sum(x.p_times)] )                            #[211.2, 474.45, 757.41, 1060.17, 1190.96, 1499.99, 1792.91, 2008.8, 2309.92, 2621.5]
                # po wadze. malejąco (-)
                # key = lambda x: [-x.w, sum(x.p_times)])                                                 #[211.2, 474.45, 511.43, 685.3, 1190.96, 994.71, 1792.91, 1380.81, 1543.72, 1671.93]

                task1 = sorted_by_cost[0]
                task2 = sorted_by_cost[1]

                if int(self.find_finish_time2(task1, task2)) > int(self.find_finish_time2(task2, task1)):
                    self.order.append(task2.task_id)
                    self.result += machines_add_task(machines=self.machines, task=task2)
                    self.late.remove(task2)
                else:
                    self.order.append(task1.task_id)
                    self.result += machines_add_task(machines=self.machines, task=task1)
                    self.late.remove(task1)

            # wybraliśmy jedno zadanie więc aktualizujemy tablice self.late i self.not_late
            for task in self.not_late:
                if self.find_finish_time(task) >= task.d_time:
                    self.late.append(task)
                    self.not_late.remove(task)

        self.result /= sum(task.w for task in self.tasks)
        self.result = round(self.result, 2)
        # print(self.result)

        return self.order

    def find_finish_time(self, task):
        finish_time = 0

        for i in range(3):
            machine = self.machines[i]

            finish_time = max(machine.cur_time, finish_time) + task.p_times[i]

        return finish_time

    def find_finish_time2(self, task1, task2):
        finish_time1 = 0
        finish_time2 = 0
        my_machines = []

        for i in range(3):
            my_machines.append(self.machines[i].cur_time)

        for i in range(3):
            finish_time1 = max(my_machines[i], finish_time1) + task1.p_times[i]
            my_machines[i] = finish_time1

        for i in range(3):
            finish_time2 = max((my_machines[i] + task1.p_times[i]), finish_time2) + task2.p_times[i]
            my_machines[i] = finish_time2

        return finish_time2

    def save_to_file(self, file_path):
        with open(file_path, "w") as file:
            result = f"{self.result}\n"
            result += " ".join([str(x) for x in self.order])
            file.write(result)


class Task:

    def __init__(self, *args):
        if len(args) > 4:
            task_id = int(args[0])
            input_ = " ".join([str(x) for x in args[1:] if x is not None])

            self.parse_input_for_task(task_id=task_id, input_str=input_)

    def parse_input_for_task(self, task_id, input_str):
        input_str = input_str.strip()
        params = input_str.split(" ")

        if len(params[-1]) < 1:
            params = params[:-1]
        if len(params) < 5:
            raise AttributeError("Not enough parameters")
        for idx, item in enumerate(params):
            params[idx] = int(item)
        self.task_id = task_id
        self.p_times = params[:3]
        self.d_time = params[-2]
        self.w = params[-1]


class Machine:

    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.cur_time = 0
        self.tasks = []

    def add_task(self, machines, task):

        self.tasks.append(task)

        if self.machine_id == 0:
            self.cur_time += task.p_times[0]
        else:
            self.cur_time = max(self.cur_time, machines[self.machine_id - 1].cur_time) + task.p_times[self.machine_id]


def read_file(input_str):
    lines = input_str.split("\n")
    number_of_tasks = int(lines[0])

    machines = []
    for idx in range(3):
        machines.append(Machine(machine_id=idx))

    tasks = []
    lines_with_tasks = lines[1:]
    for idx in range(1, number_of_tasks + 1):
        new_task = Task()
        new_task.parse_input_for_task(idx, lines_with_tasks[idx - 1])
        tasks.append(new_task)

    return tasks, machines


def run_algorithm():
    [path_to_file, output_dir] = sys.argv[-2:]

    if os.path.exists(path_to_file):
        with open(path_to_file, "r") as file:
            tasks, machines = read_file(file.read())

        filename = os.path.split(path_to_file)[-1]
        save_path = os.path.join(output_dir, filename.replace("in", "out"))

        solver = Solver(tasks=tasks, machines=machines)
        solver.run()
        solver.save_to_file(save_path)


if __name__ == '__main__':
    run_algorithm()
