import networkx as nx
import matplotlib.pyplot as plt
import os
import re
import time
import xml.etree.ElementTree as ET
import sys


start_time = time.time()

 # save graph in dot format
 # dot -Tpdf PLCprog-PDG.dot -o PLCprog-PDG.pdf
 # dot -Tpng PLCprog-PDG.dot -o PLCprog-PDG.png
 # dot PLCprog-PDG.dot -Tjpg -o PLCprog-PDG.jpg

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
	line = ""
	lineTupleSize = ""
	regionType = ""
	regionName = ""


def findRegions(IRlines):
	startEndRegions = {}
	regionDefinitions = ["(FUNC, ", "(PROG, ", "(CONFIG, "]

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

		
def add_node(G, stmtName, nodeType, dataName, nSubType="", nodeValue="", nodeLabel="", nodeLineSize=2, regionType="", regionName=""):
	if len(stmtName) > 0:
		if not G.has_node(stmtName):
			G.add_node(stmtName, dataName=dataName, nType=nodeType, nSubType=nSubType, nValue=nodeValue, nSize=nodeLineSize, label=nodeLabel, regionType=regionType, regionName=regionName)


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

def parseLine(line, regionType, regionName):
	global globalStmtCounter

	n = node()
	lineTuple = tuple(line[1:-1].split(", "))
	n.stmtName = "stmt_" + str(globalStmtCounter)
	globalStmtCounter += 1
	n.lineTupleSize = len(lineTuple)
	n.nodeType = lineTuple[0]
	n.dataName = lineTuple[1]
	n.nSubType = ""
	n.nodeValue = []
	n.line = line
	n.regionType = regionType
	n.regionName = regionName

	if "-declarations" in n.nodeType:
		if n.lineTupleSize == 5:
			n.nSubType = "directVar+init_" + lineTuple[3]
			n.nodeValue = [lineTuple[2], lineTuple[4]]
		else:
			if n.lineTupleSize >= 3:
				n.nSubType = lineTuple[2]
			if n.lineTupleSize >= 4:
				n.nodeValue = [lineTuple[3]]
		if n.nodeType == "input-declarations":
			n.nodeValue.append("formalInPara_" + n.regionName + "_" + n.dataName)

	if "IVAR" == n.nodeType:
		if lineTuple[2] == "multi-element-variable":
			n.nSubType = "multi-element-variable"
			n.nodeValue = [lineTuple[-3], lineTuple[-1]]
		else:
			if n.lineTupleSize == 3:
				n.nSubType = "const"
				n.nodeValue = [lineTuple[-1]]
				# if re.match(r[0-9]+):
			if n.lineTupleSize == 4:
				n.nSubType = "1-op"
				n.nodeValue = [lineTuple[-1]]
			if n.lineTupleSize == 5:
				n.nSubType = "2-op"
				n.nodeValue = [lineTuple[-3], lineTuple[-1]]

	if "ASSIGNMENT" == n.nodeType:
		n.nodeValue = [lineTuple[2]]
		# print(lineTuple)

	if "function-call" == n.nodeType:
		if n.lineTupleSize >= 3:
			n.nSubType = lineTuple[2]
		if n.lineTupleSize >= 4:
			n.nodeValue = list(lineTuple[3:])

	if "fb-invocation" == n.nodeType:
		n.nSubType = lineTuple[1]
		if n.lineTupleSize >= 3:
			n.nodeValue = list(lineTuple[2:])
		# print(n.nSubType)

	if "direct-variable" == n.nodeType:
		if n.lineTupleSize == 8:
			n.nSubType = lineTuple[3]
			n.nodeValue = [str(lineTuple[3]+lineTuple[5]+lineTuple[7])]

	return n


def skipRegion(firstLine):
	if firstLine.startswith("(CONFIG, "): # "CONFIG block need some fixes on the IR part, mostly not needed, skip it."
		return True
	return False

def skipNode(n):
	# if "-declarations" in n.nodeType and n.lineTupleSize == 3: # not a good idea, some variable are non-initialized, e.g., %IX0
	# 	return True
	return False

