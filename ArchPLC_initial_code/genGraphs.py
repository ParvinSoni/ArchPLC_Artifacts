import networkx as nx
import matplotlib.pyplot as plt
import os
import re
import time
import xml.etree.ElementTree as ET
import sys
import pydot

start_time = time.time()


 # save graph in dot format
 # dot -Tpdf PLCprog-PDG.dot -o PLCprog-PDG.pdf
 # dot -Tpng PLCprog-PDG.dot -o PLCprog-PDG.png
 # dot PLCprog-PDG.dot -Tjpg -o PLCprog-PDG.jpg

# o_f_IR = open("IR_directVars.txt", "r")
o_f_IR = open("IR.txt", "r")
IRlines = o_f_IR.readlines()
IRlines = [x.strip() for x in IRlines]
globalStmtCounter = 0

declFunctions = None
funcDeclVars = None

class node:
	stmtName = ""
	nodeType = ""
	dataName = ""
	nSubType = ""
	nodeValue = ""
	label = ""
	lineTupleSize = ""
	regionType = ""
	regionName = ""
	controlID = ""
	rTag = ""


def findRegions(IRlines):
	startEndRegions = {}
	regionDefinitions = ["(FUNC, ", "(PROG, ", "(CONFIG, ", "(DATA_BLOCK, ", "(structure-type-name, ", "(DIRECT_VARS, "] #
 
	for i in range(0, len(IRlines)):
		for definition in regionDefinitions:
			if IRlines[i].startswith(definition) or i == len(IRlines)-1:
				keysList = list(startEndRegions.keys())
				if (not len(keysList) == 0) or i == len(IRlines)-1:
					last_index = keysList[-1]
					startEndRegions[last_index] = i
				if not i == len(IRlines)-1:
					startEndRegions[i] = i
				break

	return startEndRegions

		
def add_node(G, stmtName, nodeType, dataName, nSubType="", nodeValue="", nodeLabel="", nodeLineSize=2, regionType="", regionName="", rTag=""):
	if len(stmtName) > 0:
		if not G.has_node(stmtName):
			# print("*: " + stmtName)
			G.add_node(stmtName, dataName=dataName, nType=nodeType, nSubType=nSubType, nValue=nodeValue, nSize=nodeLineSize, label=nodeLabel, regionType=regionType, regionName=regionName, rTag=rTag)


def isDuplicateEdge(G, source, destination, edgeLabel):
	# no edges, no duplicates
	if not G.has_edge(source, destination):
		return False
	
	for (u, v, c) in G.out_edges.data(nbunch=source):
		if u == source and v == destination and c["tLabel"] == edgeLabel:
			return True
		
	return False

def add_edge(G, source, destination, edgeLabel):
	if isDuplicateEdge(G, source, destination, edgeLabel):
		print("Duplicate edge!")
		return

	if len(source) == 0 or len(destination) == 0 or not source in list(G.nodes()) or not destination in list(G.nodes()):
		print("source: " + str(source) + ", destination: " + str(destination))
		return

	if not "nType" in list(G.nodes(data=True)[source].keys()):
		print("G.nodes(data=True)[source]: " + str(G.nodes(data=True)[source]))
	if not "nType" in list(G.nodes(data=True)[destination].keys()):
		print("G.nodes(data=True)[destination]: " + str(G.nodes(data=True)[destination]))



	if len(source) > 0 and len(destination) > 0:
		# G.add_edge(source, destination, label=edgeLabel) # print on edge
		if edgeLabel == "ctrl":
			G.add_edge(source, destination, style="solid", tLabel=edgeLabel, color="black")
		elif edgeLabel == "data":
			G.add_edge(source, destination, style="dashed", tLabel=edgeLabel, color="red")
		elif edgeLabel == "interp-ctrl":
			G.add_edge(source, destination, style="dotted", tLabel=edgeLabel, color="blue")
		elif edgeLabel == "interp-data":
			G.add_edge(source, destination, style="dotted", tLabel=edgeLabel, color="orange")
		elif edgeLabel == "global-data":
			G.add_edge(source, destination, style="dotted", tLabel=edgeLabel, color="green")

	if G.nodes(data=True)[source]["nType"] == "case-statement" or G.nodes(data=True)[source]["nType"] == "case-element":
		if G.nodes(data=True)[destination]["nType"] == "case-element":
			if edgeLabel == "ctrl":
				if len(G.nodes(data=True)[source]["nValue"]) > 0:
					nValue = G.nodes(data=True)[source]["nValue"][0]
					if not nValue in G.nodes(data=True)[destination]["nValue"]:
						G.nodes(data=True)[destination]["nValue"].append(nValue)

	if G.nodes(data=True)[source]["nType"] == "for-statement":
		if G.nodes(data=True)[destination]["nType"] == "for-list":
			if edgeLabel == "ctrl":
				if len(G.nodes(data=True)[source]["nValue"]) > 0:
					lineTuple = tuple(G.nodes(data=True)[destination]["label"][1:-1].split(", "))
					nValue = G.nodes(data=True)[source]["nValue"][0] + "_" + str(lineTuple[-2]) + "_" + str(lineTuple[-1])
					if not nValue in G.nodes(data=True)[destination]["nValue"]:
						G.nodes(data=True)[destination]["nValue"].append(nValue)


def parseLine(line, regionType, regionName):
	global globalStmtCounter

	# if not regionType == "FUNC":
	# 	print(regionType)
	# 	None

	operators = ["elevated-by", "plus", "minus", "logical-not", "multiply-with", "divide-by", "modulo", "adding",
	"subtracting", "equals", "equals-not", "less-or-equal", "greater-or-equal", "less-than", "greater-than",
	"logical-or", "logical-xor", "logical-and"]
	unary_operators = ["logical-not"]
	binary_operators = ["elevated-by", "plus", "minus", "multiply-with", "divide-by", "modulo", "adding",
	"subtracting", "equals", "equals-not", "less-or-equal", "greater-or-equal", "less-than", "greater-than",
	"logical-or", "logical-xor", "logical-and"]

	n = node()
	lineTuple = tuple(line[1:-1].split(", "))
	n.stmtName = "stmt_" + str(globalStmtCounter)
	globalStmtCounter += 1
	n.lineTupleSize = len(lineTuple)
	n.nodeType = lineTuple[0]
	n.dataName = lineTuple[1]
	n.rTag = lineTuple[1]
	n.nSubType = ""
	n.nodeValue = []
	n.label = line
	n.regionType = regionType
	n.regionName = regionName

	if lineTuple[1][0] == "r" and lineTuple[1][1:].isdigit():
		n.controlID = lineTuple[1]
		# n.dataName = "" # handle in ASSIGNMENT & IVAR

	if "DATA_BLOCK" in n.nodeType:
		n.rTag = ""
		n.nSubType = lineTuple[2]
		n.nodeValue = list(lineTuple[3:])
		# print(n.nodeValue)
		# print("DATA_BLOCK22222")
		# print(lineTuple)
		# None

	if "DIRECT_VARS" in n.nodeType:
		n.rTag = ""
		n.nSubType = "DIRECT_VARS"

	if "structure-type-name" in n.nodeType:
		print(lineTuple)
		n.rTag = ""
		n.nSubType = lineTuple[1]

	if "structure-element-declaration" in n.nodeType:
		n.rTag = ""
		n.nSubType = lineTuple[2]

	if "-declarations" in n.nodeType:
		if n.lineTupleSize == 4:
			n.nSubType = "directVar_" + lineTuple[2]
			n.nodeValue = [lineTuple[2]]
		if n.lineTupleSize == 3:
			n.nSubType = lineTuple[2]

		# if n.nodeType == "input-declarations":
		if "input" in n.nodeType and "declarations" in n.nodeType:
			n.nodeValue.append("formalInPara_" + n.regionName + "_" + n.dataName)

	if "IVAR" == n.nodeType:

		# if lineTuple[2] == "multi-element-variable":
		# 	n.nSubType = "multi-element-variable"
		# 	n.nodeValue = [lineTuple[-3], lineTuple[-1]]
		# else:
		# 	if n.lineTupleSize == 3:
		# 		n.nSubType = "const"
		# 		n.nodeValue = [lineTuple[-1]]
		# 		# if re.match(r[0-9]+):
		# 	if n.lineTupleSize == 4:
		# 		n.nSubType = "1-op"
		# 		n.nodeValue = [lineTuple[-1]]
		# 	if n.lineTupleSize == 5:
		# 		n.nSubType = "2-op"
		# 		n.nodeValue = [lineTuple[-3], lineTuple[-1]]

		new_str = ""
		substr = lineTuple[2:]
		firstIter = True
		n.nSubType = ""

		# for unary_op in unary_operators:
		# 	if unary_op in substr:
		# 		n.nSubType = "1-op"

		# if line.count("multi-element-variable") == 2:
		# 	n.nSubType = "2-op"

		# for binary_op in binary_operators:
		# 	if binary_op in substr:
		# 		n.nSubType = "2-op"

		for i in range(0, len(substr)):
			if substr[i] == "multi-element-variable" or substr[i] in binary_operators:
				if len(new_str) > 0:
					if not new_str in n.nodeValue:
						n.nodeValue.append(new_str)
					new_str = ""
					firstIter = True
				continue

			if substr[i] in operators or substr[i] == "field-selector":
				continue
			
			if not firstIter:
				new_str += "@"

			new_str += substr[i]

			if i == len(substr)-1 and len(new_str) > 0:
				if not new_str in n.nodeValue:
					n.nodeValue.append(new_str)
				new_str = ""

			firstIter = False
		# if "r220147" in substr:
		# 	print("!!!!!!!!!!")
		# 	print(n.regionName)
		# 	print(n.nodeValue)
		# 	sys.exit()

	if "ASSIGNMENT" == n.nodeType:
		# n.nodeValue = [lineTuple[2]]
		n.nodeValue = [lineTuple[-1]] # all values in FT are 1-term
		startIndex = 1

		# n.nSubType = "const-value"
		# if lineTuple[-1][0] == "r" and lineTuple[-1][1:].isdigit():
		# 	n.nSubType = "reference-value"

		if lineTuple[1][0] == "r" and lineTuple[1][1:].isdigit():
			# print(lineTuple[1])
			startIndex = 2

			# "some" ASSIGNMENT statements have control dependency on some statement list (, hence r number)
			# n.nodeValue.append(lineTuple[1])
			# n.controlID = lineTuple[1]
		
		new_str = ""
		substr = lineTuple[startIndex:-1]
		firstIter = True
		for i in range(0, len(substr)):
			if substr[i] == "multi-element-variable" or substr[i] == "field-selector":
				continue
				
			if not firstIter:
				new_str += "@"
			new_str += substr[i]
			firstIter = False

		# update destination node, this is useful if it is a struct-field var, or array index var
		n.dataName = new_str

	if "function-call" == n.nodeType:
		if n.lineTupleSize >= 3:
			n.nSubType = lineTuple[2]
		if n.lineTupleSize >= 4:
			n.nodeValue = list(lineTuple[3:])

	if "fb-invocation" == n.nodeType:
		# print(lineTuple)
		if n.lineTupleSize >= 4:
			if lineTuple[1][0] == "r" and lineTuple[1][1:].isdigit():
				n.nSubType = lineTuple[2] # for constructFuncSDG()
				n.dataName = lineTuple[2] # for constructSDG()
			else:
				n.nSubType = lineTuple[1] # for constructFuncSDG()
				n.dataName = lineTuple[1] # for constructSDG()

			if lineTuple[1][0] == "r" and lineTuple[1][1:].isdigit():
				n.nodeValue = list(lineTuple[2:]) # list(lineTuple[3:]) # (doesn't include ptr name)
			else:
				n.nodeValue = list(lineTuple[1:]) # list(lineTuple[2:]) # (doesn't include ptr name)
		elif n.lineTupleSize == 2:
			n.nSubType = lineTuple[1] # for constructFuncSDG()
			n.dataName = lineTuple[1] # for constructSDG()

			# if lineTuple[1][-3:] == "_DB":
			# 	n.nSubType = lineTuple[1][:-3]
			# 	if not regionName in funcDeclVars.keys():
			# 		funcDeclVars[regionName] = {}
			# 	funcDeclVars[regionName][n.nSubType] = n.nSubType

	if "direct-variable" == n.nodeType:
		if n.lineTupleSize == 8:
			n.nSubType = lineTuple[3]
			n.nodeValue = [str(lineTuple[3]+lineTuple[5]+lineTuple[7])]
		if n.lineTupleSize == 11:
			n.nSubType = lineTuple[3]
			n.nodeValue = [str(lineTuple[3]+lineTuple[5]+lineTuple[7]+"."+lineTuple[-1])]

	if "if-statement" == n.nodeType:
		if n.lineTupleSize >= 3:
			# if not (lineTuple[2][0] == "r" and lineTuple[2][1:].isdigit()):
			# 	if not str(lineTuple[2]) in n.nodeValue:
			# 		n.nodeValue.append(str(lineTuple[2]))
			if not str(lineTuple[2]) in n.nodeValue:
				n.nodeValue.append(str(lineTuple[2]))

	if "case-statement" == n.nodeType:
		if n.lineTupleSize >= 3:
			if not str(lineTuple[2]) in n.nodeValue:
				n.nodeValue.append(str(lineTuple[2]))

	if "for-statement" == n.nodeType:
		if n.lineTupleSize >= 3:
			if not str(lineTuple[2]) in n.nodeValue:
				n.nodeValue.append(str(lineTuple[2]))

	# if "for-list" == n.nodeType:
	# 	if n.lineTupleSize >= 3:
	# 		if not str(lineTuple[2]) in n.nodeValue:
	# 			n.nodeValue.append(str(lineTuple[-2]) + "_" + str(lineTuple[-1]))

	# for the if-statements that have "t" as their dataName
	# if n.dataName == "t":
	# 	n.dataName = ""

	return n


