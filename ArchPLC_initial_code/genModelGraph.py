import networkx as nx
import matplotlib.pyplot as plt
import os
import re
import time
import xml.etree.ElementTree as ET
import pydot
# from graphviz import Source
import sys

input_file = "output/PLCprog_SDG.dot"
res_file = "output/physicalModel.txt"
res_file = open(res_file, "w")
res_lines = []
start_time = time.time()

 # save graph in dot format
 # dot -Tpdf PLCprog-PDG.dot -o PLCprog-PDG.pdf
 # dot -Tpng PLCprog-PDG.dot -o PLCprog-PDG.png
 # dot PLCprog-PDG.dot -Tjpg -o PLCprog-PDG.jpg

def isAcceptedPath(G, path):
	# visitedNodes = []
	# toVisitNodes = []
	callStack = []
	# print("-----")
	# print(path)
	isLastNode = False
	for i in range(0, len(path)):
		n = path[i]
		
		if i == len(path)-1:
			isLastNode = True

		nRegionName = G.nodes[n]["regionName"]
		nType = G.nodes[n]["nType"]
		nSubType = G.nodes[n]["nSubType"]

		if not isLastNode:
			nn = path[i+1]
			nnRegionName = G.nodes[nn]["regionName"]
			nnType = G.nodes[nn]["nType"]
			nnSubType = G.nodes[nn]["nSubType"]

			if nnType == "formalIn":
				callStack.append(nRegionName) # push
				# print("pushed " + nRegionName)

		if nType == "formalOut":
			# for e in G.out_edges(n, keys=True,data=True):
			if not isLastNode:
				nn = path[i+1]
				nnRegionName = G.nodes[nn]["regionName"]
				nnType = G.nodes[nn]["nType"]
				nnSubType = G.nodes[nn]["nSubType"]


				if len(callStack) > 0 and not nnRegionName == callStack[-1]:
					# print("Failed " + nnRegionName + " vs. " + callStack[-1])
					return False
				else:
					if nnRegionName in callStack:
						callStack.remove(nnRegionName)
						# print(" popped " + nnRegionName)
	return True


def walkCallStack(G, srcNode, dstNode):
	visitedNodes = []
	toVisitNodes = []
	callStack = []

	toVisitNodes.append(srcNode)
	# print(G.out_degree(srcNode))
	discoveredNewNodes = False
	while len(toVisitNodes) > 0:
		for n in toVisitNodes:
			for e in G.out_edges(n, keys=True,data=True):
				if not e[1] in visitedNodes:
					if not e[1] in toVisitNodes:
						nRegionName = G.nodes[n]["regionName"]
						nType = G.nodes[n]["nType"]
						nSubType = G.nodes[n]["nSubType"]
						nnRegionName = G.nodes[e[1]]["regionName"]
						nnType = G.nodes[e[1]]["nType"]
						nnSubType = G.nodes[e[1]]["nSubType"]

						# print(G.nodes[e[1]])
						# exit()
						toVisitNodes.append(e[1])
						discoveredNewNodes = True
						# print(e)
			visitedNodes.append(n)
			toVisitNodes.remove(n)
	# print(visitedNodes)
	# print(toVisitNodes)
	# exit()

def getPaths(G, srcNode, dstNode):
	paths = []

	for path in nx.all_simple_paths(G, srcNode, dstNode):
		paths.append(path)

	return paths

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

def removeCtrlEdges(G, EdgesType = "ctrl"):
	edges2Delete = []

	for (u, v, k) in G.edges(keys=True):
		if G.adj[u][v][k]["tLabel"] == EdgesType:
			# or G.adj[u][v][k]["tLabel"] == "interp-ctrl" or G.adj[u][v][k]["tLabel"] == '"interp-ctrl"'
			# if not G.nodes[u]["nType"] == "fb-invocation" and not G.nodes[v]["nType"] == "fb-invocation":
			# 	if not G.nodes[u]["nType"] == "'fb-invocation'" and not G.nodes[v]["nType"] == "'fb-invocation'":
			# 		if not G.nodes[u]["nType"] == '"fb-invocation"' and not G.nodes[v]["nType"] == '"fb-invocation"':
			#			# print(G.nodes[u]["nType"] + ", " + G.nodes[v]["nType"])
			edges2Delete.append((u, v, k))

	for e in edges2Delete:
		u = e[0]
		v = e[1]
		k = e[2]
		G.remove_edge(u, v, key=k)