def constructCFG(regionlines):
	global globalStmtCounter

	firstLine = regionlines[0]
	firstLineTuple = tuple(firstLine[1:-1].split(", "))
	regionType = firstLineTuple[0]
	regionName = firstLineTuple[1]
	prev_n = ""
	firstNode = True
	G = nx.MultiDiGraph(name="PLCprog-CFG-" + regionType + "-" + regionName, data=True, align='vertical')

	print(regionName)
	
	entryNode = "ENTRY_"+regionName

	for line in regionlines[1:]:
		n = parseLine(line, regionType, regionName)
		# if skipNode(n):
		# 	continue
		add_node(G, n.stmtName, n.nodeType, n.dataName, n.nSubType, n.nodeValue, n.line, n.lineTupleSize, regionType, regionName)
		add_edge(G, prev_n, n.stmtName, "ctrl")
		# if n.nodeType == "fb-invocation":
		# 	ptrName = n.nSubType
		# 	ptr2func = funcDeclVars[regionName][ptrName]
		# 	paraList = n.nodeValue
		# 	for i in range(1, len(paraList), 2):
		# 		actualIn = paraList[i]
		# 		formalIn = paraList[i-1]
		# 		actualInNode = paraList[i] + "_" + str(time.time())
		# 		add_node(G, actualInNode, "actualIn", formalIn, ptr2func, [actualIn], paraList[i-1] + " = " + actualIn, 1, regionType, regionName)
		# 		add_edge(G, n.stmtName, actualInNode, "ctrl")
		prev_n = n.stmtName

		if firstNode:
			firstNode = False
			add_node(G, entryNode, "ENTRY_NODE", "ENTRY_NODE", nodeLabel=entryNode, regionType=regionType, regionName=regionName)
			add_edge(G, entryNode, prev_n, "ctrl")

	exitNode = "EXIT_"+regionName
	add_node(G, exitNode, "EXIT_NODE", "EXIT_NODE", nodeLabel=exitNode, regionType=regionType, regionName=regionName)
	add_edge(G, prev_n, exitNode, "ctrl")
	add_edge(G, entryNode, exitNode, "ctrl")

	return G, entryNode, exitNode

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

	directVarQ = getDirectVarQ(DDG)

	for n in DDG.nodes(data=True):
		nIndex = n[0]
		nContent = n[1]
		ndataName = nContent["dataName"]
		nType = nContent["nType"]
		nSubType = nContent["nSubType"]
		nValue = nContent["nValue"]
		nregionName = nContent["regionName"]

		if nType == "fb-invocation":
			continue

		for nn in DDG.nodes(data=True):
			nnIndex = nn[0]
			nnContent = nn[1]
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
				
				tempNnValue = []
				for i in range(1, len(nnValue), 2):
					tempNnValue.append(nnValue[i])
				nnValue = tempNnValue
				# print(nnValue)

			if nIndex == nnIndex:
				continue

			if ndataName in nnValue:
				# if ndataName == "pressure" and nregionName == "main" and nnregionName == "main":
				# 	paths = nx.all_simple_paths(G, nIndex, nnIndex)
				# 	for p in paths:
				# 		print("nIndex: " + str(nIndex) + ", nnIndex: " + str(nnIndex) + ", ndataName: " + str(ndataName) + ", nndataName: " + str(nndataName))
				# 		break

				if isReachingDefinition(G, nIndex, nnIndex, ndataName):
					# add_edge(DDG, nIndex, nnIndex, "data")

					if ndataName == "pressure" and nregionName == "main" and nnregionName == "main":
						print("nIndex: " + str(nIndex) + ", nnIndex: " + str(nnIndex) + ", ndataName: " + str(ndataName) + ", nndataName: " + str(nndataName))

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
	global IRlines
	declFunctions = []
	funcDeclVars = {}

	i = 0
	for k in keysList:
		rStart = k
		rEnd = startEndRegions[k]
		firstLine = IRlines[k]

		lineTuple = tuple(firstLine[1:-1].split(", "))
		regionType = lineTuple[0]
		regionName = lineTuple[1]

		if not (firstLine.startswith("(FUNC, ") or firstLine.startswith("(PROG, ")):
			continue
		
		if not regionName in declFunctions:
			declFunctions.append(regionName)
			funcDeclVars[regionName] = {}

		regionlines = IRlines[rStart:rEnd]

		for line in regionlines:
			n = parseLine(line, regionType, regionName)
			if "-declarations" in n.nodeType:
				funcDeclVars[regionName][n.dataName] = [n.nodeType, n.nSubType]
	
	# print(declFunctions)
	# print(funcDeclVars)
	# sys.exit()
	return declFunctions, funcDeclVars

