import os
import sys


class Task:
    def __init__(self, task_value):
        self.pj1 = int(task_value[0])
        self.pj2 = int(task_value[1])
        self.pj3 = int(task_value[2])
        self.dj = int(task_value[3])  # due end line
        self.wj = int(task_value[4])  # waga

    def __init__(self, no, task_value):
        self.no = int(no)  # nr
        self.pj1 = int(task_value[0])
        self.pj2 = int(task_value[1])
        self.pj3 = int(task_value[2])
        self.dj = int(task_value[3])  # due end line
        self.wj = int(task_value[4])  # waga

    def show(self):
        print(f"Show: {self.pj1} {self.pj2} {self.pj3} {self.dj} {self.wj}")

    def show_with_no(self):
        print(f"ShowNo: {self.no} - {self.pj1} {self.pj2} {self.pj3} {self.dj} {self.wj}")


class Engine:
    # f_mt1 function_machine_time
    # funkcja dla pojedynczego taska!!!
    def get_end_time_task(self, f_mt1, f_mt2, f_mt3, task: Task):
        f_mt1 += task.pj1

        if f_mt2 < f_mt1:
            f_mt2 = f_mt1
        f_mt2 += task.pj2

        if f_mt3 < f_mt2:
            f_mt3 = f_mt2
        f_mt3 += task.pj3
        return f_mt1, f_mt2, f_mt3, self.get_criterium(f_mt3, task)

    def get_criterium(self, f_mt3, task: Task):
        if task.dj < f_mt3:
            return (f_mt3 - task.dj) * task.wj
        return 0

    def resolve_problem(self, in_data_path):
        in_file = open(in_data_path)
        in_data = in_file.read()
        in_rows = in_data.split("\n")
        instance_size = int(in_rows[0])
        tasks = []

        for i, row in enumerate(in_rows[1:]):
            if row != "":
                tasks.append(Task(i + 1, row.split(" ")))

        sorted_tasks = list(sorted(tasks, key=lambda x: (x.dj, -x.wj)))

        # Machine Time
        mt1 = 0
        mt2 = 0
        mt3 = 0

        criteria_result = 0
        weight_result = 0
        result_list = []

        # TODO: Jeśli będzie dużo ludzi z lepszymi algo, to dodać porównanie ze wszytkimi, albo z większym zakresem w przód

        for i, current_task in enumerate(sorted_tasks):
            # czy istnieje next_task
            if i < instance_size - 2:
                task2 = sorted_tasks[i + 1]
                task3 = sorted_tasks[i + 2]
                # 1. Wyliczenie wartości dla wartości kryterium po wykonaniu permutacji dwóch tasków
                # 1.1: current, 2, 3
                c_mt1, c_mt2, c_mt3, c_crit = self.get_end_time_task(mt1, mt2, mt3, current_task)
                c_2_mt1, c_2_mt2, c_2_mt3, c_2_crit = self.get_end_time_task(c_mt1, c_mt2, c_mt3, task2)
                c_2_3_mt1, c_2_3_mt2, c_2_3_mt3, c_2_3_crit = self.get_end_time_task(c_2_mt1, c_2_mt2, c_2_mt3, task3)
                c23_result = c_crit + c_2_crit + c_2_3_crit
                # 1.2: current, 3, 2
                c_3_mt1, c_3_mt2, c_3_mt3, c_3_crit = self.get_end_time_task(c_mt1, c_mt2, c_mt3, task3)
                c_3_2_mt1, c_3_2_mt2, c_3_2_mt3, c_3_2_crit = self.get_end_time_task(c_3_mt1, c_3_mt2, c_3_mt3, task2)
                c32_result = c_crit + c_3_crit + c_3_2_crit
                # 1.3: 2, current, 3
                t2_mt1, t2_mt2, t2_mt3, t2_crit = self.get_end_time_task(mt1, mt2, mt3, task2)
                t2_c_mt1, t2_c_mt2, t2_c_mt3, t2_c_crit = self.get_end_time_task(t2_mt1, t2_mt2, t2_mt3, current_task)
                t2_c_3_mt1, t2_c_3_mt2, t2_c_3_mt3, t2_c_3_crit = self.get_end_time_task(t2_c_mt1, t2_c_mt2, t2_c_mt3, task3)
                t2c3_result = t2_crit + t2_c_crit + t2_c_3_crit
                # 1.4: 2, 3, current
                t2_3_mt1, t2_3_mt2, t2_3_mt3, t2_3_crit = self.get_end_time_task(t2_mt1, t2_mt2, t2_mt3, task3)
                t2_3_c_mt1, t2_3_c_mt2, t2_3_c_mt3, t2_3_c_crit = self.get_end_time_task(t2_3_mt1, t2_3_mt2, t2_3_mt3, current_task)
                t23c_result = t2_crit + t2_3_crit + t2_3_c_crit
                # 1.5: 3, current, 2
                t3_mt1, t3_mt2, t3_mt3, t3_crit = self.get_end_time_task(mt1, mt2, mt3, task3)
                t3_c_mt1, t3_c_mt2, t3_c_mt3, t3_c_crit = self.get_end_time_task(t3_mt1, t3_mt2, t3_mt3, current_task)
                t3_c_2_mt1, t3_c_2_mt2, t3_c_2_mt3, t3_c_2_crit = self.get_end_time_task(t3_c_mt1, t3_c_mt2, t3_c_mt3, task2)
                t3c2_result = t3_crit + t3_c_crit + t3_c_2_crit
                # 1.6: 3, 2, current
                t3_2_mt1, t3_2_mt2, t3_2_mt3, t3_2_crit = self.get_end_time_task(t3_mt1, t3_mt2, t3_mt3, task2)
                t2_3_c_mt1, t2_3_c_mt2, t2_3_c_mt3, t2_3_c_crit = self.get_end_time_task(t3_2_mt1, t3_2_mt2, t3_2_mt3, current_task)
                t32c_result = t3_crit + t3_2_crit + t2_3_c_crit

                # 2. Wybranie koleności dającej mniejszą wartość kryterium
                # 2.1. Jeśli puszczenie next_tesk jest lepsze przed current, to to robię
                tmp_lis = {c23_result, c32_result, t2c3_result, t23c_result, t3c2_result, t32c_result}
                winner_time = sorted(tmp_lis)[0]

                if winner_time == t2c3_result:
                    sorted_tasks[i] = task2
                    sorted_tasks[i+1] = current_task
                    sorted_tasks[i+2] = task3
                    current_task = task2

                elif winner_time == t23c_result:
                    sorted_tasks[i] = task2
                    sorted_tasks[i + 1] = task3
                    sorted_tasks[i + 2] = current_task
                    current_task = task2

                elif winner_time == t3c2_result:
                    sorted_tasks[i] = task3
                    sorted_tasks[i + 1] = current_task
                    sorted_tasks[i + 2] = task2
                    current_task = task3

                elif winner_time == t32c_result:
                    sorted_tasks[i] = task3
                    sorted_tasks[i + 1] = task2
                    sorted_tasks[i + 2] = current_task
                    current_task = task3

            # 3. Dodanie czasów do maszyn
            mt1, mt2, mt3, crit = self.get_end_time_task(mt1, mt2, mt3, current_task)
            criteria_result += crit
            weight_result += current_task.wj
            result_list.append(current_task.no)
            # print(f"APPEND: {current_task.no}")

        result = round(criteria_result/weight_result, 2)

        str_result_list = []
        for no in result_list:
            str_result_list.append(str(no))

        save_path = os.path.join(save_dir_path, os.path.split(path_file)[-1].replace("in", "out"))
        with open(save_path, 'w') as file:
            file.write(str(result) + "\n" + " ".join(str_result_list))
        return


if __name__ == '__main__':
    path_file = sys.argv[-2]
    save_dir_path = sys.argv[-1]
    engine = Engine()
    engine.resolve_problem(path_file)