def skipRegion(firstLine):
	if firstLine.startswith("(CONFIG, "): # "CONFIG block need some fixes on the IR part, mostly not needed, skip it."
		return True
	return False

def skipNode(n):
	# if "-declarations" in n.nodeType and n.lineTupleSize == 3: # not a good idea, some variable are non-initialized, e.g., %IX0
	# 	return True
	return False

def findnth(haystack, needle, n):
	if not needle in haystack or haystack.count(needle) < n:
		return -1

	last_index = 0
	cumulative_last_index = 0
	for i in range(0, n):
		last_index = haystack[cumulative_last_index:].find(needle)
		cumulative_last_index += last_index

		# if not last element, then jump over it
		if i < n-1:
			cumulative_last_index += len(needle)

	return cumulative_last_index

if_cond_mapping = {}
def constructCFG(regionlines):
	global globalStmtCounter, if_cond_mapping

	firstLine = regionlines[0]
	firstLineTuple = tuple(firstLine[1:-1].split(", "))
	regionType = firstLineTuple[0]
	regionName = firstLineTuple[1]
	prev_n = ""
	firstNode = True
	G = nx.MultiDiGraph(name="PLCprog-CFG-" + regionType + "-" + regionName, data=True, align='vertical')

	print(regionName)
	
	entryNode = "ENTRY_"+regionName

	

	stored_globalStmtCounter = globalStmtCounter
	for line in regionlines[1:]:
		n = parseLine(line, regionType, regionName)
		# print("n2: " + str(n.stmtName) + ", " + str(n.nodeType))

		# if "R_TRIG" in entryNode:
		# 	print("!!!!4")
		# 	print(regionlines)
		# 	print(line)
		# 	print(n.dataName)
		# 	print(regionName)
		# 	print(n.stmtName)
		# 	sys.exit()

		add_node(G, n.stmtName, n.nodeType, n.dataName, n.nSubType, n.nodeValue, n.label, n.lineTupleSize, regionType, regionName, n.rTag)
		# if "r220147" in n.nodeValue:
		# 	print("!!!!!!!!!!")
		# 	print(n.regionName)
		# 	print(n.nodeValue)
		# 	sys.exit()

	globalStmtCounter = stored_globalStmtCounter
	for line in regionlines[1:]:
		n = parseLine(line, regionType, regionName)

		if not firstNode:
			# print("e1: " + str(prev_n) + ", " + str(n.stmtName))
			if not (n.rTag[0] == "r" and n.rTag[1:].isdigit()):

				print("=======")
				# print(n.label)
				# print(n.dataName)
				# print(n.nodeType)
				print(G.nodes(data=True)[prev_n])
				print(G.nodes(data=True)[n.stmtName])

				add_edge(G, prev_n, n.stmtName, "ctrl")
				prev_n = n.stmtName

		if firstNode:
			firstNode = False
			prev_n = n.stmtName

			add_node(G, entryNode, "ENTRY_NODE", "ENTRY_NODE", nodeLabel=entryNode, regionType=regionType, regionName=regionName)
			add_edge(G, entryNode, prev_n, "ctrl")

	exitNode = "EXIT_"+regionName
	add_node(G, exitNode, "EXIT_NODE", "EXIT_NODE", nodeLabel=exitNode, regionType=regionType, regionName=regionName)
	add_edge(G, prev_n, exitNode, "ctrl")
	add_edge(G, entryNode, exitNode, "ctrl")

	specialEdges = {}
	for n in G.nodes(data=True):
		print("TTTTTTT")
		print(n[1])
		print(n[0])
		# 	None
		if len(n[1]["rTag"]) == 0:
			continue

		if not (n[1]["rTag"][0] == "r" and n[1]["rTag"][1:].isdigit()):
			continue

		if n[1]["nType"] == "statement-list":
			nth_index = findnth(n[1]["label"], ", ", 2)
			temp_elements = n[1]["label"][nth_index:-1].split(", ")
			firstIter = True
			prev_e = None
			elements = []
			for e in temp_elements:
				if len(e) > 0:
					elements.append(e)

			for e in elements:
				if firstIter:
					if not n[1]["rTag"] in specialEdges.keys():
						specialEdges[n[1]["rTag"]] = []
					specialEdges[n[1]["rTag"]].append(e)
					firstIter = False
					prev_e = e # n[1]["rTag"]
					continue
				if not prev_e in specialEdges.keys():
					specialEdges[prev_e] = []
				specialEdges[prev_e].append(e)
				prev_e = e
	
	tempG = nx.MultiDiGraph(name="tempG", data=True, align='vertical')
	tempG.add_nodes_from(G.nodes(data=True))
	tempG.add_edges_from(G.edges(data=True))
	toPrependNode = {}
	toPostpendNode = {}
	latestIVARAdded = {}

	for n in tempG.nodes(data=True):
		if len(n[1]["rTag"]) == 0:
			continue

		if not (n[1]["rTag"][0] == "r" and n[1]["rTag"][1:].isdigit()):
			continue

		for nn in tempG.nodes(data=True):
			if n[0] == nn[0]:
				continue

			if nn[1]["label"].count(", ") < 2:
				continue

			if n[1]["rTag"][0] == "r" and n[1]["rTag"][1:].isdigit():
				nth_index = findnth(nn[1]["label"], ", ", 2)
				if n[1]["rTag"]+", " in nn[1]["label"][nth_index:] or n[1]["rTag"]+")" in nn[1]["label"][nth_index:]:
					if nn[1]["nType"] == "statement-list" or nn[1]["nType"] == "if-statement" or nn[1]["nType"] == "case-statement" or nn[1]["nType"] == "case-element" or nn[1]["nType"] == "for-statement":
						# we don't need to link statement-list blocks
						# they are covered with sequential edges
						if not nn[1]["nType"] == "statement-list":
							# add_edge(G, nn[0], n[0], "ctrl")
							if nn[1]["nType"] == "if-statement":
								add_edge(G, n[0], nn[0], "ctrl")
							else:
								add_edge(G, nn[0], n[0], "ctrl")
							
							# if nn[1]["nType"] == "if-statement":
							# 	if nn[1]["label"].split(", ")[1][0] == "r" and nn[1]["label"].split(", ")[1][1:].isdigit():
							# 		if nn[1]["label"].split(", ")[2][0] == "r" and nn[1]["label"].split(", ")[2][1:].isdigit():
							# 			if_cond_rTag = nn[1]["label"].split(", ")[2]
							# 			if_cond_nName = None
							# 			if n[1]["rTag"] == if_cond_rTag:
							# 				add_edge(G, nn[0], n[0], "ctrl")
							# 			else:
							# 				if not if_cond_rTag in if_cond_mapping.keys():
							# 					for nnn in G.nodes(data=True):
							# 						if nnn[1]["rTag"] == if_cond_rTag:
							# 							if_cond_mapping[if_cond_rTag] = nnn[0]
							# 							if_cond_nName = nnn[0]
							# 							break
							# 				else:
							# 					if_cond_nName = if_cond_mapping[if_cond_rTag]
		
							# 				if not if_cond_nName == None:
							# 					add_edge(G, if_cond_nName, n[0], "ctrl")
							# 				else:
							# 					print("$$$$$$$$$$")
							# 					print(n[1])
							# 					print(nn[1])
							# 					print("ISSUE1!")
							# 					sys.exit()
							# 		else:
							# 			# this to handle  if-statements with direct bool vars
							# 			add_edge(G, nn[0], n[0], "ctrl")
							# 	else:
							# 		# this to handle ", t, " if-statements
							# 		add_edge(G, nn[0], n[0], "ctrl")
							# else:
							# 	add_edge(G, nn[0], n[0], "ctrl")
					else:
						if not n[1]["nType"] == "IVAR":
							add_edge(G, n[0], nn[0], "ctrl")
							if not nn[0] in toPrependNode.keys():
								toPrependNode[nn[0]] = []
							toPrependNode[nn[0]].append(n[0])
						else:
							if nn[0] in latestIVARAdded.keys():
								add_edge(G, n[0], latestIVARAdded[nn[0]], "ctrl")
								latestIVARAdded[nn[0]] = n[0]
							else:
								add_edge(G, n[0], nn[0], "ctrl")
								latestIVARAdded[nn[0]] = n[0]

				if n[1]["rTag"] in specialEdges.keys():
					for e in specialEdges[n[1]["rTag"]]:
						if e == nn[1]["rTag"]:
							add_edge(G, n[0], nn[0], "ctrl")
							print("^^^^^^^^^^^^")
							print(n[1]["label"])
							print(nn[1]["label"])
							break
	
	'''
	while True:
		# attach to entry related descendents
		tempG = nx.MultiDiGraph(name="tempG", data=True, align='vertical')
		tempG.add_nodes_from(G.nodes(data=True))
		tempG.add_edges_from(G.edges(data=True))
		toRemoveEdge = []

		for n in tempG.nodes(data=True):
			if n[0] == entryNode:
				continue
				
			isOrphanNode = len(tempG.in_edges.data(nbunch=n[0])) == 0
			if isOrphanNode:
				foundOrphan = True

				added_edge = False
				for d in nx.descendants(tempG, n[0]):
					isDescEntryReachable = nx.has_path(tempG, entryNode, d)
					if isDescEntryReachable:
						for (u, v, c) in tempG.in_edges.data(nbunch=d):
							if u == entryNode: # and n[0] in nx.descendants(G, entryNode)
								continue
	
							isDescEntryReachable = nx.has_path(tempG, entryNode, u) and not u in nx.descendants(tempG, n[0])
							if isDescEntryReachable:
								if G.has_edge(u, d):
									G.remove_edge(u, d)
									add_edge(G, u, n[0], "ctrl")
									added_edge = True
									break
						if added_edge:
							break

		# check if some nodes have no Entry related descednets except the exit node
		tempG = nx.MultiDiGraph(name="tempG", data=True, align='vertical')
		tempG.add_nodes_from(G.nodes(data=True))
		tempG.add_edges_from(G.edges(data=True))
		toRemoveEdge = []
	
		target_node = None
		for exitP in tempG.in_edges.data(nbunch=exitNode):
			if not exitP[0] == entryNode:
				target_node = exitP[0]
				# print("ssss")
				# print(target_node)
				# print(tempG.nodes(data=True)[exitP[0]])
				# sys.exit()
				break
	
		target_orphan = None
		for n in tempG.nodes(data=True):
			if n[0] == entryNode:
				continue
				
			isOrphanNode = len(tempG.in_edges.data(nbunch=n[0])) == 0
			if isOrphanNode:
				foundOrphan = True
	
				if target_orphan == None:
					target_orphan = n[0]
				elif not (n[1]["rTag"][0] == "r" and n[1]["rTag"][1:].isdigit()) and len(n[1]["rTag	"]) > 0:
					target_orphan = n[0]
				else:
					# if paraList[1][0] == "r" and paraList[1][1:].isdigit():
					node_rtag = tempG.nodes(data=True)[target_orphan]["rTag"]
					if node_rtag[0] == "r" and node_rtag[1:].isdigit():
						if n[1]["rTag"][0] == "r" and n[1]["rTag"][1:].isdigit():
							if int(n[1]["rTag"][1:]) < int(node_rtag[1:]):
								target_orphan = n[0]
	
		if not target_node == None and not target_orphan == None:
			if G.has_edge(target_node, exitNode):
				G.remove_edge(target_node, exitNode)
				add_edge(G, target_node, target_orphan, "ctrl")

		foundOrphan = False
		for n in G.nodes(data=True):
			if n[0] == entryNode:
				continue
				
			isOrphanNode = len(G.in_edges.data(nbunch=n[0])) == 0
			if isOrphanNode:
				foundOrphan = True
				break
		if not foundOrphan:
			break
	'''

	for n in G.nodes(data=True):
		if n[0] == exitNode:
			continue
		if len(G.out_edges.data(nbunch=n[0])) == 0:
			add_edge(G, n[0], exitNode, "ctrl")

	return G, entryNode, exitNode

