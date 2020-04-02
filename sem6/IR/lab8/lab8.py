import numpy as np

# L1  = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
L1 = [0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
L2 = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
# L3  = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
L3 = [0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
L4 = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
L5 = [0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
L6 = [0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
L7 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
L8 = [0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
L9 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
L10 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

L = np.array([L1, L2, L3, L4, L5, L6, L7, L8, L9, L10])

ITERATIONS = 100


def getM(L):
    M = np.zeros([10, 10], dtype=float)
    # number of outgoing links
    c = np.zeros([10], dtype=int)

    ## TODO 1 compute the stochastic matrix M
    for i in range(0, 10):
        c[i] = sum(L[i])

    for i in range(0, 10):
        for j in range(0, 10):
            if L[j][i] == 0:
                M[i][j] = 0
            else:
                M[i][j] = 1.0 / c[j]
    return M


print("Matrix L (indices)")
print(L)

M = getM(L)

print("Matrix M (stochastic matrix)")
print(M)

### TODO 2: compute pagerank with damping factor q = 0.15
### Then, sort and print: (page index (first index = 1 add +1) : pagerank)
### (use regular array + sort method + lambda function)
print("PAGERANK")

q = 0.15

pr = np.zeros([10], dtype=float)
pr.fill(0.1)
iterations = 100
for i in range(iterations):
    prCopy = np.zeros([10], dtype=float)
    for rank in range(pr.size):
        prCopy[rank] = q
        for j in range(10):
            prCopy[rank] += (1 - q) * M[j][rank] * pr[j]
    pr = prCopy * (1 / np.sum(prCopy))

res = [(no + 1, pr[no]) for no in range(10)]
res = sorted(res, key=lambda i: i[1], reverse=True)
print(res)

print('sum = ', sum(pr))


### TODO 3: compute trustrank with damping factor q = 0.15
### Documents that are good = 1, 2 (indexes = 0, 1)
### Then, sort and print: (page index (first index = 1, add +1) : trustrank)
### (use regular array + sort method + lambda function)
print("TRUSTRANK (DOCUMENTS 1 AND 2 ARE GOOD)")

q = 0.15

d = [0.5, 0.5, 0, 0, 0, 0, 0, 0, 0, 0]

tr = [v for v in d]

for i in range(iterations):
    trCopy = np.zeros([10], dtype=float)
    for i2 in range(trCopy.size):
        trCopy[i2] = q * d[i2]
        for i3 in range(trCopy.size):
            trCopy[i2] += (1 - q) * tr[i3] * M[i3][i2]
    tr = trCopy * (1 / np.sum(trCopy))

res = [(no + 1, tr[no]) for no in range(10)]
res = sorted(res, key=lambda i: i[1], reverse=True)
print(res)

### TODO 4: Repeat TODO 3 but remove the connections 3->7 and 1->5 (indexes: 2->6, 0->4)
### before computing trustrank

# usuwając te krawędzie wierzchołek numer 3 (index = 2) ma większy trustRank, ponieważ teraz nie prowadzi do
# wierzchołków o zerowej wartości trustRank