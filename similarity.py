# python3
# coding: utf-8
"""
Hamed
"""
import numpy as np
import commonlib as comm
import json
#takes sets

def jaccard(s1, s2): 
    intersect = s1.intersection(s2)
    return len(intersect)/(len(s1)+len(s2))
    
#s1 m s2 should be np.array
def cosine(s1, s2): 
    return sum(s1*s2)/ (np.sqrt(sum(s1**2)) * np.sqrt(sum(s2**2)))

#####        method parameter can equal "cosine" or "jaccard" according to what we need
def getDistance(s1, s2 , method = "cosine"):
    method = method.lower()
    if(method == "jaccard"):
        return jaccard(set(s1),set(s2))
    else: 
        return cosine(s1 , s2)

#This function calculates the similarity between all the columns of the matrix and saves them into a dictionary and writes them into a file for future use    
def buildSimilarityIndex():
    data = comm.getdata()
#    print("similarity.py",data.nnz)
    simindex = dict()
    rowdata, coldata = data.get_shape()
    for i in range(coldata):
        for j in range(i+1, coldata):
            key = str(i) +"," + str(j)
            value = getDistance(data[:, i].toarray(), data[: , j].toarray())
            simindex[key] = float(value)
    f = open("similarity_index.json", "w")
    f.write(json.dumps(dict(simindex)));
    f.close()    
    return simindex
    
#this function calculates most similar items to a certain item from the index and returns a dictionary with keys as distances and each value is a list of items that have the same distance from the item we are comparing to
def getSimilarItems(item, simindex):
#    data = comm.getdata()
    similarsDict = dict()
    for i in range(item):
        value = str(i) +"," + str(item)
        key = simindex[value]
        if(key not in similarsDict.keys()): similarsDict[key] = []
        similarsDict[key].append(value)
#        print(i,",",item)
    for i in range(item+1 , 100):
        value = str(item) + "," + str(i)
        key = simindex[value]
        if(key not in similarsDict.keys()): similarsDict[key] = []
        similarsDict[key].append(value)
    return similarsDict
#bl = getSimilarItems(39,26, simind, test_data)
