# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import sys
import numpy as np

def printMat(Mat):
    print("Print matrix\n")
    for x in range(0, len(Mat)):
        for y in range(0, len(Mat[0])):
            print(Mat[x][y])
        print("\n")


###########################################################

def getBipartiteCliques(Mat,attr):
    cList = []
    aLen = len(Mat)
    bLen = len(Mat[0])
    #    printMat(aMat)
    #   print(aLen, bLen,  " are aLen and bLen\n\n")
    for x in range(0, aLen):
        tmpList = []
        tmpObj = [obj[x]]

        for y in range(0, bLen):
            if Mat[x][y] == '1':
                tmpList.append(attr[y])

        tmp = tmpObj, tmpList
        dictBC[obj[x]] = tmpList
        cList.append(tmp)

    for x in range(0, bLen):
        tmpList = []
        tmpattr = [attr[x]]

        for y in range(0, aLen):
            if Mat[y][x] == '1':
                tmpList.append(obj[y])

        tmp = tmpList, tmpattr
        dictBC[attr[x]] = tmpList
        cList.append(tmp)

    return cList


###########################################################

def condenseList(inputlist):
    clist = []
    toSkip = []
    for x in range(0, len(inputlist)):
        if x in toSkip:
            continue
        matched = 0;
        for y in range(x + 1, len(inputlist)):
            if y in toSkip:
                continue
            if set(inputlist[x][0]) == set(inputlist[y][0]):
                tmpTuple = inputlist[x][0], list(set(inputlist[x][1]).union(set(inputlist[y][1])))
                clist.append(tmpTuple)
                toSkip.append(y)
                matched = 1
                break
            elif set(inputlist[x][1]) == set(inputlist[y][1]):
                tmpTuple = list(set(inputlist[x][0]).union(set(inputlist[y][0]))), inputlist[x][1]
                clist.append(tmpTuple)
                toSkip.append(y)
                matched = 1;
                break
        if matched == 0:
            clist.append(inputlist[x])

    return clist


###########################################################

def removeUnclosed(clist):
    flist = []
    listo = []
    lista = []
    for x in range(0, len(clist)):
        lista = []
        listo = []
        for y in range(0, len(clist[x][0])):
            if lista == []:
                lista = dictBC[clist[x][0][y]]
            else:
                lista = list(set(lista).intersection(set(dictBC[clist[x][0][y]])))

        for z in range(0, len(clist[x][1])):
            if listo == []:
                listo = dictBC[clist[x][1][z]]
            else:
                listo = list(set(listo).intersection(set(dictBC[clist[x][1][z]])))
        #       print ("printing both list for ",  x,  lista,  listo)
        if set(lista) == set(clist[x][1]) and set(listo) == set(clist[x][0]):
            flist.append(clist[x])
    return flist


###########################################################

def generateLattice(bCList,attr):
    G = nx.Graph()
    for x in range(0, len(bCList)):
        nodeName = "".join(str(m) for m in bCList[x][0]) + ", " + "".join(str(m) for m in bCList[x][1])
        G.add_node(nodeName)

    for x in range(0, len(bCList)):
        for y in range(x + 1, len(bCList)):
            if set(bCList[x][0]).issubset(set(bCList[y][0])):
                nodeName1 = "".join(str(m) for m in bCList[x][0]) + ", " + "".join(str(m) for m in bCList[x][1])
                nodeName2 = "".join(str(m) for m in bCList[y][0]) + ", " + "".join(str(m) for m in bCList[y][1])
                G.add_edge(nodeName1, nodeName2)
                hasSuccessor.append(x)
                hasPredecessor.append(y)

    # Creating top most and bottom most node
    listo = []
    lista = []
    for x in range(0, len(attr)):
        if listo == []:
            listo = dictBC[attr[x]]
        else:x
    listo = list(set(listo).intersection(set(attr[x])))

    for x in range(0, len(obj)):
        if lista == []:
            lista = dictBC[obj[x]]
        else:
            lista = list(set(lista).intersection(set(obj[x])))
    if lista == []:
        lista = ["null"]
    if listo == []:
        listo = ["null"]

    # adding them to graph
    firstNode = "".join(str(m) for m in listo) + ", " + "".join(str(m) for m in attr)
    G.add_node(firstNode)
    lastNode = "".join(str(m) for m in obj) + ", " + "".join(str(m) for m in lista)
    G.add_node(lastNode)

    # adding edges to them
    for x in range(0, len(bCList)):
        if x not in hasSuccessor:
            nodeName = "".join(str(m) for m in bCList[x][0]) + ", " + "".join(str(m) for m in bCList[x][1])
            G.add_edge(nodeName, lastNode)

    for x in range(0, len(bCList)):
        if x not in hasPredecessor:
            nodeName = "".join(str(m) for m in bCList[x][0]) + ", " + "".join(str(m) for m in bCList[x][1])
            G.add_edge(nodeName, firstNode)
    nx.draw(G)
    plt.savefig("lattice.png")

def matrix_01(Num_Objects,len_Attr):
    Mat=[[0 for i in range(len_Attr)] for j in range(Num_Objects)]
    for x in range(0, Num_Objects):
        row=input()
        rowlist = row.split()
        for y in range(0, len_Attr):
            Mat[x][y] = rowlist[y]
    return Mat

