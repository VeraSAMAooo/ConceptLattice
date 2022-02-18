# -*- coding: utf-8 -*-

# 应用管理 http://localhost:8000/admin.html?database=admin

#应用数据管理 http://localhost:8000/admin.html?database=apps


from flask import Flask, url_for, redirect, render_template, request, Response, stream_with_context,jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json
import os
import time
import codecs
from flask_cors import *
from pydub import AudioSegment
app = Flask(__name__)
# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求 
CORS(app, resources=r'/*')

databaseUse = 'sqlite3'

import networkx as nx
import matplotlib.pyplot as plt


def printMat(Mat):
	print("Print matrix\n")
	for x in range(0, len(Mat)):
		for y in range(0, len(Mat[0])):
			print(Mat[x][y])
		print("\n")


###########################################################

def getBipartiteCliques(aMat):
	cList = []
	aLen = len(aMat)
	bLen = len(aMat[0])
	#	printMat(aMat)
	#   print(aLen, bLen,  " are aLen and bLen\n\n")
	for x in range(0, aLen):
		tmpList = []
		tmpObj = [obj[x]]

		for y in range(0, bLen):
			if aMat[x][y] == '1':
				tmpList.append(attr[y])

		tmp = tmpObj, tmpList
		dictBC[obj[x]] = tmpList
		cList.append(tmp)

	for x in range(0, bLen):
		tmpList = []
		tmpattr = [attr[x]]

		for y in range(0, aLen):
			if aMat[y][x] == '1':
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
		#	   print ("printing both list for ",  x,  lista,  listo)
		if set(lista) == set(clist[x][1]) and set(listo) == set(clist[x][0]):
			flist.append(clist[x])
	return flist


###########################################################

def generateLattice(bCList):
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
import os
import shutil
@app.route("/getd",methods=['GET'])
def getd():

	###########################################################

	######################## starts here ###########################
	print("python3 FAC.py "+request.args.get('a','erro') + ' '+request.args.get('b','erro') + ' '+request.args.get('c','erro'))
	os.system( "python3 FAC.py "+request.args.get('a','erro') + ' '+request.args.get('b','erro') + ' '+request.args.get('c','erro'))


	time.sleep(10)
	shutil.move('./lattice.png', './static/lattice.png')
	return json.dumps({"msg":"获取成功","data":[]})


	dictBC = {}
	hasSuccessor = []
	hasPredecessor = []

	obj = request.args.get('a','erro')
	numObj = len(obj)



	attr = request.args.get('b','erro')
	numAttr = len(attr)




	aMat = [[0 for i in range(numAttr)] for j in range(numObj)]

	print("\nEnter the adjecency matrix in row major order (0 or 1, one row per line):\n")
	for x in range(0, len(obj)):
		row = input()
		rowlist = row.split()
		a = request.args.get('c','erro').split('/')
		b = a[x].split(' ')
		for y in range(0, len(attr)):
			aMat[x][y] = b[y]
	print(aMat)

	# Get Bipartite Cliques
	bCliques = getBipartiteCliques(aMat)
	bCliquesStore = bCliques

	print("there is the 1111 first bCliques:\n",bCliques)

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

	for j in range(numAttr):
		clist.append(attr[j])
	dlist=["",clist]
	bCliques.append((dlist))
	print("there is the 222 second bCliques:\n",bCliques)




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
	generateLattice(bCliques)
	print("\nLattice has been generated in file 'test_lattice.png'\n")


	return json.dumps({"msg":"获取成功","data":[]})



@app.route("/<name>")
def hello(name):
	return render_template('%s' %name)

#  管理应用
# http://localhost:8000/admin.html?database=admin&type=admin
if __name__ == '__main__':
	# 绑定的地址0.0.0.0，表示任意ip都能访问
	app.run(host='0.0.0.0', port=8000,debug="True")