def extractModelGraph(G, srcNode, dstNode):
	# srcNode = "stmt_715" # sensor
	# print(srcNode)
	# print(dstNode)
	# print(G.nodes(data=True))
	reachableDescStmts = list(nx.descendants(G, srcNode)) + [srcNode]
	# print(reachableDescStmts)

	# dstNode = "stmt_741" # actuator
	reachableAncesStmts = list(nx.ancestors(G, dstNode)) + [dstNode]
	# print(reachableAncesStmts)

	reachableStmts = intersection(reachableDescStmts, reachableAncesStmts)

	# reachableStmts = reachableDescStmts

	# print(reachableStmts)
	# print(len(reachableStmts))

	modelGraph = G.subgraph(reachableStmts).copy()

	return modelGraph

def extractModelGraph2(G, srcNode, dstNode):
	reachableDescStmts = list(nx.descendants(G, srcNode)) + [srcNode]

	reachableAncesStmts = list(nx.ancestors(G, dstNode)) + [dstNode]

	reachableStmts = union(reachableDescStmts, reachableAncesStmts)
	modelGraph = G.subgraph(reachableStmts).copy()

	return modelGraph

directVarNodes = {}

def find_substr(target_str, start_str, end_str):
	start = target_str.find(start_str) + len(start_str)
	end = target_str.find(end_str)

	return target_str[start:end]


def genModelGraph(G, directIQMVariables, vType="Q", fileName=""):
	global directVarNodes, res_file

	# temp_G = G.copy(as_view=False)
	# removeCtrlEdges(temp_G)
	
	for n in list(directIQMVariables.keys()):
		# if directIQMVariables[n][0] == "I":
		if not directIQMVariables[n][0] == vType:
			continue

		print("\n")

		current_actuator = find_substr(directIQMVariables[n][1], "\"['", "']\"")
		result_str = "" # current_actuator + ","
		print("======")
		print("Actuator " + n + " (" + current_actuator + ") has relationships with the following variables: ")
		
		g_acceptedNodes = [n]
		for nn in list(directIQMVariables.keys()):
			if n == nn:
				continue

			# actuator doesn't effect another actuator!
			# if vType == "Q" and directIQMVariables[nn][0] == vType:
			# 	continue

			# print("====")
			# print(n)
			# print(nn)
			# print(directIQMVariables[nn][1][0])

			# this is True when vType == "Q"
			srcNode = nn # sensor
			dstNode = n # actuator
			# if vType == "I":
			# 	srcNode = n # sensor 
			# 	dstNode = nn # actuator

			if not nx.is_empty(G):
				# print("Variable " + directIQMVariables[nn][1])
				# oFileName = "output/PLCprogMG_" + dstNode + "_" + srcNode + ".dot"
				# print(oFileName)
				# nx.drawing.nx_pydot.write_dot(modelGraph, oFileName)

				

				isReachable = nx.has_path(G, srcNode, dstNode)
				# if isReachable and "QX_VGR_ValveVacuum_Q8" in dstNode:
				# 	paths = getPaths(G, srcNode, dstNode)
				# 	print(paths)
				# 	sys.exit()

				if isReachable:
					g_acceptedNodes.append(srcNode)
					print(srcNode)
		
		g_acceptedNodes = list(set(g_acceptedNodes))
		# print(g_acceptedNodes)
		if len(g_acceptedNodes) <= 1:
			continue

		directVarNodes = []
		directVarNames = {}
		
		for an in g_acceptedNodes:
			if an in list(directIQMVariables.keys()):
				# print("Variable " + str(an) + ": " + str(directIQMVariables[an]))
				# current_var = find_substr(directIQMVariables[an][1], "\"['", "']\"")
				current_var = an
				directVarNodes.append(an)
				if len(current_var) > 0:
					result_str += current_var + ","
				directVarNames[an] = current_var

		res_line = result_str[:-1] + "\n"
		if "," in res_line and not res_line in res_lines:
			res_file.write(res_line.replace("@", "."))
			res_lines.append(res_line)

