import csv
import numpy as np
import math

def load_data(filepath):
    pokemonList = []
    #this was taken from teh following link: https://docs.python.org/3/library/csv.html
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar='|')
        first = True
        for line in reader:
            if not first:
                dict = {"#": int(line[0]), "Name": line[1], "Type 1": line[2], "Type 2": line[3], "Total": int(line[4]), "HP": int(line[5]),
                        "Attack": int(line[6]), "Defense": int(line[7]), "Sp. Atk": int(line[8]), "Sp. Def": int(line[9]), "Speed": int(line[10])}
                pokemonList.append(dict)
            else:
                first = False
            if len(pokemonList) == 20:
                return pokemonList

def calculate_x_y(stats):
    x = stats["Attack"] + stats["Sp. Atk"] + stats["Speed"]
    y = stats["HP"] + stats["Defense"] + stats["Sp. Def"]
    return (x,y)

def calculate_dist_point(point1, point2):
    #this code was directly taken from : https://community.esri.com/thread/158038
    dist = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
    return dist

def calculate_dist_clust(cluster1, cluster2):
    min_dist = float('inf')
    for point1 in cluster1:
        for point2 in cluster2:
            tempDist = calculate_dist_point(point1, point2)
            if tempDist < min_dist:
                min_dist = tempDist
    return min_dist

def calculate_dist_Dict(Dict):
    minDistClus = []
    for key1 in Dict.keys():
        for key2 in Dict.keys():
            if key1 != key2:
                cluster1 = Dict[key1]
                cluster2 = Dict[key2]
                dist = calculate_dist_clust(cluster1, cluster2)
                if len(minDistClus) == 0:
                    if key1 < key2:
                        minDistClus = [key1, key2, dist, cluster1 + cluster2]
                    else:
                        minDistClus = [key2, key1, dist, cluster1 + cluster2]
                elif dist < minDistClus[2]:
                    if key1 < key2:
                        minDistClus = [key1, key2, dist, cluster1 + cluster2]
                    else:
                        minDistClus = [key2, key1, dist, cluster1 + cluster2]
                elif dist == minDistClus[2]: #tie breaker
                    smallestKey = None
                    biggerKey = None
                    if key1 < key2:
                        smallestKey = key1
                        biggerKey = key2
                    else:
                        smallestKey = key2
                        biggerKey = key1

                    if smallestKey < minDistClus[0]:
                        minDistClus = [smallestKey, biggerKey, dist, cluster1 + cluster2]
                    elif smallestKey == minDistClus[0]:
                        if biggerKey < minDistClus[1]:
                            minDistClus = [smallestKey, biggerKey, dist, cluster1 + cluster2]

    return minDistClus

def hac(dataset):
    z = []
    index = 0
    clusterDict = {}
    for point in dataset:
        clusterDict[index] = [point]
        index += 1
    while len(clusterDict) > 1:
        minDistClus = []
        tempClus = calculate_dist_Dict(clusterDict)
        clusterDict[index] = tempClus[3]
        clusterDict.pop(tempClus[0])
        clusterDict.pop(tempClus[1])
        minDistClus = [tempClus[0], tempClus[1], tempClus[2], len(tempClus[3])]
        z.append(minDistClus)
        index += 1

    z = np.array(z)
    return z



