import sys
import os
import itertools
import math

class Scheduler:

    def __init__(self, file_path, save_path):
        self.used = []
        self.current_time = [0, 0, 0]
        self.dw_sum = 0
        self.w_sum = 0
        self.d_calculated = 0
        self.file_path = file_path
        self.save_path = save_path
        self.iterator = None
        self.data = []
        self.data_sorted = []

    def convert_data(self, raw_data):
        for i in range(1, self.iterator+1):
            task = raw_data[i].split()
            task = [int(x) for x in task]
            p1 = int(task[0])
            p2 = int(task[1])
            p3 = int(task[2])
            d = int(task[3])
            w = int(task[4])
            temp = []
            temp.append(p1)
            temp.append(p2)
            temp.append(p3)
            temp.append(d)
            temp.append(w)

            self.data.append(temp)

    def read_data(self):
        in_file = open(self.file_path, 'r')
        raw_data = in_file.read().splitlines()
        self.iterator = int(raw_data[0])
        self.convert_data(raw_data)

    def save_to_file(self):
        filename = os.path.split(self.file_path)[-1]
        output = os.path.join(self.save_path, filename.replace("in", "out"))
        file = open(output, "w+")
        file.write(str(round(self.d_calculated,2)) + "\n" + " "
            .join([str(x+1) for x in self.used])) 

    def maxD(self, time):
        if time > 0:
            return time
        else:
            return 0

    def calc_result(self):
        for i in range(self.iterator):
            p1 = self.data_sorted[i][1]
            p2 = self.data_sorted[i][2]
            p3 = self.data_sorted[i][3]
            d = self.data_sorted[i][4]
            w = self.data_sorted[i][5]
            self.current_time[0] += p1
            if i == 0:
                self.current_time[1] = self.current_time[0] + p2
                self.current_time[2] = self.current_time[1] + p3
            else:
                if self.current_time[0] > self.current_time[1]:
                    self.current_time[1] = self.current_time[0] + p2
                else:
                    self.current_time[1] += p2
                if self.current_time[1] > self.current_time[2]:
                    self.current_time[2] = self.current_time[1] + p3
                else:
                    self.current_time[2] += p3
            self.used.append(self.data_sorted[i][0])
            self.dw_sum += self.maxD(self.current_time[2]-d) * w
            self.w_sum += w
            
        self.d_calculated = self.dw_sum/self.w_sum   

    def solve(self):
        self.read_data()
        task_indices = []
        for i in range(self.iterator):
            task_indices.append([i])

        self.data = list(map(list.__add__, task_indices, self.data))
        #print(self.data)
        self.data_sorted = sorted(self.data, key=lambda task: (task[1] + task[2] + task[3] + task[4]))
        self.calc_result()
        #print(self.used)
        self.save_to_file()

def main(file_path, save_path):
    scheduler = Scheduler(file_path, save_path)
    scheduler.solve()

if __name__=="__main__":
    if len(sys.argv) < 3:
        raise("Script requires 2 arguments!")
    main(sys.argv[1],sys.argv[2])