def fixSDG(SDG, declFunctions, funcDeclVars):
	specialEdges = {}

	for n in SDG.nodes(data=True):
		elements = []

		if not "label" in n[1].keys():
			continue

		if len(n[1]["rTag"]) == 0:
			continue

		if not (n[1]["rTag"][0] == "r" and n[1]["rTag"][1:].isdigit()):
			continue

		if not (n[1]["nType"] == "statement-list" or n[1]["nType"] == "if-statement" or n[1]["nType"] == "case-statement" or n[1]["nType"] == "case-element") or n[1]["nType"] == "for-statement":
			continue

		if n[1]["nType"] == "statement-list":
			nth_index = findnth(n[1]["label"], ", ", 2)
			elements = n[1]["label"][nth_index:-1].split(", ")

		if n[1]["nType"] == "if-statement" or n[1]["nType"] == "case-statement" or n[1]["nType"] == "case-element" or n[1]["nType"] == "for-statement":
			nth_index = findnth(n[1]["label"], ", ", 3)
			elements = n[1]["label"][nth_index:-1].split(", ")
			# print(n[1]["label"])
			# print(n[1]["label"][nth_index:-1])
			# print(elements)
			# sys.exit()

		for e in elements:
			if len(e) == 0:
				continue

			for nn in SDG.nodes(data=True):
				if n[0] == nn[0]:
					continue
				
				if not "label" in nn[1].keys():
					continue

				if nn[1]["label"].count(", ") < 2:
					continue
				
				if len(nn[1]["rTag"]) == 0 or " : " in nn[1]["rTag"]:
					continue

				# if nn[1]["rTag"][0] == "r" and nn[1]["rTag"][1:].isdigit():
				# 	nnth_index = findnth(nn[1]["label"], ", ", 2)
				# 	if e+", " in nn[1]["label"][nnth_index:] or e+")" in nn[1]["label"][nnth_index:]:
				# 		add_edge(SDG, n[0], nn[0], "ctrl")
				# 		break

				if nn[1]["rTag"][0] == "r" and nn[1]["rTag"][1:].isdigit():
					if e == nn[1]["rTag"]:
						add_edge(SDG, n[0], nn[0], "ctrl")
						break
	
	# tempG = nx.MultiDiGraph(name="tempG", data=True, align='vertical')
	# tempG.add_nodes_from(G.nodes(data=True))
	# tempG.add_edges_from(G.edges(data=True))
	# toPrependNode = {}
	# toPostpendNode = {}
	# latestIVARAdded = {}

	return SDG

def getNonExitReachableNodes(G, entryNode, exitNode):
	nonExitReachableNodes = []

	for n in G.nodes(data=True):
	 	nName = n[0]
	 	if not nName.startswith("EXIT_"):
	 		paths = nx.all_simple_paths(G, nName, exitNode)
	 		isExitReachable = False
	 		for path in paths:
	 			isExitReachable = True
	 			break
				
	 		if not isExitReachable:
	 			nonExitReachableNodes.append(nName)

	return nonExitReachableNodes

def constructCDG(G, entryNode, exitNode):
	nonExitReachableNodes = getNonExitReachableNodes(G, entryNode, exitNode)
	for n in nonExitReachableNodes:
		add_edge(G, n, exitNode, "ctrl")

	CFGRev = G.reverse()
	pDomFrontiers = nx.dominance_frontiers(CFGRev, exitNode)
	pList = list(pDomFrontiers.keys())
	CDG = nx.MultiDiGraph(name=str(G).replace("fSDG", "CDG"), data=True, align='vertical')
	CDG.add_nodes_from(G.nodes(data=True))

	for p in pList:
		pdfList = list(pDomFrontiers[p])
		for pdf in pdfList:
			add_edge(CDG, pdf, p, "ctrl")

	return CDG

def isDefinition(G, nodeName, varName):
	ndataName = G.nodes(data=True)[nodeName]["dataName"]
	nType = G.nodes(data=True)[nodeName]["nType"]

	if ndataName == varName and "decl" in nType:
		return True
	return False


def isReachingDefinition(G, defStmt, useStmt, varName):
	paths = nx.all_simple_paths(G, defStmt, useStmt)
	foundReachingDefinition = False

	for path in paths:
		for n in path[1:]:
			if isDefinition(G, n, varName):
				break
			if n == useStmt:
				foundReachingDefinition = True
		if foundReachingDefinition:
			break

	return foundReachingDefinition

def getDirectVarQ(DDG):
	directVarQ = {}

	for n in DDG.nodes(data=True):
		nIndex = n[0]
		nContent = n[1]
		ndataName = nContent["dataName"]
		nType = nContent["nType"]
		nSubType = nContent["nSubType"]
		nValue = nContent["nValue"]
		nregionName = nContent["regionName"]

		if nType == "direct-variable":
			if nSubType == "Q" or nSubType == "M":
				for nn in DDG.nodes(data=True):
					nnIndex = nn[0]
					nnContent = nn[1]
					nndataName = nnContent["dataName"]
					nnType = nnContent["nType"]
					nnSubType = nnContent["nSubType"]
					nnValue = nnContent["nValue"]
					nnregionName = nnContent["regionName"]

					if nIndex == nnIndex:
						continue

					if ndataName in nnValue:
						if not nndataName in list(directVarQ.keys()):
							directVarQ[nndataName] = ndataName

					if nndataName in list(directVarQ.keys()):
						if not directVarQ[nndataName] in DDG.nodes[nnIndex]["nValue"]:
							DDG.nodes[nnIndex]["nValue"].append(directVarQ[nndataName])

	return directVarQ