'''
def genModelGraph(G, directIQMVariables, vType="Q", fileName=""):
	global directVarNodes, res_file

	for n in list(directIQMVariables.keys()):
		# if directIQMVariables[n][0] == "I":
		if not directIQMVariables[n][0] == vType:
			continue

		print("\n")
		
		current_actuator = find_substr(directIQMVariables[n][1], "\"['", "']\"")
		result_str = "" # current_actuator + ","
		print("======")
		print("Actuator " + n + " (" + current_actuator + ") has relationships with the following variables: ")
		
		g_acceptedNodes = []
		for nn in list(directIQMVariables.keys()):
			if n == nn:
				continue

			# actuator doesn't effect another actuator!
			# if vType == "Q" and directIQMVariables[nn][0] == vType:
			# 	continue

			# print("====")
			# print(n)
			# print(nn)
			# print(directIQMVariables[nn][1][0])

			# this is True when vType == "Q"
			srcNode = nn # sensor
			dstNode = n # actuator
			# if vType == "I":
			# 	srcNode = n # sensor 
			# 	dstNode = nn # actuator 

			temp_G = G.copy(as_view=False)
			# removeCtrlEdges(temp_G)
			modelGraph = extractModelGraph(temp_G, srcNode, dstNode)
			acceptedNodes = []

			if not nx.is_empty(modelGraph):
				# print("Variable " + directIQMVariables[nn][1])
				# oFileName = "output/PLCprogMG_" + dstNode + "_" + srcNode + ".dot"
				# print(oFileName)
				# nx.drawing.nx_pydot.write_dot(modelGraph, oFileName)

				paths = getPaths(modelGraph, srcNode, dstNode)
				# print(paths)
				

				for path in paths:
					# if isAcceptedPath(modelGraph, path):
					if True:
						# cur_path = []
						# for p in path:
						# 	if not p == n:
						# 		cur_path.append(p)
						# acceptedNodes = union(acceptedNodes, cur_path)
						acceptedNodes = union(acceptedNodes, path)
				
				g_acceptedNodes += acceptedNodes

		
		g_acceptedNodes = list(set(g_acceptedNodes))
		# print(g_acceptedNodes)

		directVarNodes = []
		directVarNames = {}
		
		for an in g_acceptedNodes:
			if an in list(directIQMVariables.keys()):
				# print("Variable " + str(an) + ": " + str(directIQMVariables[an]))
				# current_var = find_substr(directIQMVariables[an][1], "\"['", "']\"")
				current_var = an
				directVarNodes.append(an)
				if len(current_var) > 0:
					result_str += current_var + ","
				directVarNames[an] = current_var

		cleanedModelGraph = temp_G.subgraph(g_acceptedNodes).copy()
		if not nx.is_empty(cleanedModelGraph):
			# print("Variable " + directIQMVariables[nn][1])
			# oFileName = "output/PLCprogMG_" + dstNode + "_" + srcNode + ".dot"
			# print(dstNode)
			# print(fileName)
			oFileName = "output/PLCprogMG_" + dstNode + fileName
			nx.drawing.nx_pydot.write_dot(cleanedModelGraph, oFileName + ".dot")
			# nx.drawing.nx_pydot.write_pdf(cleanedModelGraph, oFileName + ".pdf")
			pdot = nx.drawing.nx_pydot.to_pydot(cleanedModelGraph)
			pdot.write_pdf(oFileName + ".pdf")
			print(oFileName)
			# print("done")

			temp_cmg = cleanedModelGraph.copy(as_view=False)
			amg_model = genAbstractedModelGraph(temp_cmg, directIQMVariables, directVarNodes, directVarNames)
			if not nx.is_empty(amg_model):
				oFileName = "output/PLCprogAMG_" + dstNode + fileName
				nx.drawing.nx_pydot.write_dot(amg_model, oFileName + ".dot")
				# nx.drawing.nx_pydot.write_pdf(amg_model, oFileName + ".pdf")
				pdot = nx.drawing.nx_pydot.to_pydot(amg_model)
				pdot.write_pdf(oFileName + ".pdf")
				# print(oFileName)
				oFileName = "output/vars_" + dstNode + fileName + ".txt"
				output_file = open(oFileName, "w")
				output_file.write(result_str)
				res_line = result_str[:-1] + "\n"
				if "," in res_line and not res_line in res_lines:
					res_file.write(res_line)
					res_lines.append(res_line)
				# print(result_str[:-1] + "\n")
				# sys.exit()
			# sys.exit()

		# walkCallStack(G, srcNode, dstNode)

		# exit()
'''
def getModelGraphPathsSources(G, directIQMVariables):
	nPaths = {}
	# temp_G = G.copy(as_view=False)

	for n in list(directIQMVariables.keys()):
		if not directIQMVariables[n][0] == "Q":
			continue

		for nn in list(directIQMVariables.keys()):

			if n == nn:
				continue

			if directIQMVariables[nn][0] == "Q":
				continue

			if not n in G.nodes() or not nn in G.nodes():
				continue

			srcNode = nn # sensor
			dstNode = n # actuator

			if not nx.is_empty(G):
				paths = getPaths(G, srcNode, dstNode)
				nPaths[srcNode] = paths
	sources = list(nPaths.keys()) # sensors, actuators and configuration variables
	# sources_names = {}
	# for s in sources:

	# print(G.nodes(data=True)[s])
	# sys.exit()
	return nPaths, sources

