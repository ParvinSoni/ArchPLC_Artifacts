import networkx as nx
import matplotlib.pyplot as plt
import os
import re
import time
import xml.etree.ElementTree as ET
import pydot
from graphviz import Source
import sys

os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'

start_time = time.time()

 # save graph in dot format
 # dot -Tpdf PLCprog-PDG.dot -o PLCprog-PDG.pdf
 # dot -Tpng PLCprog-PDG.dot -o PLCprog-PDG.png
 # dot PLCprog-PDG.dot -Tjpg -o PLCprog-PDG.jpg

directVarRegNames = {}
directVarRegNames["MW0"] =  "flow_set"
directVarRegNames["MW1"] =  "a_setpoint"
directVarRegNames["MW2"] = "pressure_sp"
directVarRegNames["MW3"] = "override_sp"
directVarRegNames["MW4"] = "level_sp"
directVarRegNames["IW0"] = "f1_valve_pos"
directVarRegNames["IW1"] = "f1_flow"
directVarRegNames["IW2"] = "f2_valve_pos"
directVarRegNames["IW3"] = "f2_flow"
directVarRegNames["IW4"] = "purge_valve_pos"
directVarRegNames["IW5"] = "purge_flow"
directVarRegNames["IW6"]	= "product_valve_pos"
directVarRegNames["IW7"] = "product_flow"
directVarRegNames["IW8"] = "pressure"
directVarRegNames["IW9"] = "level"
directVarRegNames["IW10"] = "a_in_purge"
directVarRegNames["IW11"] = "b_in_purge"
directVarRegNames["IW12"] = "c_in_purge"
directVarRegNames["QW0"] = "f1_valve_sp"
directVarRegNames["QW1"] = "f2_valve_sp"
directVarRegNames["QW2"] = "purge_valve_sp"
directVarRegNames["QW3"] = "product_valve_sp"

# directVarRegNames = {}
# directVarRegNames["flow_set"] = "MW0"
# directVarRegNames["a_setpoint"] = "MW1"
# directVarRegNames["pressure_sp"] = "MW2"
# directVarRegNames["override_sp"] = "MW3"
# directVarRegNames["level_sp"] = "MW4"
# directVarRegNames["f1_valve_pos"] = "IW0"
# directVarRegNames["f1_flow"] = "IW1"
# directVarRegNames["f2_valve_pos"] = "IW2"
# directVarRegNames["f2_flow"] = "IW3"
# directVarRegNames["purge_valve_pos"] = "IW4"
# directVarRegNames["purge_flow"] = "IW5"
# directVarRegNames["product_valve_pos"]	= "IW6"
# directVarRegNames["product_flow"] = "IW7"
# directVarRegNames["pressure"] = "IW8"
# directVarRegNames["level"] = "IW9"
# directVarRegNames["a_in_purge"] = "IW10"
# directVarRegNames["b_in_purge"] = "IW11"
# directVarRegNames["c_in_purge"] = "IW12"
# directVarRegNames["f1_valve_sp"] = "QW0"
# directVarRegNames["f2_valve_sp"] = "QW1"
# directVarRegNames["purge_valve_sp"] = "QW2"
# directVarRegNames["product_valve_sp"] = "QW3"

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

def removeCtrlEdges(G):
	edges2Delete = []

	for (u, v, k) in G.edges(keys=True):
		if G.adj[u][v][k]["tLabel"] == "ctrl" :
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