'''
using the feedback concept the process variable (PV) is regulated according to the difference between its current value and the value
of the set point (SP) (i.e. what it should be). The output is the action required on the system
to keep the regulation.

The PID calculation is achieved by a method of sampling; Ts specifies the minimum sample period.
If Ts is less than the application scan time, the effective sample interval will be the application scan time.
The maximum effective sample period is Ts plus the application scan time. The outputs are recalculated
only if a new sample is made.

The input Auto determines whether the function block is to operate in AUTO or MANUAL mode:

AUTO Mode Operation
==================

If a new sample is made and Auto = TRUE, the output Xout is calculated as follows:

Xout = Kp * ( E[t] + I[t]/Ti + D[t] * Td)

where

E[t] = SP - PV (error)
I[t] = I[t-1] + ( E[t] * T ) (integral term)
D[t] = ( E[t] - E[t-1] ) / T (derivative term)

E[t-1] is the stored error value (i.e. value on last sample)
I[t-1] is the stored integral term (i.e. value on last sample)
T is the elapsed time in milliseconds since the last sample

On initialisation (i.e. first application program scan), the stored integral term is set to zero, and the
action is calculated using proportional action only (i.e. Xout = Kp * E[t]).

If Ti = 0, the stored integral term is set to zero and Xout is calculated using proportional and derivative
action only (i.e. Xout = Kp * (E[t] + D[t] * Td) ).

Once Xout has been calculated, the increment stop (INCstop), decrement stop (DECstop) and the clamp
(Xmax and Xmin) are applied. If INCstop = TRUE and Xout has increased since the last sample or if
DECstop = TRUE and Xout has decreased since the last sample, Xout is set to its previous value. If
Xout > Xmax or Xout < Xmin, Xout is clamped to the range Xmin to Xmax, LIMIThi is set to Xout > Xmax,
and LIMITlo to Xout < Xmin.

If INCstop, DECstop or the clamp are active, the previous integral term is retained (i.e. the stored
integral term is not set to the current integral term). On initialisation, INCstop and DECstop have no
effect.

MANUAL mode operation
====================

If a new sample is made and Auto = FALSE, the output Xout immediately follows the adjustment
value (XO) clamped to the range Xmin to Xmax. LIMIThi is set to XO > Xmax and LIMITlo to XO < Xmin.
The stored error term is set to (SP - PV) and the stored integral term is set to zero. The increment
and decrement stop (INCstop and DECstop) have no effect.

Parameter Summary
=================

Parameter Type Description
--- --- ---
Auto BOOLEAN TRUE for AUTO mode, FALSE for MANUAL mode
PV REAL Process variable
SP REAL Set point
XO REAL Adjustment value (in MANUAL mode, Xout = XO)
Kp REAL Proportionality constant
Ti TIMER Integral time constant
Td TIMER Derivative time constant
Ts TIMER Sampling period
Xmax REAL Maximum value of Xout
Xmin REAL Minimum value of Xout
INCstop REAL Increment stop
DECstop REAL Decrement stop
Xout REAL PID_II function output
LIMIThi REAL TRUE if Xout is clamped at its maximum value (Xmax)
LIMITlo REAL TRUE if Xout is clamped at its minimum value (Xmin)

N.B. Parameters PV, SP, XO, Kp, Xmax, and Xmin must be finite (i.e. not +/- infinities or NaNs).


call: PV, SP, XO, Kp, Xmax, Xmin (REAL); Auto, INCstop, DECstop (BOOLEAN); Ts, Ti, Td (TIMER)
return: Xout (REAL); LIMIThi, LIMITlo (BOOLEAN)

prototype: PID_II(PV, SP, Auto, XO, Kp, Ti, Td, Ts, Xmax, Xmin, INCstop, DECstop);
Xout := PID_II.Xout;
LIMIThi := PID_II.LIMIThi;
LIMITlo := PID_II.LIMITlo;

notes:

Loss of precision and underflow may occur.

Due to the limitations of ISaGRAF TIMER data type, Ti, Td and Ts cannot have a value of 24 hours or greater.

If Xmax < Xmin, the function assumes that the values have been reversed and 'swaps' the
values. The 'Reversed' error counter is incremented for every application program scan that the
values are reversed.

Either the following behaviour will occur *TBD*:

EITHER:

If overflow occurs during the execution of the function, the stored integral and error terms are set to
zero. In AUTO mode, if SP > PV, Xout is set to Xmax, LIMIThi to TRUE and LIMITlo to FALSE. If
SP < PV, Xout is set to Xmin, LIMIThi to FALSE and LIMITlo to TRUE. In MANUAL mode Xout is set
to XO clamped to the range Xmin to Xmax, LIMIThi is set to XO > Xmax and LIMITlo is set to XO < Xmin.

OR:

If overflow occurs during the execution of the function, the stored integral and error terms are set to
zero. In AUTO mode, Xout is set to zero, and LIMIThi and LIMITlo to FALSE. In MANUAL mode, Xout is
set to XO clamped to the range Xmin to Xmax, LIMIThi is set to XO > Xmax and LIMITlo is set to XO < Xmin.
'''

def constructDDG(G, entryNode, exitNode):
	DDG = nx.MultiDiGraph(name=str(G).replace("fSDG", "DDG"), data=True, align='vertical')
	DDG.add_nodes_from(G.nodes(data=True))

	# directVarQ = getDirectVarQ(DDG)

	for n in DDG.nodes(data=True):
		nIndex = n[0]
		nContent = n[1]
		# print("*2*")
		# print(nIndex)
		# print(nContent)
		# if nIndex == "ENTRY_R_TRIG" or nIndex == "ENTRY_TOF_TIME" or nIndex == "ENTRY_F_TRIG":
		# 	continue
		ndataName = nContent["dataName"]
		nType = nContent["nType"]
		nSubType = nContent["nSubType"]
		nValue = nContent["nValue"]
		nregionName = nContent["regionName"]

		# if "r220147" in nValue:
		# 	print("!!!!!!!!!!")
		# 	# print(n.regionName)
		# 	# print(n.nodeValue)
		# 	sys.exit()

		if nType == "fb-invocation":
			continue

		for nn in DDG.nodes(data=True):
			nnIndex = nn[0]
			nnContent = nn[1]
			# print("*1*")
			# print(nnIndex)
			# print(nnContent)
			# if nnIndex == "ENTRY_R_TRIG" or nnIndex == "ENTRY_TOF_TIME" or nnIndex == "ENTRY_F_TRIG":
			# 	continue

			nndataName = nnContent["dataName"]
			nnType = nnContent["nType"]
			nnSubType = nnContent["nSubType"]
			nnValue = nnContent["nValue"]
			nnregionName = nnContent["regionName"]
			# if nSubType == "multi-element-variable" and nnType == "actualOut":
			# 	if nndataName in nValue:
			# 		print("**")
			# 		# print(nValue)
			# 		print(nn)
			# 		print("&&")
			# 		print(n)
			if nnType == "fb-invocation":
				# print(nnValue)
				# print(nnContent["label"])
				if len(nnValue) == 0:
					continue
				tempNnValue = [nnValue[0]]
				for i in range(2, len(nnValue), 2):
					tempNnValue.append(nnValue[i])
				nnValue = tempNnValue
				# print(nnValue)
				# print(nnContent["label"])
				# None

			if nIndex == nnIndex:
				continue

			if ndataName in nnValue:
				# if ndataName == "pressure" and nregionName == "main" and nnregionName == "main":
				# 	paths = nx.all_simple_paths(G, nIndex, nnIndex)
				# 	for p in paths:
				# 		print("nIndex: " + str(nIndex) + ", nnIndex: " + str(nnIndex) + ", ndataName: " + str(ndataName) + ", nndataName: " + str(nndataName))
				# 		break

				# if True:
				if isReachingDefinition(G, nIndex, nnIndex, ndataName):
					# add_edge(DDG, nIndex, nnIndex, "data")

					# if ndataName == "pressure" and nregionName == "main" and nnregionName == "main":
					# 	print("nIndex: " + str(nIndex) + ", nnIndex: " + str(nnIndex) + ", ndataName: " + str(ndataName) + ", nndataName: " + str(nndataName))

					if nType == "direct-variable" and nSubType == "Q":
						# nTuple = tuple(nContent["label"][1:-1].split(", "))
						# nTupleSize = len(nTuple)
						# if nTupleSize == 8:
						# 	nSubType = nTuple[3]
						# 	nValue = [str(nTuple[3]+nTuple[5]+nTuple[7])]

						# print(nSubType)
						
						if nnType == "ASSIGNMENT":
							# if DDG.nodes(data=True)[nnIndex]["dataName"] == "f1_valve_sp":
							# 	print(DDG.nodes(data=True)[nIndex])
							# 	print(DDG.nodes(data=True)[nnIndex])
							# 	print("----")
							mIndex = ""
							for m in DDG.nodes(data=True):
								if nndataName == m[1]["dataName"] and nnregionName == m[1]["regionName"] and "decl" in m[1]["nType"]:
									mIndex = m[0]
									# break
							add_edge(DDG, nnIndex, mIndex, "data")
						else:
							add_edge(DDG, nnIndex, nIndex, "data")
					else:
						if nType == "direct-variable" and nSubType == "M":
							if nnType == "ASSIGNMENT":
								add_edge(DDG, nnIndex, nIndex, "data")
							else:
								add_edge(DDG, nIndex, nnIndex, "data")
						else:
							# if nnType == "ASSIGNMENT":
							# 	mIndex = ""
							# 	for m in DDG.nodes(data=True):
							# 		if nndataName == m[1]["dataName"] and nnregionName == m[1]["regionName"] and "decl" in m[1]["nType"]:
							# 			mIndex = m[0]
							# 			break
							# 	add_edge(DDG, mIndex, nnIndex, "data")
							# else:
							# 	add_edge(DDG, nIndex, nnIndex, "data")
							add_edge(DDG, nIndex, nnIndex, "data")
							
							# if nType == "ASSIGNMENT" or nnType == "ASSIGNMENT":
							# 	if DDG.nodes(data=True)[nIndex]["dataName"] == "f1_valve_sp" or DDG.nodes(data=True)[nnIndex]["dataName"] == "f1_valve_sp":
							# 		print(DDG.nodes(data=True)[nIndex])
							# 		print(DDG.nodes(data=True)[nnIndex])
							# 		print("----")
				else:
					# nndataName == "formalInPara_"+ndataName or 
					# this is important for formalOutPara, they don't show up on CFG
					if nndataName == "formalOutPara_"+nregionName+"_"+ndataName: 
						# add_edge(DDG, nIndex, nnIndex, "data")
						if nType == "ASSIGNMENT":
							mIndex = ""
							for m in DDG.nodes(data=True):
								if ndataName == m[1]["dataName"] and nnregionName == m[1]["regionName"] and "decl" in m[1]["nType"]:
									mIndex = m[0]
									break

							add_edge(DDG, nIndex, mIndex, "data")
						else:
							add_edge(DDG, nIndex, nnIndex, "data")
					elif nType == "actualOut": #  or nType == "formalOut"
						if ndataName in nnValue: #  or nndataName == "formalOutPara_"+ndataName
							# print(nn)
							add_edge(DDG, nIndex, nnIndex, "data")
					# if nndataName == "formalOutPara_"+ndataName: 
					# 	add_edge(DDG, nIndex, nnIndex, "data")
					# if nndataName in nValue:
					# 	add_edge(DDG, nIndex, nnIndex, "data")
			elif nregionName == "PID" and nnregionName == "PID":
				if nType == "input-declarations" and nnType == "output-declarations":
					# if DDG.nodes(data=True)[nnIndex]["dataName"] == "new_pos":
					# print(DDG.nodes(data=True)[nIndex])
					# print(DDG.nodes(data=True)[nnIndex])
					# print("----")
					# 	mIndex = ""
					# 	for m in DDG.nodes(data=True):
					# 		if nndataName == m[1]["dataName"] and nnregionName == m[1]["regionName"] and "decl" in m[1]["nType"]:
					# 			mIndex = m[0]
					# 			break
					# 	add_edge(DDG, mIndex, nnIndex, "data")
					# else:
					# 	add_edge(DDG, nIndex, nnIndex, "data")
					add_edge(DDG, nIndex, nnIndex, "data")
					
		firstNnScan = False
	# print(len(DDG.edges()))
	# print("----")
	return DDG

	