###########################################################

######################## starts here ###########################

dictBC = {}
hasSuccessor = []
hasPredecessor = []

obj = input("Input the C1 Obj seperated by space:\n").split()
numObj = len(obj)

attr_C1 = input("\nInput the C1 attr seperated by space:\n").split()
numAttr_C1 = len(attr_C1)

attr_Q = input("\nInput the refine Q set belongs to attr_C1 seperated by space:\n").split()
numAttr_Q = len(attr_Q)

#print("there is attr_Q:\n:",attr_Q)

R_attrC1= input("\nInput rough attr R :\n")
R_attrC1=list(R_attrC1)
numR_attrC1=len(R_attrC1)

print("\nEnter the first matrix in row major order (0 or 1, one row per line):\n")
Mat_C1 = matrix_01(numObj,numAttr_C1)

#print("there is Mat_C1:\n:",Mat_C1)

print("\nEnter the second matrix in row major order (0 or 1, one row per line):\n")
Mat_R = matrix_01(numObj,numR_attrC1)

#print("there is Mat_R:\n:",Mat_R)

# Get Bipartite Cliques
bCliques = getBipartiteCliques(Mat_C1,attr_C1)
bCliquesStore = bCliques

#print("there is the 1111 first bCliques:\n",bCliques)
bCListSize = len(bCliques)
bCListSizeCondensed = -1

# Condense bipartite cliques until no change
while bCListSize != bCListSizeCondensed:
    bCListSize = len(bCliques)
    bCliques = condenseList(bCliques)
    bCListSizeCondensed = len(bCliques)
#print("there is B1 bCliques:\n",bCliques)

# filter concepts
#bCliques = removeUnclosed(bCliques)

#print("there is the 333 third bCliques:\n",bCliques)
print("\nNodes of Concept Lattice:\n")
for x in range(0, len(bCliques)):
    extent = "".join(str(m) for m in sorted(bCliques[x][0]))
    intent = "".join(str(m) for m in sorted(bCliques[x][1]))
    print("(", extent, ",", intent, ")")

conceptDict = {}
for x in range(0, len(bCliques)):
    object = "".join(str(m) for m in sorted(bCliques[x][0]))
    attribute = "".join(str(m) for m in sorted(bCliques[x][1]))
    conceptDict[object] = set(bCliques[x][1])
    conceptDict[attribute] = set(bCliques[x][0])

# sort the concepts based on intent length
bCliques.sort(key=lambda x: len(x[0]))

# generate the image file containing the lattice
generateLattice(bCliques,attr_C1)
print("\nLattice has been generated in file 'ZIlattice.png'\n")


###粗化属性后

new_attr=(attr_C1+R_attrC1)
Size_new_attr=len(new_attr)
print("there is new_attr:\n:",new_attr)
for i in reversed(range(Size_new_attr)):
    if new_attr[i] in attr_Q:
        new_attr.remove(new_attr[i])

#print("there is 2new_attr:\n:",new_attr)

pos=[]
for item in attr_Q:
    pos.append(attr_C1.index(item))

Mat_com=np.delete(Mat_C1,pos,axis=1)

new_Mat=np.hstack((Mat_com,Mat_R))

bCliques_W = getBipartiteCliques(new_Mat,new_attr)
bCliquesStore_W = bCliques_W

#print("there is the 1111 first bCliques:\n",bCliques)
bCListSize_W = len(bCliques_W)
bCListSizeCondensed_W=-1
# Condense bipartite cliques until no change
while bCListSize_W != bCListSizeCondensed_W:
    bCListSize_W = len(bCliques_W)
    bCliques_W = condenseList(bCliques_W)
    bCListSizeCondensed_W = len(bCliques_W)
#print("there is B2 bCliques:\n",bCliques_W)

# filter concepts
#bCliques = removeUnclosed(bCliques)

#print("there is the 333 third bCliques:\n",bCliques)
#print("\nNodes of B2 Concept Lattice:\n")
for x in range(0, len(bCliques_W)):
    extent = "".join(str(m) for m in sorted(bCliques_W[x][0]))
    intent = "".join(str(m) for m in sorted(bCliques_W[x][1]))
    print("(", extent, ",", intent, ")")

conceptDict_W = {}
for x in range(0, len(bCliques_W)):
    object = "".join(str(m) for m in sorted(bCliques_W[x][0]))
    attribute = "".join(str(m) for m in sorted(bCliques_W[x][1]))
    conceptDict_W[object] = set(bCliques_W[x][1])
    conceptDict_W[attribute] = set(bCliques_W[x][0])

# sort the concepts based on intent length
bCliques_W.sort(key=lambda x: len(x[0]))

# generate the image file containing the lattice
generateLattice(bCliques_W,new_attr)
print("\nLattice has been generated in file 'ZOlattice.png'\n")


# Queries
while True:
    qin = input("Enter the query. Intent or Extent seperated by space, Ex- 2 3 4 OR a b\nEnter 'Q' to exit.\n")
    if qin == "Q":
        sys.exit(0)
    key = "".join(str(m) for m in sorted(qin.split()))
    if key in conceptDict:
        print(', '.join(conceptDict[key]), "\n")
    else:
        print("Not present in Concept lattice\n")