def genModelGraph(G, directIQMVariables, fileName=""):
	global directVarNodes

	# print(len(list(G.nodes)))

	# srcNode = "stmt_715" # sensor
	# dstNode = "stmt_741" # actuator
	# modelGraph = extractModelGraph(G, srcNode, dstNode)
	# nx.drawing.nx_pydot.write_dot(modelGraph, "output/PLCprogMG_" + srcNode + "_" + dstNode + ".dot")
	# print(directIQMVariables)

	res_file = "output/result.txt"
	res_file = open(res_file, "w")

	for n in list(directIQMVariables.keys()):
		# if directIQMVariables[n][0] == "I":
		if not directIQMVariables[n][0] == "Q":
			continue

		print("\n")

		
		current_actuator = find_substr(directIQMVariables[n][1], "\"['", "']\"")
		result_str = "" # current_actuator + ","
		print("======")
		print("Actuator " + current_actuator + " has relationships with the following variables: ")
		# directVarNodes[current_actuator] = [n]


		# print(str(list(directIQMVariables.keys())) + "\n")

		g_acceptedNodes = []

		for nn in list(directIQMVariables.keys()):

			if n == nn:
				continue

			if directIQMVariables[nn][0] == "Q":
				continue

			# print("====")
			# print(n)
			# print(nn)
			# print(directIQMVariables[nn][1][0])

			srcNode = nn # sensor
			dstNode = n # actuator
			temp_G = G.copy(as_view=False)
			removeCtrlEdges(temp_G)
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
					if isAcceptedPath(modelGraph, path):
						# print(path)
						acceptedNodes = union(acceptedNodes, path)
				
				g_acceptedNodes += acceptedNodes

				# print(acceptedNodes)
				# cleanedModelGraph = modelGraph.subgraph(acceptedNodes).copy()

				'''
				# let's add the read nodes for every node in the cleanedModelGraph
				temp_G2 = G.copy(as_view=False)
				removeCtrlEdges(temp_G2)
				acceptedNodes2 = []
				for dstNode2 in cleanedModelGraph.nodes(data=True):
					for srcNode2 in temp_G2.nodes(data=True):
						modelGraph2 = extractModelGraph(temp_G2, srcNode2[0], dstNode2[0])
						if not nx.is_empty(modelGraph2):
							paths2 = getPaths(modelGraph2, srcNode2[0], dstNode2[0])
							
							for path2 in paths2:
								# if isAcceptedPath(modelGraph2, path2):
								# 	acceptedNodes2 = union(acceptedNodes2, path2)

								acceptedNodes2 = union(acceptedNodes2, path2)
				
				print(acceptedNodes2)
				cleanedModelGraph2 = modelGraph2.subgraph(acceptedNodes2).copy()
				cleanedModelGraph.add_nodes_from(cleanedModelGraph2.nodes(data=True))
				cleanedModelGraph.add_edges_from(cleanedModelGraph2.edges(data=True))
				'''
		g_acceptedNodes = list(set(g_acceptedNodes))
		# print(g_acceptedNodes)

		# for an in g_acceptedNodes:
		# 	if an in list(directIQMVariables.keys()):
		# 		print("Variable " + str(an) + ": " + str(directIQMVariables[an]))
		# 		current_var = find_substr(directIQMVariables[an][1], "\"['", "']\"")
		# 		directVarNodes[current_actuator].append((an, directIQMVariables[an][0], current_var))

		directVarNodes = []
		directVarNames = {}
		
		for an in g_acceptedNodes:
			if an in list(directIQMVariables.keys()):
				# print("Variable " + str(an) + ": " + str(directIQMVariables[an]))
				current_var = find_substr(directIQMVariables[an][1], "\"['", "']\"")
				directVarNodes.append(an)
				result_str += current_var + ","
				directVarNames[an] = current_var

		# print(directVarNodes)
		print(directVarNames)
		# ['stmt_741', 'stmt_703', 'stmt_715', 'stmt_729']
		# {'stmt_741': 'QW0', 'stmt_715': 'IW0', 'stmt_729': 'IW7', 'stmt_703': 'MW0'}

		# sys.exit()

		cleanedModelGraph = temp_G.subgraph(g_acceptedNodes).copy()
		if not nx.is_empty(cleanedModelGraph):
			# print("Variable " + directIQMVariables[nn][1])
			# oFileName = "output/PLCprogMG_" + dstNode + "_" + srcNode + ".dot"
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
				print(oFileName)
				oFileName = "output/vars_" + dstNode + fileName + ".txt"
				output_file = open(oFileName, "w")
				output_file.write(result_str)
				res_file.write(result_str + "\n")
			# sys.exit()



		# walkCallStack(G, srcNode, dstNode)

		# exit()

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
		elif edgeLabel == "relationship":
			G.add_edge(source, destination, style="solid", tLabel=edgeLabel, color="green")

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

def getDirectIQMVariables(G, includeDecl=False):
	directIQMVariables = {}

	for n in G.nodes(data=True):
		if len(list(n[1].keys())) == 0:
			continue
		nIndex = n[0]
		nContent = n[1]
		ndataName = nContent["dataName"]
		nType = nContent["nType"]
		nSubType = nContent["nSubType"]
		nValue = nContent["nValue"]
		nregionName = nContent["regionName"]
		# print(n)
		if nType == "direct-variable" or nType == '"direct-variable"':
			# if nSubType == "I" or nSubType == "Q" or nSubType == "M":
			# print(n)
			if not nIndex in list(directIQMVariables.keys()):
				directIQMVariables[nIndex] = (nSubType, nValue, nregionName)
		elif includeDecl and (nType == "var-declarations" or nType == '"var-declarations"' or nType == "input-declarations" or nType == '"input-declarations"' or nType == "output-declarations" or nType == '"output-declarations"'):
			if not nIndex in list(directIQMVariables.keys()):
				if hasNumbers(nValue):
					directIQMVariables[nIndex] = (nSubType, nValue, nregionName)

	return directIQMVariables


def main():
	SDG = nx.drawing.nx_pydot.read_dot("output/PLCprog_SDG.dot")

	# set to True if you want to include other declared variables as sources
	directIQMVariables = getDirectIQMVariables(SDG) # , True
	genModelGraph(SDG, directIQMVariables)

	# include other vars as sources
	# directIQMVariables = getDirectIQMVariables(SDG, True) # , True
	# genModelGraph(SDG, directIQMVariables, "_allVars")

if __name__ == "__main__":
    main()
    

print("--- %s seconds ---" % (time.time() - start_time))