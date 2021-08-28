import sys
import os

f = open(sys.argv[1], "r")

lines = f.readlines()
linescopy = lines.copy()
n = int(lines[0])

numbers = list(range(0, n))

time = 0

result = []
r = []
ids = []

del linescopy[0]

time1 = 0
time11 = time1
time2 = 0
time22 = time2
time3 = 0
time33 = time3

for i in range(n):
    for j in range(len(linescopy)):
        p1 = int(linescopy[j].split()[0])
        p2 = int(linescopy[j].split()[1])
        p3 = int(linescopy[j].split()[2])
        d = int(linescopy[j].split()[3])
        w = int(linescopy[j].split()[4])
        time1 = time11 + p1
        time2 = max(time11, time22) + p2
        time3 = max(time33, time22) + p3
        
        r.append(d+time3/w)
    
    numbers = list(range(0, len(linescopy)+1))
    res = [numbers for _,numbers in sorted(zip(r,numbers))][0]
    r.clear()
    copy = linescopy[res]
    result.append(lines.index(copy))

    del linescopy[res]

    a = lines.index(copy)
    
    time1 = time11
    time2 = time22
    time3 = time33

    time1 += int(lines[a].split()[0])
    time11 = time1
    time2 = max(time1, time2) + int(lines[a].split()[1])
    time22 = time2
    time3 = max(time3, time2) + int(lines[a].split()[2])
    time33 = time3
    
time1 = 0
time2 = 0
time3 = 0

D1 = []
D2 = []

for i in result:
    time1 += int(lines[i].split()[0])

    time2 = max(time1, time2) + int(lines[i].split()[1])
    
    time3 = max(time2, time3) + int(lines[i].split()[2])

    D = max(0, max(time1, time2, time3) - int(lines[i].split()[3]))
    D1.append(D*int(lines[i].split()[4]))
    D2.append(int(lines[i].split()[4]))
    time = 0

sum1 = sum(D1)
sum2 = sum(D2)
Dw = sum1/sum2

id = sys.argv[1].find('in_')
id2 = sys.argv[1].find('_',id+3) 

surname = sys.argv[1][id+3:id2]

outputdir = ""
if(len(sys.argv)>2):
    outputdir = sys.argv[2] 

f = open(os.path.join(outputdir, "out_" + surname + "_" + str(n) + ".txt"), "w")
Dw = round(Dw, 2)
print(Dw)
f.write(str(Dw) + "\n")

for i in range(n-1):
    f.write(str(result[i]) + " ") 

f.write(str(result[n-1]))