def genAbstractedModelGraph(G, directIQMVariables, directVarNodes, directVarNames):
	nPaths, sources = getModelGraphPathsSources(G, directIQMVariables)
	
	nodes2Combine = []
	combinedNodes = []

	# print(directVarNodes)

	for s in sources:
		for p in nPaths[s]:
			for n in p:
				if "decl" in G.nodes(data=True)[n]["nType"] or "direct" in G.nodes(data=True)[n]["nType"]:
					continue
				n_successors = G.successors(n)
				i_anc = set(nx.ancestors(G, n))
				# print("n = " + str(n))
				for n_s in n_successors:
					if "decl" in G.nodes(data=True)[n_s]["nType"] or "direct" in G.nodes(data=True)[n_s]["nType"]:
						continue
					ii_anc = set(nx.ancestors(G, n_s))
					# print("n_s = " + str(n_s))
					shouldCombine = len(ii_anc.difference(i_anc)) == 1

					if shouldCombine:
						if not n_s in combinedNodes:
							found_n = False

							for l in nodes2Combine:
								if n in l:
									found_n = True
									l.append(n_s)
							if not found_n:
								nodes2Combine.append([n, n_s])

							combinedNodes.append(n_s)

	# nPaths, sources = getModelGraphPathsSources(G, directIQMVariables)

	# let's taint the nodes
	tainted_nodes = {}
	tn_count = {}
	for s in sources:
		for p in nPaths[s]:
			# print(p)
			cc = 1
			for n in p:
				if not n in G:
					continue
				if n == s:
					continue

				if not n in list(tainted_nodes.keys()):
					tainted_nodes[n] = [s]
					tn_count[n] = {}
					tn_count[n][s] = cc
				else:
					if not s in tainted_nodes[n]:
						tainted_nodes[n].append(s)
						tn_count[n][s] = cc

				cc += 1
	

	tainted_nodes = {k: v for k, v in sorted(tainted_nodes.items(), key=lambda item: len(item[1]))}
	tn_count = {k: v for k, v in sorted(tn_count.items(), key=lambda item: len(item[1]))}
	tn_list = list(tn_count.keys())

	# contract nodes
	for nodes in nodes2Combine:
		for node in nodes[1:]:
			G = nx.contracted_nodes(G, nodes[0], node, self_loops=False)

	# print(tainted_nodes)
	# print("=====")
	# print(tn_count)
	# print("=====")
	# print(tn_list)

	directVarDistances = {}
	for n in directVarNodes:
		# if directIQMVariables[n][0] == "Q":
		# 	continue

		if directVarNames[n].startswith("Q"):
			continue

		directVarDistances[n] = {}

		for nn in directVarNodes:
			if directVarNames[nn].startswith("Q"):
				continue

			if n == nn:
				continue
			directVarDistances[n][nn] = None

	for n in tn_list:
		# print(G.nodes(data=True)[n])
		if n in directVarNodes:
			continue

		for vn1 in directVarNodes:
			if vn1 in tainted_nodes[n]:
				for vn2 in directVarNodes:
					if vn1 == vn2:
						continue
					if vn2 in tainted_nodes[n]:
						if directVarDistances[vn1][vn2] == None:
							directVarDistances[vn1][vn2] = tn_count[n][vn1]
						else:
							if directVarDistances[vn1][vn2] > tn_count[n][vn1]:
								directVarDistances[vn1][vn2] = tn_count[n][vn1]
	print("=====")
	print(directVarDistances)

	# sys.exit()

	return G

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def getDirectIQMVariables(G):
	directIQMVariables = {}

	for n in G.nodes(data=True):
		nIndex = n[0]
		nContent = n[1]
		if len(nContent.keys()) == 0:
			continue
		ndataName = nContent["dataName"]
		nType = nContent["nType"]
		nSubType = nContent["nSubType"]
		nValue = nContent["nValue"]
		nregionName = nContent["regionName"]
		regionType = nContent["regionType"]

		# if nSubType == "direct-var-def" or nSubType == '"direct-var-def"':
		if nSubType == "direct-var-use" or nSubType == '"direct-var-use"':
			if not nIndex in list(directIQMVariables.keys()):
				if ", I," in nContent["label"] or ((nSubType == "direct-var-use" or nSubType == '"direct-var-use"') and ndataName.startswith("I")):
					directIQMVariables[nIndex] = ("I", nValue, nregionName)
				elif ", Q," in nContent["label"] or ((nSubType == "direct-var-use" or nSubType == '"direct-var-use"') and ndataName.startswith("Q")):
					directIQMVariables[nIndex] = ("Q", nValue, nregionName)
		elif regionType == "DATA_BLOCK": # and "gtyp_" in nContent["label"]
			if not nIndex in list(directIQMVariables.keys()):
				directIQMVariables[nIndex] = ("M", nValue, nregionName)

	return directIQMVariables