def constructSDG(G, entryNode, exitNode, declFunctions, funcDeclVars):
	# tempG = nx.MultiDiGraph(name="PLCprog-SDG", data=True, align='vertical')
	# tempG.add_nodes_from(G.nodes(data=True))
	# tempG.add_edges_from(G.edges(data=True))

	for n in G.nodes(data=True):
		nName = n[0]
		regionType = n[1]["regionType"]
		regionName = n[1]["regionName"]
		dataName = n[1]["dataName"]

		if n[1]["nType"] == "fb-invocation":
			calleeFunc = funcDeclVars[regionName][dataName][1]
			add_edge(G, nName, "ENTRY_"+calleeFunc, "interp-ctrl")
			# exit()

		# if n[1]["nType"] == "formalIn":
		# 	print(n)
		# 	exit()

		if n[1]["nType"] == "actualIn":
			calleeFunc = n[1]["nSubType"]
			paraName = n[1]["dataName"]
			formalInPara = "formalInPara_" + calleeFunc + "_" + paraName
			add_edge(G, nName, formalInPara, "interp-data")
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
	nName = n[0]
	regionType = n[1]["regionType"]
	regionName = n[1]["regionName"]
	dataName = n[1]["dataName"]
	nValue = n[1]["nValue"]
	ptr = nValue[0]
	field = nValue[1]
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

# actualOut = "actualOutPara " + ptr + " " + calledFunction + " " + calledFunctionVar


def findActualOutParaRef(G, declFunctions, funcDeclVars):
	actualOutParaRef = []

	for n in G.nodes(data=True):
		nName = n[0]
		# print(G.nodes[nName])
		if n[1]["nType"] == "IVAR" and n[1]["nSubType"] == "multi-element-variable":
			isActualOutPara, interpPtrList = isActualOutParaRef(n, declFunctions, funcDeclVars)
			if isActualOutPara:
				actualOutParaRef.append(interpPtrList)
				# add data ref
				ptr = interpPtrList[2]
				calledFunction = interpPtrList[3]
				calledFunctionVar = interpPtrList[4]
				# n[1]["nValue"] = n[1]["nValue"] + ["actualOutPara " + ptr + " " + calledFunction + " " + calledFunctionVar]
				# G.nodes[nName]["nValue"] = G.nodes[nName]["nValue"] + ["actualOutPara " + ptr + " " + calledFunction + " " + calledFunctionVar]
				G.nodes[nName]["nValue"] = ["actualOutPara " + "_" + n[1]["regionName"] + "_" + ptr + " " + calledFunction + " " + calledFunctionVar]
				# print(G.nodes[nName])

	return actualOutParaRef


