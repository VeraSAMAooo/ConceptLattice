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
    plt.savefig("515lattice.png")

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

print("\nEnter the first matrix in row major order (0 or 1, one row per line):\n")
Mat_C1 = matrix_01(numObj,numAttr_C1)

p_attrC1= input("\nInput p belongs to attrC1:\n")

attr_W = input("\nInput the refine set W seperated by space:\n").split()
numAttr_W = len(attr_W)

print("\nEnter the second matrix in row major order (0 or 1, one row per line):\n")
Mat_W = matrix_01(numObj,numAttr_W)

print("there is def_matrix_01:\n:",Mat_C1)




# Get Bipartite Cliques
bCliques = getBipartiteCliques(Mat_C1,attr_C1)








bCliquesStore = bCliques

print("there is def_getBipartiteCliques bCliques:\n",bCliques)
bCListSize = len(bCliques)
bCListSizeCondensed = -1

# Condense bipartite cliques until no change
while bCListSize != bCListSizeCondensed:
    bCListSize = len(bCliques)
    bCliques = condenseList(bCliques)
    bCListSizeCondensed = len(bCliques)

alist=[]

for i in range(numObj):
    alist.append(obj[i])
blist=[alist,""]
bCliques.append(blist)

clist=[]

for j in range(numAttr_C1):
    clist.append(attr_C1[j])
dlist=["",clist]
bCliques.append((dlist))

print("there is def_condenseList bCliques:\n",bCliques)

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
#print("\nLattice has been generated in file 'BFzoomInLattice.png'\n")


###细分属性后

new_attr=(attr_C1+attr_W)
new_attr.remove(p_attrC1)

Mat_com=np.delete(Mat_C1,attr_C1.index(p_attrC1),axis=1)
#print("there is common mat:\n",Mat_com)
new_Mat=np.hstack((Mat_com,Mat_W))

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
print("there is B2 bCliques:\n",bCliques_W)



#print("there is the 333 third bCliques:\n",bCliques)
print("\nNodes of B2 Concept Lattice:\n")
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
#generateLattice(bCliques_W,new_attr)
#print("\nLattice has been generated in file 'AFzoom-inLattice.png'\n")


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