def constructPDG(CDG, DDG):
	PDG = nx.MultiDiGraph(name=str(CDG).replace("CDG", "PDG"), data=True, align='vertical')
	PDG.add_nodes_from(CDG.nodes(data=True))
	PDG.add_edges_from(CDG.edges(data=True))
	PDG.add_edges_from(DDG.edges(data=True))

	return PDG

def scanFunctionsVars(keysList, startEndRegions):
	global IRlines, funcDeclVars, declFunctions

	declFunctions = []
	funcDeclVars = {}
	funcDeclVars["global"] = {}

	i = 0
	for k in keysList:
		rStart = k
		rEnd = startEndRegions[k]
		firstLine = IRlines[k]

		lineTuple = tuple(firstLine[1:-1].split(", "))
		regionType = lineTuple[0]
		regionName = lineTuple[1]

		if regionType == "DATA_BLOCK":
			if regionName.endswith("_DB"):
				continue


		if not (firstLine.startswith("(FUNC, ") or firstLine.startswith("(PROG, ") or firstLine.startswith("(DATA_BLOCK, ") or firstLine.startswith("(structure-type-name, ") or firstLine.startswith("(DIRECT_VARS, ")): # 
			continue
		
		if not regionName in declFunctions:
			if regionType == "FUNC" or regionType == "PROG":
				declFunctions.append(regionName)
				funcDeclVars[regionName] = {}

		regionlines = IRlines[rStart:rEnd]

		for line in regionlines:
			n = parseLine(line, regionType, regionName)
			if "-declarations" in n.nodeType or regionType == "structure-type-name" or regionType == "DATA_BLOCK" or regionType == "DIRECT_VARS":
				# print("regionName: " + regionName + ", n.dataName: " + n.dataName + ", [n.nodeType, n.nSubType]: " + str([n.nodeType, n.nSubType]))

				# if regionType == "DATA_BLOCK" and n.nodeType == "ASSIGNMENT":
				# 	print("#############")
				# 	print(regionName)
				# 	print(line)
				# 	None
				if "-declarations" in n.nodeType and not regionType == "DIRECT_VARS":
					funcDeclVars[regionName][n.dataName] = [n.nodeType, n.nSubType]
					# if "lfb_horizontal_Axis" in n.dataName:
					# 	print("$$")
					# 	print(n.dataName)
					# 	print(funcDeclVars[regionName][n.dataName])
					# 	None
				elif regionType == "DATA_BLOCK":
					# if len(regionlines) > 1:
						# print(regionlines)
						# None
						# print(n.nodeType)
					if n.nodeType == "DATA_BLOCK":
						funcDeclVars["global"][regionName] = [n.nodeType, n.nSubType]
						if len(n.nodeValue) > 0:
							if " : " in n.nodeValue[0]:
								funcDeclVars["global"][regionName].append(n.nodeValue)
								# print(n.nodeValue)
								# None
						# print("*************************")
						# print(regionName)
						# print(funcDeclVars["global"][regionName])
					else:
						# print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
						# print(n.nodeValue)
						# print(n.dataName)
						funcDeclVars["global"][regionName].append([n.dataName, n.nodeValue])
						# print(regionName)
						# print(funcDeclVars["global"][regionName])
						# None
				elif regionType == "structure-type-name":
					if n.nodeType == "structure-type-name":
						funcDeclVars["global"][regionName] = []
					if n.nodeType == "structure-element-declaration":
						funcDeclVars["global"][regionName].append([n.nodeType, n.dataName, n.nSubType])
				elif regionType == "DIRECT_VARS":
					if not "DIRECT_VARS" in funcDeclVars["global"].keys():
						# funcDeclVars["global"]["DIRECT_VARS"] = ["DIRECT_VARS", "DIRECT_VARS"]
						funcDeclVars["global"]["DIRECT_VARS"] = ["DIRECT_VARS"]
					if not n.nodeType == "DIRECT_VARS":
						# funcDeclVars["global"]["DIRECT_VARS"].append([n.dataName, n.nodeValue])
						funcDeclVars["global"]["DIRECT_VARS"].append(n)

			# elif "DATA_BLOCK" in n.nodeType:
			# 	# print("regionName: " + regionName + ", n.dataName: " + n.dataName + ", [n.nodeType, n.nSubType]: " + str([n.nodeType, n.nSubType]))
			# 	funcDeclVars[regionName][n.dataName] = [n.nodeType, n.nSubType]
			# 	# None
	
	# print(declFunctions)
	# print(funcDeclVars)
	# None
	return declFunctions, funcDeclVars

def constructSDG(G, entryNode, exitNode, declFunctions, funcDeclVars):
	tempG = nx.MultiDiGraph(name="PLCprog-SDG", data=True, align='vertical')
	tempG.add_nodes_from(G.nodes(data=True))
	tempG.add_edges_from(G.edges(data=True))

	for n in tempG.nodes(data=True):
		nName = n[0]
		regionType = n[1]["regionType"]
		regionName = n[1]["regionName"]
		dataName = n[1]["dataName"]

		if n[1]["nType"] == "fb-invocation":
			# print("regionName: " + regionName + ", dataName: " + dataName)
			calleeFunc = funcDeclVars[regionName][dataName][1]
			add_edge(G, nName, "ENTRY_"+calleeFunc, "interp-ctrl")
			# exit()

		# if n[1]["nType"] == "formalIn":
		# 	print(n)
		# 	exit()

		if n[1]["nType"] == "actualIn":
			calleeFunc = n[1]["nSubType"]
			paraName = n[1]["dataName"]
			# formalInPara = "formalInPara_2_" + calleeFunc + "_" + paraName
			formalInPara = "formalInPara_" + calleeFunc + "_" + paraName
			# if formalInPara == "formalInPara_TON_TIME_Q":
			# 	print("AAAAAA")
			# 	print(formalInPara)
			# 	sys.exit()
			add_edge(G, nName, formalInPara, "interp-data") # interp-data1
			# FOUNDPARA = False
			# for nn in G.nodes(data=True):
			# 	nnIndex = nn[0]
			# 	nnContent = nn[1]
			# 	nndataName = nnContent["dataName"]
			# 	nnType = nnContent["nType"]
			# 	nnSubType = nnContent["nSubType"]
			# 	nnValue = nnContent["nValue"]
			# 	if nnType == "formalIn":
			# 		if formalInPara == nnIndex:
			# 			FOUNDPARA = True
			# 			print(nn)
			# 			break
			# if not FOUNDPARA:
			# 	print("NOT FOUND")
			# 	print(formalInPara)
			# exit()

		if n[1]["nType"] == "actualOut":
			calleeFunc = n[1]["nSubType"][1]
			paraName = n[1]["nSubType"][2]
			formalOutPara = "formalOutPara_" + calleeFunc + "_" + paraName
			add_edge(G, formalOutPara, nName, "interp-data")

def isActualOutParaRef(n, declFunctions, funcDeclVars):
	# print(n[1]["label"])
	# print(n[1])
	nName = n[0]
	regionType = n[1]["regionType"]
	regionName = n[1]["regionName"]
	dataName = n[1]["dataName"]
	nValue = n[1]["nValue"]

	interpPtrList = []
	for i in range(0, len(nValue)):
		if not "@" in nValue[i]:
			continue

		ptr = nValue[i].split("@")[0]
		# field = nValue[i].split("@")[1]
		field = nValue[i][nValue[i].find("@")+1:]
		# print(regionName)
		# print(ptr)
		# print(field)
		# print(nValue[i])
		# print(nValue)
		if ptr == "date-and-time":
			continue
		ptrType = ""
		ptrSubtype = ""

		# if call to another function
		if ptr in funcDeclVars[regionName].keys():
			ptrType = funcDeclVars[regionName][ptr][0]
			ptrSubtype = funcDeclVars[regionName][ptr][1]
			if (not (ptrSubtype == regionName)) and (ptrSubtype in declFunctions): #  and (ptrSubtype in declFunctions)
				# if "lfb_horizontal_Axis@outx_Motor_Pos" in nValue[i]:
					# print("!!!!")
					# print(nValue[i])
					# print(n[0])
					# print(n[1])
					# None

				# print("&&&")
				# print(ptrSubtype)
				# print(field)
				# print(funcDeclVars[ptrSubtype])
				valueType = funcDeclVars[ptrSubtype][field][0]
				valueSubtype = funcDeclVars[ptrSubtype][field][1]
				interpPtrList.append([nName, regionName, ptr, ptrSubtype, field, valueSubtype])
		else:
			# regionName = "global"
			nName = nValue[i]

			if ptr in funcDeclVars["global"].keys():
				ptrType = funcDeclVars["global"][ptr][0]
				ptrSubtype = funcDeclVars["global"][ptr][1]
				if ptrSubtype in funcDeclVars["global"].keys():
					interpPtrList.append([nName, "global", ptr, ptrSubtype, field, "valueSubtype"])

	if len(interpPtrList) > 0:			
		# print(interpPtrList)
		# None
		return True, interpPtrList

	return False, []

	'''
	ptr = nValue[0].split("@")[0]
	field = nValue[0].split("@")[1]
	ptrType = funcDeclVars[regionName][ptr][0]
	ptrSubtype = funcDeclVars[regionName][ptr][1]

	# print("**")
	# print(ptrType)
	# print(regionName)
	if (not (ptrSubtype == regionName)) and (ptrSubtype in declFunctions):
		valueType = funcDeclVars[ptrSubtype][field][0]
		valueSubtype = funcDeclVars[ptrSubtype][field][1]
		# return True, ptr, [nName, regionName, field, ptrType, ptrSubtype, valueType, valueSubtype]
		interpPtrList = [nName, regionName, ptr, ptrSubtype, field, valueSubtype]

		return True, interpPtrList

	return False, []
	'''

# actualOut = "actualOutPara " + ptr + " " + calledFunction + " " + calledFunctionVar