def main():
	global res_file, res_lines, input_file

	SDG = nx.drawing.nx_pydot.read_dot(input_file)
	print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
	print("Performing configuration variables correlation analysis....")

	# set to True if you want to include other declared variables as sources
	directIQMVariables = getDirectIQMVariables(SDG) # , True

	# removeCtrlEdges(SDG)

	genModelGraph(SDG, directIQMVariables, "Q")
	genModelGraph(SDG, directIQMVariables, "M")
	genModelGraph(SDG, directIQMVariables, "I")

	res_file.close()
	res_file = "output/physicalModel1.txt"
	res_file = open(res_file, "w")
	res_lines = []

	temp_SDG = SDG.copy(as_view=False)
	removeCtrlEdges(temp_SDG)
	
	genModelGraph(temp_SDG, directIQMVariables, "Q")
	genModelGraph(temp_SDG, directIQMVariables, "M")
	genModelGraph(temp_SDG, directIQMVariables, "I")

	res_file.close()
	res_file = "output/physicalModel2.txt"
	res_file = open(res_file, "w")
	res_lines = []

	temp_SDG = SDG.copy(as_view=False)
	removeCtrlEdges(temp_SDG, "data")

	genModelGraph(temp_SDG, directIQMVariables, "Q")
	genModelGraph(temp_SDG, directIQMVariables, "M")
	genModelGraph(temp_SDG, directIQMVariables, "I")

	res_file.close()

if __name__ == "__main__":
    main()
    

print("--- %s seconds ---" % (time.time() - start_time))