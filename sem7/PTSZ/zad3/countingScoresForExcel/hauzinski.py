import os
import sys
import time
import statistics
import math

# MAGIC NUBMER DEFS
P1 = 0
P2 = 1
P3 = 2
D = 3
W = 4
IDX = 5

MACHINE_COUNT = 3

# TOOLS
def jobScore(previous_job, job, machine_clocks):
  shape_diff = (abs(previous_job[P2] - job[P1]) + abs((max(previous_job[P2], job[P1]) + job[P2]) - (previous_job[P2] + previous_job[P3])))

  p1 = machine_clocks[P1] + job[P1]
  p2 = max(p1, machine_clocks[P2]) + job[P2]
  p3 = max(p2, machine_clocks[P3]) + job[P3]
  return (abs(p3 - job[D]) + shape_diff)/job[W]  

def chooseJob(previous_job, jobs, machine_clocks):
  best_job = []
  best_score = -1
  for job in jobs:
    score = jobScore(previous_job, job, machine_clocks)
    if score < best_score or best_score == -1 or (score == best_score and job[W] > best_job[W]):
      best_job = job
      best_score = score
  return best_job

# IO
in_filename = sys.argv[1]
out_dir = sys.argv[2]

file = open(in_filename, 'r') 
content = file.readlines()
job_strings = content[1:]
file.close()

# PARSING
jobs = [[int(val) for val in job_string.split(' ')] + [idx+1] for idx, job_string in enumerate(job_strings)]
unscheduled_jobs = jobs[:]

# SCHEDULING
schedule = []
previous_job = []
machine_clocks = [0 for i in range(0, MACHINE_COUNT)]
for i in range(len(jobs)):
  next_job = []
  if previous_job == []:
    best_job = []
    min_due = -1
    for job in unscheduled_jobs:
      if job[D] < min_due or min_due == -1:
        min_due = job[D]
        best_job = job
    next_job = best_job
  else:
    next_job = chooseJob(previous_job, unscheduled_jobs, machine_clocks)

  machine_clocks[P1] += next_job[P1]
  machine_clocks[P2] = max(machine_clocks[P1], machine_clocks[P2]) + next_job[P2]
  machine_clocks[P3] = max(machine_clocks[P2], machine_clocks[P3]) + next_job[P3]
  previous_job = next_job
  schedule.append(next_job[IDX])
  unscheduled_jobs.remove(next_job)

# COST CALCULATION
machine_clocks = [0 for i in range(0, MACHINE_COUNT)]
weight_sum = 0
cost = 0
for job_idx in schedule:
  # finding job
  next_job = []
  for job in jobs:
    if(job[IDX] == job_idx):
      next_job = job
  # updating machine clocks
  machine_clocks[P1] += next_job[P1]
  machine_clocks[P2] = max(machine_clocks[P1], machine_clocks[P2]) + next_job[P2]
  machine_clocks[P3] = max(machine_clocks[P2], machine_clocks[P3]) + next_job[P3]
  # updating weight sum and cost
  weight_sum += next_job[W]
  cost += next_job[W] * max(0, machine_clocks[P3] - next_job[D])

final_cost = round(cost/weight_sum, 2)
#print(round(cost/weight_sum, 2))

# IO
path = os.path.join(out_dir, os.path.split(in_filename)[-1].replace('in_', 'out_'))

content = ' '.join([str(job_idx) for job_idx in schedule])
content = str(final_cost) + '\n' + content

file = open(path, 'w')
file.writelines(content)
file.close()