def findActualOutParaRef(G, declFunctions, funcDeclVars):
	actualOutParaRef = []

	for n in G.nodes(data=True):
		nName = n[0]
		# print(G.nodes[nName])
		# if n[1]["nType"] == "IVAR" and n[1]["nSubType"] == "multi-element-variable":
		if "multi-element-variable" in n[1]["label"]:
			isActualOutPara, interpPtrList = isActualOutParaRef(n, declFunctions, funcDeclVars)
			
			if isActualOutPara:
				# None
				# G.nodes[nName]["nValue"] = []
				# print("@@@@")
				# print(interpPtrList)
				# print(len(interpPtrList))
				for i in range(0, len(interpPtrList)):
					# print("i = " + str(i))
					actualOutParaRef.append(interpPtrList[i])
					# add data ref
					ptrnName = interpPtrList[i][0]
					ptrRegion = interpPtrList[i][1]
					ptr = interpPtrList[i][2]
					calledFunction = interpPtrList[i][3]
					calledFunctionVar = interpPtrList[i][4]
					ptrField = interpPtrList[i][5]
					# n[1]["nValue"] = n[1]["nValue"] + ["actualOutPara " + ptr + " " + calledFunction + " " + calledFunctionVar]
					
					if ptrRegion == "global":
						if not ptrnName in G.nodes[nName]["nValue"]:
							G.nodes[nName]["nValue"].append(ptrnName)
						# print(G.nodes[nName]["nValue"])
						# print(G.nodes[nName]["label"])
						# print("&&")
						# None
					else:
						G.nodes[nName]["nValue"].append("actualOutPara " + "_" + n[1]["regionName"] + "_" + ptr + " " + calledFunction + " " + calledFunctionVar)
					
					# no # G.nodes[nName]["nValue"] = G.nodes[nName]["nValue"] + ["actualOutPara " + ptr + " " + calledFunction + " " + calledFunctionVar]
					# no # G.nodes[nName]["nValue"].append("actualOutPara " + "_" + n[1]["regionName"] + "_" + ptr+"@"+ptrField + " " + calledFunction + " " + calledFunctionVar)
					# print(G.nodes[nName])

	return actualOutParaRef


def constructFuncSDG(G, declFunctions, funcDeclVars):
	tempG = nx.MultiDiGraph(name="PLCprog-fSDG", data=True, align='vertical')
	tempG.add_nodes_from(G.nodes(data=True))
	tempG.add_edges_from(G.edges(data=True))

	
	for n in G.nodes(data=True):
		# print("n: " + str(n))
		# if n[1]["nType"] == "input-declarations":
		if "-declarations" in n[1]["nType"] and "input" in n[1]["nType"]:
			nName = n[0]
			regionType = n[1]["regionType"]
			regionName = n[1]["regionName"]
			dataName = n[1]["dataName"]
			rTag = n[1]["rTag"]
			nSubType = n[1]["nSubType"]
			formalInNode = "formalInPara_" + regionName + "_" + dataName
			entryNode = "ENTRY_" + regionName
			entryEdges = []
			# if formalInNode == "formalInPara_TON_TIME_lfb_ton":
			# 	print(n[1])
			# 	None

			# if "R_TRIG" in regionName or "stmt_6967" in :
			# 	print("!!!!2")
			# 	sys.exit()


			# if formalInNode == "formalInPara_R_TRIG_CLK":
			# 	print("!!!!")
			# 	sys.exit()

			# if formalInNode == "formalInPara_TON_TIME_Q":
			# if "TON_TIME" in formalInNode:
			# 	print("XXXX")
			# 	print(formalInNode)
			# 	sys.exit()

			add_node(tempG, formalInNode, "formalIn", formalInNode, dataName, [], formalInNode, 1, regionType, regionName, rTag)
			
			for e in tempG.edges(data=True):
				if e[0].startswith("ENTRY_"):
					if not e[1].startswith("EXIT_"):
						entryEdges.append(e)

			for e in entryEdges:
				tempG.remove_edge(e[0], e[1])
				add_edge(tempG, formalInNode, e[1], "ctrl")

			add_edge(tempG, entryNode, formalInNode, "ctrl")


		# if n[1]["nType"] == "output-declarations":
		if "-declarations" in n[1]["nType"] and "output" in n[1]["nType"]:
			nName = n[0]
			regionType = n[1]["regionType"]
			regionName = n[1]["regionName"]
			dataName = n[1]["dataName"]
			rTag = n[1]["rTag"]
			nSubType = n[1]["nSubType"]
			formalOutNode = "formalOutPara_" + regionName + "_" + dataName
			entryNode = "ENTRY_" + regionName
			entryEdges = []
			
			add_node(tempG, formalOutNode, "formalOut", formalOutNode, dataName, [dataName], formalOutNode, 1, regionType, regionName, rTag)
			
			for e in tempG.edges(data=True):
				if e[0].startswith("ENTRY_"):
					if not e[1].startswith("EXIT_"):
						entryEdges.append(e)

			for e in entryEdges:
				tempG.remove_edge(e[0], e[1])
				add_edge(tempG, formalOutNode, e[1], "ctrl")

			add_edge(tempG, entryNode, formalOutNode, "ctrl")

	# print(declFunctions)
	# print(funcDeclVars)

	actualOutParaRef = findActualOutParaRef(tempG, declFunctions, funcDeclVars)

	# if len(actualOutParaRef) > 0:
	# 	print(actualOutParaRef)

	for n in G.nodes(data=True):
		nName = n[0]
		regionType = n[1]["regionType"]
		regionName = n[1]["regionName"]
		rTag = n[1]["rTag"]
		if n[1]["nType"] == "fb-invocation":
			ptrName = n[1]["nSubType"]
			# print("regionName: " + regionName + ", ptrName: " + ptrName)
			# print("funcDeclVars[regionName]: " + str(funcDeclVars[regionName]))
			ptr2func = funcDeclVars[regionName][ptrName][1]
			paraList = n[1]["nValue"]

			# if ptr2func in declFunctions:
			# 	print("----------")
			# 	print(ptr2func)

			# 	if not ptr2func == "TON_TIME":
			# 		None

			if not ptr2func in declFunctions:
				continue
			# print("777")
			# print(paraList)
			# if paraList[1][0] == "r" and paraList[1][1:].isdigit():
			# 	None
			# print(paraList)
			# None
			for i in range(1, len(paraList), 2):
				actualIn = paraList[i+1]
				# formalIn = paraList[i-1]
				formalIn = paraList[i]
				actualInNode = paraList[i] + "_" + str(time.time())
				add_node(tempG, actualInNode, "actualIn", formalIn, ptr2func, [actualIn], "actualInPara " + formalIn + " = " + actualIn, 1, regionType, regionName, rTag)
				add_edge(tempG, nName, actualInNode, "ctrl")
				# add_edge(tempG, nName, actualInNode, "data")
				# print(actualInNode)

			# print(ptrName)
			# print(actualOutParaRef)
			for p in actualOutParaRef:
				if p[2] == n[1]["dataName"]:
					ptr = p[2]
					calledFunction = p[3]
					calledFunctionVar = p[4]
					actualOut = "actualOutPara " + "_" + n[1]["regionName"] + "_" + ptr + " " + calledFunction + " " + calledFunctionVar
					# actualOutNode = actualOut + "_" + str(time.time())
					# add_node(G, stmtName, nodeType, dataName, nSubType="", nodeValue="", nodeLine="", nodeLineSize=2, regionType="", regionName=""):
					add_node(tempG, actualOut, "actualOut", actualOut, [ptr, calledFunction, calledFunctionVar], [], actualOut, 1, regionType, regionName, rTag)
					add_edge(tempG, nName, actualOut, "ctrl")

	return tempG

# structs_gdb = []
# structs_gdb_tuples = []
# def findMoreGlobalDataNodesInStructs(SDG, declFunctions, funcDeclVars, valuedVars):
# 	global globalVars, globalDefinedDBs, structs_gdb, structs_gdb_tuples

# 	for e in funcDeclVars["global"][struct_name]:
# 		e_name = e[1]
# 		if not e_name in valuedVars:
# 			stmtName = k + "@" + e_name
# 			nodeType = "var-declarations"
# 			dataName = k + "@" + e_name
# 			nSubType = k
# 			nodeValue = ""
# 			line = ("(var-declarations, " + stmtName + ")")
# 			lineTupleSize = 2
# 			rTag = dataName
# 			if not globalVars in globalVars:
# 				structs_gdb.append(stmtName)
# 				gdb_tuple = (stmtName, nodeType, dataName, nSubType, nodeValue, line, lineTupleSize, regionType, regionName, rTag)
# 				structs_gdb_tuples.append(gdb_tuple)

missedGlobalVariables = []
def addMissedGlobalVariables(SDG, declFunctions, funcDeclVars):
	global globalVars, globalDefinedDBs, allglobalVarNames, missedGlobalVariables

	missedGlobalVarParameters = []
	regionType = "DATA_BLOCK"
	regionName = "global"

	for n in SDG.nodes(data=True):
		nIndex = n[0]
		nContent = n[1]

		if len(nContent) == 0 or not "nValue" in nContent.keys():
			continue

		nValue = nContent["nValue"]
		if len(nValue) == 0:
			continue

		for e in nValue:
			if "@" in e:
				v = e[:e.find("@")]

				if v in allglobalVarNames:
					if not e in globalVars and not e in missedGlobalVariables:
						stmtName = e
						nodeType = "var-declarations"
						dataName = e
						nSubType = v
						nodeValue = ""
						line = ("(var-declarations, " + stmtName + ")")
						lineTupleSize = 2
						rTag = dataName

						globalVars.append(e)
						missedGlobalVariables.append(e)
						missedGlobalVarParameters.append((stmtName, nodeType, dataName, nSubType, nodeValue, line, lineTupleSize, regionType, regionName, rTag))
						
	
	for i in range(0, len(missedGlobalVariables)):
		stmtName = missedGlobalVariables[i][0]
		nodeType = missedGlobalVariables[i][1]
		dataName = missedGlobalVariables[i][2]
		nSubType = missedGlobalVariables[i][3]
		nodeValue = missedGlobalVariables[i][4]
		line = missedGlobalVariables[i][5]
		lineTupleSize = missedGlobalVariables[i][6]
		regionType = missedGlobalVariables[i][7]
		regionName = missedGlobalVariables[i][8]
		rTag = missedGlobalVariables[i][9]

		add_node(SDG, stmtName, nodeType, dataName, nSubType, nodeValue, line, lineTupleSize, regionType, regionName, rTag)

	return SDG

