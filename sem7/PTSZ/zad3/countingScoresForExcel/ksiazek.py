import numpy as np
import sys
import os


class Algorithm:
    def __init__(self, inputPath):
        self.jobs_list = self.readfile(inputPath)
        self.machines = [0, 0, 0]

    def readfile(self, inputPath):
        #make list of lists with tasks [p1, p2, p3, duedate, weight, index, 0 for calculate delay]
        array = []
        with open(inputPath, 'r') as file:
            self.N = int(file.readline())
            for i in range(0, self.N):
                one = file.readline().split() + [i + 1] + [0]
                array.append(one)
        jobs = np.array(array).astype(int)
        jobs = jobs.tolist()
        #print(jobs)
        return jobs

    def sortjobs(self):
        self.jobs_list = sorted(self.jobs_list, key=lambda x: x[2])
        #self.jobs_list = np.asarray(self.jobs_list)
        #print(self.jobs_list)
        return self.jobs_list


    def select_next_task(self, machines, tasks):
        first_task = tasks[0]
        #print("first" + str(first_task))
        t1 = machines[0] + first_task[0]
        t2 = max(machines[0], machines[1]) + first_task[1]
        t3 = max(machines[1], machines[2]) + first_task[2]
        current_best = (t3 - first_task[3]) * first_task[4]
        selected = first_task
        for task in tasks:
            t1, t2, t3 = 0, 0, 0
            t1 = machines[0] + task[0]
            t2 = max(machines[0], machines[1]) + task[1]
            t3 = max(machines[1], machines[2]) + task[2]
            if (t3 - task[3]) * task[4] >= current_best:
                current_best = (t3 - task[3]) * task[4]
                selected = task
        return selected
    '''def select_next_task(self, machines, tasks):
        first_task = tasks[0]
        #print("first" + str(first_task))
        t1 = machines[0] + first_task[0]
        t2 = max(machines[0], machines[1]) + first_task[1]
        t3 = max(machines[1], machines[2]) + first_task[2]
        current_best = (0.75*((first_task[0]+first_task[1]+first_task[2])/first_task[4]) + 0.25 * t3)/2 #* first_task[4]
        selected = first_task
        for task in tasks:
            t1, t2, t3 = 0, 0, 0
            t1 = machines[0] + task[0]
            t2 = max(machines[0], machines[1]) + task[1]
            t3 = max(machines[1], machines[2]) + task[2]
            if (0.75 * ((task[0]+task[1]+task[2])/task[4]) + 0.25*t3)/2 <= current_best:
                current_best = (0.75 * ((task[0]+task[1]+task[2])/task[4]) + 0.25 * t3)/2 #* task[4]
                selected = task
        return selected'''
    def scheduling(self):
        tasks = self.sortjobs() #sorted by due date
        scheduled = []
        delay = 0
        weight_sum = 0
        while len(tasks) > 0:
            next_task = self.select_next_task(self.machines, tasks)
            self.machines[0] += next_task[0]
            self.machines[1] = max(self.machines[0], self.machines[1]) + next_task[1]
            self.machines[2] = max(self.machines[1], self.machines[2]) + next_task[2]
            scheduled.append(next_task)
            #tasks = np.setdiff1d(tasks, next_task)
            tasks.remove(next_task)
            delay += next_task[4] * max(0, self.machines[2] - next_task[3])
            weight_sum += next_task[4]
        #print(scheduled)
        #print(delay)
        result = round(delay/weight_sum, 2)
        #print(result)
        return scheduled, result

    def savefile(self, outputPath, score, results):
        #print(outputPath)
        with open(outputPath, 'w') as file:
            file.write(str(score))
            file.write('\n')
            for job in results:
                file.write(str(job[5]) + ' ')


if __name__ == "__main__":
    inputpath = sys.argv[1]
    outputdir = sys.argv[2]
    filename = os.path.split(inputpath)[-1]
    outputpath = os.path.join(outputdir, filename.replace("in", "out"))
    listAlgorithm = Algorithm(inputpath)
    scheduled, result = listAlgorithm.scheduling()
    listAlgorithm.savefile(outputpath, result, scheduled)