def constructFuncSDG(G, declFunctions, funcDeclVars):
	tempG = nx.MultiDiGraph(name="PLCprog-fSDG", data=True, align='vertical')
	tempG.add_nodes_from(G.nodes(data=True))
	tempG.add_edges_from(G.edges(data=True))

	for n in G.nodes(data=True):
		if n[1]["nType"] == "input-declarations":
			nName = n[0]
			regionType = n[1]["regionType"]
			regionName = n[1]["regionName"]
			dataName = n[1]["dataName"]
			nSubType = n[1]["nSubType"]
			formalInNode = "formalInPara_" + regionName + "_" + dataName
			entryNode = "ENTRY_" + regionName
			entryEdges = []
			
			add_node(tempG, formalInNode, "formalIn", formalInNode, dataName, [], formalInNode, 1, regionType, regionName)
			
			for e in tempG.edges(data=True):
				if e[0].startswith("ENTRY_"):
					if not e[1].startswith("EXIT_"):
						entryEdges.append(e)

			for e in entryEdges:
				tempG.remove_edge(e[0], e[1])
				add_edge(tempG, formalInNode, e[1], "ctrl")

			add_edge(tempG, entryNode, formalInNode, "ctrl")


		if n[1]["nType"] == "output-declarations":
			nName = n[0]
			regionType = n[1]["regionType"]
			regionName = n[1]["regionName"]
			dataName = n[1]["dataName"]
			nSubType = n[1]["nSubType"]
			formalOutNode = "formalOutPara_" + regionName + "_" + dataName
			entryNode = "ENTRY_" + regionName
			entryEdges = []
			
			add_node(tempG, formalOutNode, "formalOut", formalOutNode, dataName, [dataName], formalOutNode, 1, regionType, regionName)
			
			for e in tempG.edges(data=True):
				if e[0].startswith("ENTRY_"):
					if not e[1].startswith("EXIT_"):
						entryEdges.append(e)

			for e in entryEdges:
				tempG.remove_edge(e[0], e[1])
				add_edge(tempG, formalOutNode, e[1], "ctrl")

			add_edge(tempG, entryNode, formalOutNode, "ctrl")

	actualOutParaRef = findActualOutParaRef(tempG, declFunctions, funcDeclVars)
	# print(actualOutParaRef)

	for n in G.nodes(data=True):
		nName = n[0]
		regionType = n[1]["regionType"]
		regionName = n[1]["regionName"]
		if n[1]["nType"] == "fb-invocation":
			ptrName = n[1]["nSubType"]
			ptr2func = funcDeclVars[regionName][ptrName][1]
			paraList = n[1]["nValue"]

			if not ptr2func in declFunctions:
				continue
		
			for i in range(1, len(paraList), 2):
				actualIn = paraList[i]
				formalIn = paraList[i-1]
				actualInNode = paraList[i] + "_" + str(time.time())
				add_node(tempG, actualInNode, "actualIn", formalIn, ptr2func, [actualIn], "actualInPara " + formalIn + " = " + actualIn, 1, regionType, regionName)
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
					add_node(tempG, actualOut, "actualOut", actualOut, [ptr, calledFunction, calledFunctionVar], [], actualOut, 1, regionType, regionName)
					add_edge(tempG, nName, actualOut, "ctrl")


	return tempG



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
	# print(declFunctions)
	# print(funcDeclVars["composition_control"])

	i = 0
	for k in keysList:
		rStart = k
		rEnd = startEndRegions[k]
	
		if skipRegion(IRlines[rStart]): # "CONFIG block need some fixes on the IR part, mostly not needed, skip it."
			continue
		
		regionlines = IRlines[rStart:rEnd]
		# print("rStart = " + str(rStart) + ", rEnd = " + str(rEnd))
		CFG, entryNode, exitNode = constructCFG(regionlines)
		# nx.drawing.nx_pydot.write_dot(CFG, "PLCprog-CFG.dot")
		#
		# oFileName = "output/PLCprog_CFG_" + str(k)
		# nx.drawing.nx_pydot.write_dot(CFG, oFileName + ".dot")
		# pdot = nx.drawing.nx_pydot.to_pydot(CFG)
		# pdot.write_pdf(oFileName + ".pdf")
		
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
		# oFileName = "output/PLCprog_DDG_" + str(k)
		# nx.drawing.nx_pydot.write_dot(DDG, oFileName + ".dot")
		# pdot = nx.drawing.nx_pydot.to_pydot(DDG)
		# pdot.write_pdf(oFileName + ".pdf")
		
		PDG = constructPDG(CDG, DDG)
		# nx.drawing.nx_pydot.write_dot(PDG, "PLCprog-PDG.dot")
		#
		# oFileName = "output/PLCprog_PDG_" + str(k)
		# nx.drawing.nx_pydot.write_dot(PDG, oFileName + ".dot")
		# pdot = nx.drawing.nx_pydot.to_pydot(PDG)
		# pdot.write_pdf(oFileName + ".pdf")

		SDG.add_nodes_from(PDG.nodes(data=True))
		SDG.add_edges_from(PDG.edges(data=True))

		# i += 1
		# if i == 4:
		# 	break
		# break

	entryNode = "ENTRY_main"
	exitNode = "EXIT_main"
	constructSDG(SDG, entryNode, exitNode, declFunctions, funcDeclVars)
	# nx.drawing.nx_pydot.write_dot(SDG, "PLCprog-SDG.dot")
	oFileName = "output/PLCprog_SDG"
	nx.drawing.nx_pydot.write_dot(SDG, oFileName + ".dot")
	pdot = nx.drawing.nx_pydot.to_pydot(SDG)
	pdot.write_pdf(oFileName + ".pdf")

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