globalVars = []
allglobalVarNames = [] # used for missed names!
globalDefinedDBs = {}
def constructGlobalDataNodes(SDG, declFunctions, funcDeclVars):
	global globalVars, globalDefinedDBs, allglobalVarNames

	for k in funcDeclVars["global"].keys():
		# print(k)
		# print(funcDeclVars["global"][k])
		if isinstance(funcDeclVars["global"][k][0], list):
			print("STRUCT")
		elif isinstance(funcDeclVars["global"][k][0], str) and funcDeclVars["global"][k][0] == "DIRECT_VARS":
			print("DIRECT_VARS")
			# None
			regionType = "DIRECT_VARS" # "FUNC" 
			regionName = "global"
			if len(funcDeclVars["global"]["DIRECT_VARS"]) >= 2:
				print(funcDeclVars["global"]["DIRECT_VARS"][1:])
				valuedVars = []
				for n in funcDeclVars["global"]["DIRECT_VARS"][1:]:
					# print(n)
					valuedVars.append(n.dataName) # valuedVars.append(n[0])
					stmtName = n.dataName # n[0]
					nodeType = "var-declarations"
					dataName = n.dataName
					nSubType = "direct-var"
					nodeValue = n.nodeValue
					line = n.label
					if "(direct-variable," in line:
						nSubType += "-def"
					else:
						nSubType += "-use"
					lineTupleSize = n.lineTupleSize
					rTag = ""
					if not stmtName in globalVars:
						globalVars.append(stmtName)
					print("*- stmtName: " + stmtName + ", nodeValue: " + str(nodeValue) + ", dataName: " + str(dataName))
					add_node(SDG, stmtName, nodeType, dataName, nSubType, nodeValue, line, lineTupleSize, regionType, regionName, rTag)

		elif isinstance(funcDeclVars["global"][k][0], str) and not funcDeclVars["global"][k][0] == "DIRECT_VARS":
			print("DB")
			# print(funcDeclVars["global"][k])
			regionType = "DATA_BLOCK" # "FUNC" 
			regionName = "global"

			if funcDeclVars["global"][k][1] == "VAR":
				print(funcDeclVars["global"][k][2])
				# if not globalVars in globalVars:
				# 	globalVars.append(stmtName)
			else:
				struct_name = funcDeclVars["global"][k][1]
				if not struct_name in globalDefinedDBs.keys():
					globalDefinedDBs[struct_name] = []
				if not k in globalDefinedDBs[struct_name]:
					globalDefinedDBs[struct_name].append(k)
					if not k in allglobalVarNames:
						allglobalVarNames.append(k)

				if len(funcDeclVars["global"][k]) >= 3:
					print(funcDeclVars["global"][k][2:])
					valuedVars = []

					for e in funcDeclVars["global"][k][2:]:
						valuedVars.append(e[0])
						stmtName = k + "@" + e[0]
						nodeType = "var-declarations"
						dataName = k + "@" + e[0]
						nSubType = k
						nodeValue = e[1][0]
						line = ("(var-declarations, " + stmtName + ", " + nodeValue + ")")
						lineTupleSize = 3
						rTag = dataName
						if not stmtName in globalVars:
							globalVars.append(stmtName)
						# print("- stmtName: " + stmtName + ", nodeValue: " + str(nodeValue) + ", dataName: " + str(dataName))
						add_node(SDG, stmtName, nodeType, dataName, nSubType, nodeValue, line, lineTupleSize, regionType, regionName, rTag)
					
					# for e in funcDeclVars["global"][struct_name]:
					# 	e_name = e[1]
					# 	if not e_name in valuedVars:
					# 		stmtName = k + "@" + e_name
					# 		nodeType = "var-declarations"
					# 		dataName = k + "@" + e_name
					# 		nSubType = k
					# 		nodeValue = ""
					# 		line = ("(var-declarations, " + stmtName + ")")
					# 		lineTupleSize = 2
					# 		rTag = dataName
					# 		if not globalVars in globalVars:
					# 			globalVars.append(stmtName)
					# 		add_node(SDG, stmtName, nodeType, dataName, nSubType, nodeValue, line, lineTupleSize, regionType, regionName, rTag)

					# add_node(G, entryNode, "ENTRY_NODE", "ENTRY_NODE", nodeLabel=entryNode, regionType=regionType, regionName=regionName)
					# add_node(G, n.stmtName, n.nodeType, n.dataName, n.nSubType, n.nodeValue, n.line, n.lineTupleSize, regionType, regionName, rTag)
		else:
			print("WTF!!!!!!!!!!!!!!!!!!!!!!")
			sys.exit()
		# if k.startswith("gtyp_") and len(funcDeclVars["global"][k]) > 2:
		# 	None

	return SDG

def addStructVarNode(SDG, new_DB_name, innerStruct="", funcDeclVars=[]):
	global globalVars, globalDefinedDBs

	regionType = "DATA_BLOCK" # "structure-type-name"
	regionName = "global"

	if innerStruct == "":
		if "@" in new_DB_name:
			innerStruct = new_DB_name.split("@")[-1]
	stmtName = new_DB_name
	nodeType = "var-declarations"
	dataName = stmtName
	nSubType = innerStruct
	# print(globalDefinedDBs)
	# print(globalDefinedDBs[innerStruct])
	# nSubType2 = globalDefinedDBs[innerStruct][-1]
	# nSubType2 = funcDeclVars["global"][innerStruct]
	nSubType2 = innerStruct
	if innerStruct.startswith("typ_"):
		nSubType2 = globalDefinedDBs[innerStruct][-1]
	# print(funcDeclVars["global"]["typ_MQTT_Interface_Dashboard_Subscribe"])
	# [['structure-element-declaration', 'EnvironmentSensor', 'typ_Environment_Sensor'], ['structure-element-declaration', 'BrightnessSensor', 'typ_Brightness_Sensor'], ['structure-element-declaration', 'CameraPicture', 'typ_Camera_Picture'], ['structure-element-declaration', 'PosPanTiltUnit', 'typ_Pos_Pan_Tilt_Unit_Enc'], ['structure-element-declaration', 'AlertMessage', 'typ_Alert_Message'], ['structure-element-declaration', 'Broadcast', 'typ_Broadcast'], ['structure-element-declaration', 'State_HBW', 'typ_State_Client'], ['structure-element-declaration', 'State_VGR', 'typ_State_Client'], ['structure-element-declaration', 'State_MPO', 'typ_State_Client'], ['structure-element-declaration', 'State_SLD', 'typ_State_Client'], ['structure-element-declaration', 'State_DSI', 'typ_State_Client'], ['structure-element-declaration', 'State_DSO', 'typ_State_Client'], ['structure-element-declaration', 'Stock_HBW', 'typ_Stock_Item'], ['structure-element-declaration', 'State_Order', 'typ_Order_Workpiece_Buttons_State'], ['structure-element-declaration', 'State_NFC_Device', 'typ_NFC_Module_State']]
	
	nodeValue = ""
	line = ("(var-declarations, " + stmtName + ", " + nSubType2 + ")")
	lineTupleSize = 3
	rTag = dataName
	# globalVars.append(stmtName)
	add_node(SDG, stmtName, nodeType, dataName, nSubType, nodeValue, line, lineTupleSize, regionType, regionName, rTag)


def decomposeStructVars(SDG, new_DB_name, innerStruct="", funcDeclVars=[]):
	global globalVars, globalDefinedDBs

	if innerStruct == "" or not innerStruct.startswith("typ_"):
		if not new_DB_name in globalVars:
			globalVars.append(new_DB_name)
			addStructVarNode(SDG, new_DB_name, innerStruct, funcDeclVars)
		return new_DB_name

	for d in funcDeclVars["global"][innerStruct]:
		dName = d[1]
		dType = d[2]
		tmp_DB_name = new_DB_name + "@" + dName

		decomposeStructVars(SDG, tmp_DB_name, dType, funcDeclVars)

	return True


def constructGlobalStructDataNodes(SDG, declFunctions, funcDeclVars):
	global globalVars, globalDefinedDBs

	regionType = "DATA_BLOCK" # "structure-type-name"
	regionName = "global"

	for k in funcDeclVars["global"].keys():
		# print(k)
		# print(funcDeclVars["global"][k])
		if isinstance(funcDeclVars["global"][k][0], list):
			# print("STRUCT")
			# print(k)
			# print(funcDeclVars["global"][k]) #[0]
			if k in globalDefinedDBs.keys():
				for DB_name in globalDefinedDBs[k]:
					for d in funcDeclVars["global"][k]:
						dType = d[2]
						new_DB_name = DB_name + "@" + d[1]
						if not new_DB_name in globalVars:
							# print(new_DB_name)
							# print("..........................")
							decomposeStructVars(SDG, new_DB_name, dType, funcDeclVars)
							# globalVars.append(new_DB_name)
							# addStructVarNode(SDG, new_DB_name, dType, funcDeclVars)
							stmtName = new_DB_name
							nodeType = "var-declarations"
							dataName = stmtName
							nSubType = k
							nSubType2 = globalDefinedDBs[k][-1]
							nodeValue = ""
							line = ("(var-declarations, " + stmtName + ", " + nSubType2 + ")")
							lineTupleSize = 3
							rTag = dataName
							# globalVars.append(stmtName)
							# add_node(SDG, stmtName, nodeType, dataName, nSubType, nodeValue, line, lineTupleSize, regionType, regionName, rTag)

			# "gtyp_HBW@typ_Workpiece" [dataName="gtyp_HBW@typ_Workpiece", label="(var-declarations, gtyp_HBW@typ_Workpiece)", nSize=2, nSubType=gtyp_HBW, nType="var-declarations", nValue="", rTag="gtyp_HBW@typ_Workpiece", regionName=global, regionType=DATA_BLOCK];
	# print("ttttttttttttt")
	# print(globalDefinedDBs)
	# sys.exit()

	return SDG

err_counter = 0
def constructGlobalDataEdges(SDG, declFunctions, funcDeclVars):
	global globalVars, err_counter

	for n in SDG.nodes(data=True):
		nIndex = n[0]
		nContent = n[1]

		if not nIndex in globalVars:
			continue
		# if nIndex == "ENTRY_R_TRIG" or nIndex == "ENTRY_TOF_TIME" or nIndex == "ENTRY_F_TRIG":
		# 	continue

		ndataName = nContent["dataName"]
		nType = nContent["nType"]
		nSubType = nContent["nSubType"]
		nValue = nContent["nValue"]
		nregionName = nContent["regionName"]

		for nn in SDG.nodes(data=True):
			nnIndex = nn[0]
			nnContent = nn[1]

			# if nnIndex == "ENTRY_R_TRIG" or nnIndex == "ENTRY_TOF_TIME" or nnIndex == "ENTRY_F_TRIG":
			# 	continue

			# print("pppppp")
			# print(nIndex)
			# print(nContent)
			# print(nnIndex)
			# print(nnContent)

			if not "label" in nn[1].keys():
				# print("kkkk")
				# if err_counter > 1:
				# 	sys.exit()
				# err_counter += 1
				continue

			nndataName = nnContent["dataName"]
			nnType = nnContent["nType"]
			nnSubType = nnContent["nSubType"]
			nnValue = nnContent["nValue"]
			nnregionName = nnContent["regionName"]

			if nIndex == nnIndex:
				continue

			if nIndex in nnValue:
				if nIndex.startswith("d") and ", Q, " in nContent["label"]:
					add_edge(SDG, nnIndex, nIndex, "global-data")
				else:
					add_edge(SDG, nIndex, nnIndex, "global-data")

			if nIndex in nndataName:
				if nnIndex.startswith("d") and ", Q, " in nnContent["label"]:
					add_edge(SDG, nIndex, nnIndex, "global-data")
				else:
					add_edge(SDG, nnIndex, nIndex, "global-data")

	return SDG

