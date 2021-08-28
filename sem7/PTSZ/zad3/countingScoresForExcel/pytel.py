import sys
import os


def get_input(path):
    with open(path, "r") as file:
        lines = file.readlines()
    tasks = []
    for i in lines:
        i = i.replace("\n", "")
        tasks.append(i.split(" "))
    for i in tasks:
        for j in range(len(i)):
            i[j] = int(i[j])
    if not tasks[-1]:
        tasks.remove(tasks[-1])
    return tasks


def order_value(task, t1, t2, t3):
    new_t1=t1+task[1]
    new_t2=max(t2, new_t1) + task[2]
    new_t3=max(new_t2,t3)+task[2]
    remaining_time=max(task[4]-new_t3, 0)
    value=max(0, new_t3 - task[4]) * task[5]
    return remaining_time,-value


def order():
    input_path = sys.argv[-2]
    output_path = sys.argv[-1]
    out_filename = os.path.basename(input_path).replace("in", "out")
    tasks = get_input(input_path)
    amount = tasks[0][0]
    tasks = tasks[1:]
    t1 = 0
    t2 = 0
    t3 = 0
    value=0
    weight=0
    for i in range(len(tasks)):
        tasks[i].insert(0, i + 1)
    result = []
    for i in range(amount):
        chosen = min(tasks, key=lambda x: order_value(x, t1, t2, t3))
        t1+=chosen[1]
        t2 = max(t2, t1) + chosen[2]
        t3 = max(t2, t3) + chosen[3]
        value += max(0, t3 - chosen[4]) * chosen[5]
        weight += chosen[5]
        result.append(chosen[0])
        tasks.remove(chosen)
    value/=weight
    value = round(value, 2)
    with open(os.path.join(output_path, out_filename), "w") as file:
        file.write(str(value) + "\n")
        line=""
        for i in result:
            line+=(str(i) + " ")
        line=line[:-1]
        file.write(line)


def fake_output():
    path_name = "outputs"
    if not os.path.isdir(path_name):
        os.mkdir(path_name)
    for n in range(50, 501, 50):
        with open(os.path.join(path_name, "out_" + "pytel" + "_" + str(n) + ".txt"), "w") as file:
            file.write("0\n")
            for i in range(1, n + 1):
                if i != n:
                    file.write(str(i) + " ")
                else:
                    file.write(str(i))
            file.write("\n")

if __name__ == '__main__':
    order()
