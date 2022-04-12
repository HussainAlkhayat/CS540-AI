import csv
import numpy as np
import math
import statistics
import random
from statistics import stdev
import copy
def get_dataset(filename):
    dataset = []
    first = True
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for line in reader:
            if not first:
                tempList = []
                for i in line[1:]:
                    tempList.append(float(i))
                dataset.append(tempList)
            else:
                first = False
    npdataset = np.array(dataset)
    return npdataset
"""
dataset = get_dataset("bodyfat.csv")

print(dataset)
print(dataset.shape)
"""
def print_stats(dataset, col):
    print(len(dataset))
    total = 0
    standard = []
    for item in dataset:
        total += item[col]
        standard.append(item[col])
    mean = total/len(dataset)
    #https://www.kite.com/python/answers/how-to-print-a-float-with-two-decimal-places-in-python
    formatedMean = "{:.2f}".format(mean) #this format was taken from the link above
    print(formatedMean)
    deviation = stdev(standard)
    formatedStandard = "{:.2f}".format(deviation)
    print(formatedStandard)

#print_stats(dataset,1)

def regression(dataset, cols, betas):
    n = len(dataset)
    totalSum = 0
    for item in dataset:
        sum = 0
        sum += betas[0]
        index = 1
        for i in cols:
            sum += item[i]*betas[index]
            index += 1
        sum -= item[0]
        totalSum += sum ** 2
    totalSum = totalSum/n
    return totalSum
"""
reg = regression(dataset, cols=[2,3], betas=[0,0,0])
print(reg)
reg = regression(dataset, cols=[2,3,4], betas=[0,-1.1,-.2,3])
print(reg)
"""
def gradient_descent(dataset, cols, betas):
    n = len(dataset)
    returnedList = []
    count = 0
    while count < len(betas):
        sum = 0
        totalSum = 0
        for item in dataset:
            sum = 0
            sum += betas[0]
            index = 1
            for i in cols:
                sum += item[i]*betas[index]
                index += 1
            sum -= item[0]
            if count != 0:
                sum *= item[cols[count-1]]
            totalSum += sum
        totalSum *= 2/n
        returnedList.append(totalSum)
        count += 1
    return np.array(returnedList)
"""
descent = gradient_descent(dataset, cols=[2,3], betas=[0,0,0])
print(descent)
"""
def iterate_gradient(dataset, cols, betas, T, eta):
    count = 1
    returned = gradient_descent(dataset, cols, betas)
    index = 0
    for value in returned:
        betas[index] = betas[index] - eta * value
        index += 1
    while count < T+1:
        returned = gradient_descent(dataset,cols, betas)
        reg = regression(dataset, cols, betas)
        reg = "{:.2f}".format(reg)
        print(str(count) +" "+ reg , end="")
        for beta in betas:
            print(" ", end="")
            beta = "{:.2f}".format(beta)
            print(beta, end="")
        print("")
        index = 0
        for value in returned:
            betas[index] = betas[index] - eta*value
            index += 1
        count += 1
#iterate_gradient(dataset, cols=[1,8], betas=[400,-400,300], T=10, eta=1e-4)

def compute_betas(dataset, cols):
    tempList = []
    y = []
    tempList.append([])
    for i in cols:
        tempList.append([])

    for item in dataset:
        index = 1
        y.append(item[0])
        tempList[0].append(1)
        for i in cols:
            tempList[index].append(item[i])
            index += 1
    x_trans = np.array(tempList)
    x = x_trans.transpose()
    y = np.array(y)
    y = y.transpose()
    m = np.linalg.inv(np.matmul(x_trans, x))
    c= np.matmul(x_trans, y)
    final = np.matmul(m,c)
    strList = []
    for i in final:
        s = float(i)
        s = "{:.8f}".format(s)
        strList.append(s)
    betas = []
    for i in strList:
        betas.append(float(i))
    reg = regression(dataset, cols, betas)
    T = []
    T.append(reg)
    for i in betas:
        T.append(float(i))
    T_tup = (*T, )
    return T_tup
#tuple = compute_betas(dataset, cols=[1,2])
#print(tuple)

def predict(dataset, cols, features):
    T = compute_betas(dataset, cols)

    betas = []
    first = True
    for i in T:
        if not first:
            betas.append(i)
        else:
            first = False
    return betas[0] + betas[1]*features[0] + betas[2]*features[1]
    sum = 0
    for item in dataset:
        y_i = betas[0]
        index = 1
        for i in cols:
            y_i += betas[index]*item[cols[index-1]]
            index += 1
        sum += y_i
    return sum
#p = predict(dataset, cols=[1,2], features=[1.0708, 23])
#print(p)

def random_index_generator(min_val, max_val, seed=42):
    """
    DO NOT MODIFY THIS FUNCTION.
    DO NOT CHANGE THE SEED.
    This generator picks a random value between min_val and max_val,
    seeded by 42.
    """
    random.seed(seed)
    while True:
        yield random.randrange(min_val, max_val)

def sgd(dataset, cols, betas, T, eta):
    rand_generator = random_index_generator(0, len(dataset))
    rand_index = next(rand_generator)
    count = 1
    row = np.array(dataset[rand_index])
    row = [row]
    returned = gradient_descent(row, cols, betas)
    index = 0
    for value in returned:
        betas[index] = betas[index] - eta * value
        index += 1
    while count < T + 1:
        rand_index = next(rand_generator)
        row = np.array(dataset[rand_index])
        row = [row]
        returned = gradient_descent(row, cols, betas)
        reg = regression(dataset, cols, betas)
        reg = "{:.2f}".format(reg)
        print(str(count) + " " + reg, end="")
        for beta in betas:
            print(" ", end="")
            beta = "{:.2f}".format(beta)
            print(beta, end="")
        print("")
        index = 0
        for value in returned:
            betas[index] = betas[index] - eta * value
            index += 1
        count += 1

#sgd(dataset, cols=[2,3], betas=[0,0,0], T=5, eta=1e-6)
#sgd(dataset, cols=[2,8], betas=[-40,0,0.5], T=10, eta=1e-5)