def constructNonGlobalDataEdges(SDG, declFunctions, funcDeclVars):
	global globalVars

	for n in SDG.nodes(data=True):
		nIndex = n[0]
		nContent = n[1]

		if nIndex in globalVars:
			continue
		# if nIndex == "ENTRY_R_TRIG" or nIndex == "ENTRY_TOF_TIME" or nIndex == "ENTRY_F_TRIG":
		# 	continue

		ndataName = nContent["dataName"]
		nType = nContent["nType"]
		nSubType = nContent["nSubType"]
		nValue = nContent["nValue"]
		nregionName = nContent["regionName"]

		for nn in SDG.nodes(data=True):
			nnIndex = nn[0]
			nnContent = nn[1]

			# if nnIndex == "ENTRY_R_TRIG" or nnIndex == "ENTRY_TOF_TIME" or nnIndex == "ENTRY_F_TRIG":
			# 	continue

			nndataName = nnContent["dataName"]
			nnType = nnContent["nType"]
			nnSubType = nnContent["nSubType"]
			nnValue = nnContent["nValue"]
			nnregionName = nnContent["regionName"]

			if nIndex == nnIndex:
				continue

			if ndataName in nnValue:
				add_edge(SDG, nIndex, nnIndex, "data")

	return SDG

def generateGraphs():
	global IRlines, declFunctions, funcDeclVars

	startEndRegions = findRegions(IRlines)

	keysList = list(startEndRegions.keys())
	CFG = ""
	entryNode =""
	exitNode = ""
	declFunctions = []
	funcDeclVars = {}
	# globalCFG = nx.MultiDiGraph(name="PLCprog-CFG", data=True, align='vertical')
	# globalCDG = nx.MultiDiGraph(name="PLCprog-CDG", data=True, align='vertical')
	# globalDDG = nx.MultiDiGraph(name="PLCprog-DDG", data=True, align='vertical')
	SDG = nx.MultiDiGraph(name="PLCprog-SDG", data=True, align='vertical')
	
	declFunctions, funcDeclVars = scanFunctionsVars(keysList, startEndRegions)
	# constructGlobalDataNodes(SDG, declFunctions, funcDeclVars)
	# print("OOOOOOOOOOOOOOO")
	# print(funcDeclVars)
	# print(funcDeclVars.keys())
	# print(funcDeclVars["global"]["typ_MQTT_Interface_Dashboard_Subscribe"])
	# [['structure-element-declaration', 'EnvironmentSensor', 'typ_Environment_Sensor'], ['structure-element-declaration', 'BrightnessSensor', 'typ_Brightness_Sensor'], ['structure-element-declaration', 'CameraPicture', 'typ_Camera_Picture'], ['structure-element-declaration', 'PosPanTiltUnit', 'typ_Pos_Pan_Tilt_Unit_Enc'], ['structure-element-declaration', 'AlertMessage', 'typ_Alert_Message'], ['structure-element-declaration', 'Broadcast', 'typ_Broadcast'], ['structure-element-declaration', 'State_HBW', 'typ_State_Client'], ['structure-element-declaration', 'State_VGR', 'typ_State_Client'], ['structure-element-declaration', 'State_MPO', 'typ_State_Client'], ['structure-element-declaration', 'State_SLD', 'typ_State_Client'], ['structure-element-declaration', 'State_DSI', 'typ_State_Client'], ['structure-element-declaration', 'State_DSO', 'typ_State_Client'], ['structure-element-declaration', 'Stock_HBW', 'typ_Stock_Item'], ['structure-element-declaration', 'State_Order', 'typ_Order_Workpiece_Buttons_State'], ['structure-element-declaration', 'State_NFC_Device', 'typ_NFC_Module_State']]
	# print(funcDeclVars["global"]["gtyp_MPO"])
	# print(funcDeclVars["global"]["gtyp_VGR"])
	# print(globalVars)
	# print(globalDefinedDBs)
	# print(allglobalVarNames)
	# addMissedGlobalVariables(SDG, declFunctions, funcDeclVars)
	# print(missedGlobalVariables)

	for k in funcDeclVars.keys():
		# print(type(funcDeclVars[k]))

		if isinstance(funcDeclVars[k], list):
			print(k)
			print(funcDeclVars[k])
			if len(funcDeclVars[k]) > 0:
				if funcDeclVars[k][0] == "DATA_BLOCK":
					print(funcDeclVars[k])
					# None
	# None

	i = 0
	for k in keysList:
		rStart = k
		rEnd = startEndRegions[k]
	
		if skipRegion(IRlines[rStart]): # "CONFIG block need some fixes on the IR part, mostly not needed, skip it."
			continue
		
		regionlines = IRlines[rStart:rEnd]
		# print("rStart = " + str(rStart) + ", rEnd = " + str(rEnd))
		if IRlines[rStart].startswith("(DATA_BLOCK, ") or IRlines[rStart].startswith("(structure-type-name, ") or IRlines[rStart].startswith("(DIRECT_VARS, "):
			print(IRlines[rStart])
		else:
			CFG, entryNode, exitNode = constructCFG(regionlines)
			# nx.drawing.nx_pydot.write_dot(CFG, "PLCprog-CFG.dot")
			#
			# oFileName = "output/PLCprog_CFG_" + str(k)
			# nx.drawing.nx_pydot.write_dot(CFG, oFileName + ".dot")
			# pdot = nx.drawing.nx_pydot.to_pydot(CFG)
			# pdot.write_pdf(oFileName + ".pdf")
			# sys.exit()
			# CFG = constructGlobalDataNodes(CFG, declFunctions, funcDeclVars)

			fSDG = constructFuncSDG(CFG, declFunctions, funcDeclVars)
			# nx.drawing.nx_pydot.write_dot(fSDG, "PLCprog-fSDG.dot")
			#
			# oFileName = "output/PLCprog_fSDG_" + str(k)
			# nx.drawing.nx_pydot.write_dot(fSDG, oFileName + ".dot")
			# pdot = nx.drawing.nx_pydot.to_pydot(fSDG)
			# pdot.write_pdf(oFileName + ".pdf")
			
			CDG = constructCDG(fSDG, entryNode, exitNode)
			# nx.drawing.nx_pydot.write_dot(CDG, "PLCprog-CDG.dot")
			#
			# oFileName = "output/PLCprog_CDG_" + str(k)
			# nx.drawing.nx_pydot.write_dot(CDG, oFileName + ".dot")
			# pdot = nx.drawing.nx_pydot.to_pydot(CDG)
			# pdot.write_pdf(oFileName + ".pdf")

			
			DDG = constructDDG(fSDG, entryNode, exitNode)
			# nx.drawing.nx_pydot.write_dot(DDG, "PLCprog-DDG.dot")
			#
			oFileName = "output/PLCprog_DDG_" + str(k)
			# nx.drawing.nx_pydot.write_dot(DDG, oFileName + ".dot")
			# pdot = nx.drawing.nx_pydot.to_pydot(DDG)
			# pdot.write_pdf(oFileName + ".pdf")

			
			PDG = constructPDG(CDG, DDG)
			# nx.drawing.nx_pydot.write_dot(PDG, "PLCprog-PDG.dot")
			#
			oFileName = "output/PLCprog_PDG_" + str(k)
			# nx.drawing.nx_pydot.write_dot(PDG, oFileName + ".dot")
			# pdot = nx.drawing.nx_pydot.to_pydot(PDG)
			# pdot.write_pdf(oFileName + ".pdf")
			# sys.exit()

			SDG.add_nodes_from(PDG.nodes(data=True))
			SDG.add_edges_from(PDG.edges(data=True))

			# if entryNode == "ENTRY_TON_TIME":
			# 	None

			# if entryNode == "ENTRY_FB_Axis":
			# 	None

			# if entryNode == "ENTRY_FB_Blinker":
			# 	None

			'''

			# i += 1
			# if i == 4:
			# 	break
			# break

			'''
	
	entryNode = "ENTRY_Main"
	exitNode = "EXIT_Main"
	constructSDG(SDG, entryNode, exitNode, declFunctions, funcDeclVars)

	t1 = len(SDG.nodes())
	t2 = len(SDG.edges())
	SDG = constructGlobalDataNodes(SDG, declFunctions, funcDeclVars)
	SDG = constructGlobalStructDataNodes(SDG, declFunctions, funcDeclVars)
	SDG = addMissedGlobalVariables(SDG, declFunctions, funcDeclVars)
	# print(len(globalVars))
	# sys.exit()
	# SDG = constructDDG(SDG, entryNode, exitNode)
	SDG = constructGlobalDataEdges(SDG, declFunctions, funcDeclVars)
	# SDG = constructNonGlobalDataEdges(SDG, declFunctions, funcDeclVars)
	SDG = fixSDG(SDG, declFunctions, funcDeclVars)
	print("SDG.nodes(): " + str(t1))
	print("SDG.edges(): " + str(t2))
	print("###################")
	print("SDG.nodes(): " + str(len(SDG.nodes())))
	print("SDG.edges(): " + str(len(SDG.edges())))

	# nx.drawing.nx_pydot.write_dot(SDG, "PLCprog-SDG.dot")
	oFileName = "output/PLCprog_SDG"
	nx.drawing.nx_pydot.write_dot(SDG, oFileName + ".dot")
	# pdot = nx.drawing.nx_pydot.to_pydot(SDG)
	# pdot.write_pdf(oFileName + ".pdf")

	# paths = nx.all_simple_paths(SDG, "stmt_711", "stmt_783")
	# for path in paths:
	# 	print("**")
	# 	print(path)

	# shortest_path = nx.shortest_path(SDG, "stmt_711", "stmt_783")
	# print(shortest_path)
	
	
def main():
    generateGraphs()
    # print(time.time())

if __name__ == "__main__":
    main()


print("--- %s seconds ---" % (time.time() - start_time))