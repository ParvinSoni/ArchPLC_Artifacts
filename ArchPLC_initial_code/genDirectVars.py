import re
import xml.etree.ElementTree as ET
import sys


ir_input = "IR.txt"
plctags_input = "PLCTags_ft.xml"
# plctags_input = "PLCTags_chemical_plant.xml"

output_f = "IR_directVars.txt"

isRoot = True
d_counter = 0
dirctVarsDict = {}
IRlines = None
globalFuncVars = []

def parseXML(node, prefix=""):
	global isRoot, d_counter, dirctVarsDict, globalFuncVars

	node_tag = node.tag.strip()
	node_text = ""
	

	# print(node)
	if "addr" in node.attrib.keys():
		out_str = ""
		addr = node.attrib["addr"][1:]
		varName = node.text.strip()
		varType = node.attrib["type"]

		# print(addr)
		# print(node.attrib)
		# print(varName)

		# if not varName in dirctVarsDict.keys():
		# if not varName in globalFuncVars:
		varFields = []
		out_str += "(direct-variable, d" + str(d_counter) + "*, location-prefix, " + addr[0] + ", size-prefix, "
		varFields.append(str(d_counter))
		varFields.append(addr[0])
		
		if not "." in addr:
			out_str +=  addr[1] + ", "
			varFields.append(addr[1] + ", ")
		else:
			if varType == "Bool":
				out_str += "X, "
				varFields.append("X, ")
			elif varType == "Int":
				out_str += "W, "
				varFields.append("W, ")
	
		if not "." in addr:
			out_str += "integer, " + addr[2:] + ")"
			varFields.append("integer, " + addr[2:] + ")")
		else:
			out_str += "integer, " + addr[1:addr.rfind(".")] + ", ., integer, " + addr[addr.rfind(".")+1:] + ")"
			varFields.append("integer, " + addr[1:addr.rfind(".")] + ", ., integer, " + addr[addr.rfind(".")+1:] + ")")
		
		# print(varName)
		# print(out_str)
		
		dirctVarsDict[varName] = ("d" + str(d_counter) + "*", varType, out_str, varFields) #varType.lower()
		# globalFuncVars.append(varName)
		# d_counter += 1
		d_counter = 0

	if len(prefix) > 0:
		node_tag = prefix + "::" + node.tag.strip()
	else:
		node_tag = "\n" + node.tag.strip()
	if isinstance(node.text, str):
		if len(node.text.strip()) > 0:
			node_text = " = " + node.text.strip()
	node_tag += node_text
	if len(node_tag.strip()) > 0:
		out_str = "\n" + node_tag.strip()
		if isRoot:
			isRoot = False
			out_str = node.tag.strip()
	for child in node:
		parseXML(child, node_tag)

class node:
	stmtName = None
	lineTupleSize = None
	nodeType = None
	dataName = None
	nSubType = None
	nodeValue = None
	line = None
	regionType = None
	regionName = None

globalStmtCounter = 0

'''
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
'''
def parseLine(line, regionType, regionName):
	global globalStmtCounter

	# if not regionType == "FUNC":
	# 	print(regionType)
	# 	sys.exit()

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
		# sys.exit()

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
				n.nodeValue.append(new_str)
				new_str = ""

			firstIter = False

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
		# print("lineTuple: " + str(len(lineTuple)))
		# print("n.lineTupleSize: " + str(n.lineTupleSize))

		if n.lineTupleSize == 8:
			n.nSubType = lineTuple[3]
			n.nodeValue = [str(lineTuple[3]+lineTuple[5]+lineTuple[7])]
		if n.lineTupleSize == 11:
			n.nSubType = lineTuple[3]
			n.nodeValue = [str(lineTuple[3]+lineTuple[5]+lineTuple[7]+"."+lineTuple[-1])]
		if n.lineTupleSize == 9 or n.lineTupleSize == 10:
			n.nSubType = lineTuple[3]
			n.nodeValue = [str(lineTuple[3]+lineTuple[5]+lineTuple[7])]

	return n

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

def scanFunctionsDirectVarAccess(keysList, startEndRegions, dirctVarsDict):
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
		print(regionName)

		if not (firstLine.startswith("(FUNC, ") or firstLine.startswith("(PROG, ")):
			continue
		
		if not regionName in declFunctions:
			declFunctions.append(regionName)
			funcDeclVars[regionName] = {}

		regionlines = IRlines[rStart:rEnd]

		for line in regionlines:
			n = parseLine(line, regionType, regionName)
			split_line = line[1:-1].split(", ")
			if regionName == "Main" and line.startswith("(fb-invocation, ") and split_line[1].endswith("_DB"):
				if not "Main" in funcDeclVars.keys():
					funcDeclVars[regionName] = {}

				fb_invocation_var = split_line[1]
				funcDeclVars[regionName][fb_invocation_var] = fb_invocation_var[:-3]
					
			
			for dv in dirctVarsDict.keys():
				stmtSrcDst = split_line[2:]
				# print(stmtSrcDst)

				if n.nodeType == "ASSIGNMENT" and dv in stmtSrcDst:
					if dv in funcDeclVars[regionName].keys():
						# if stmtSrcDst[0] == dv:
						if dv in n.dataName:
							if not "dst" in funcDeclVars[regionName][dv]:
								funcDeclVars[regionName][dv].append("dst")
						# if stmtSrcDst[1] == dv:
						if dv in n.nodeValue:
							if not "src" in funcDeclVars[regionName][dv]:
								funcDeclVars[regionName][dv].append("src")
					else:
						# if stmtSrcDst[0] == dv:
						if dv in n.dataName:
							funcDeclVars[regionName][dv] = ["dst"]
						# if stmtSrcDst[1] == dv:
						if dv in n.nodeValue:
							funcDeclVars[regionName][dv] = ["src"]

				# if n.nodeType == "IVAR" and dv in stmtSrcDst:
				if n.nodeType == "IVAR" and dv in n.nodeValue:
					if dv in funcDeclVars[regionName].keys():
						if not "src" in funcDeclVars[regionName][dv]:
							funcDeclVars[regionName][dv].append("src")
					else:
						funcDeclVars[regionName][dv] = ["src"]

	
	return declFunctions, funcDeclVars

added_lines_list = ["(DIRECT_VARS, start)"]
def instrument_ir_prog(IRlines, declFunctions, funcDeclVars, dirctVarsDict):
	global d_counter, globalFuncVars, added_lines

	d_counter = 0
	added_lines = 0 # we use 1 if include the first line
	IRlines_result = IRlines[:]

	for i in range(0, len(IRlines)):
		line = IRlines[i]

		if not (line.startswith("(FUNC, ") or line.startswith("(PROG, ")):
			continue

		split_line = line[1:-1].split(", ")
		regionName = split_line[1]
		# print(regionName)
		


		if regionName in declFunctions:
			# print(funcDeclVars[regionName])

			if regionName == "Main":
				funcDirectVars = funcDeclVars[regionName].keys()
				for k in funcDirectVars:
					fb_invocation_func = funcDeclVars[regionName][k]
					out_str1 = ""
					out_str1 += "(var-declarations, "
					out_str1 += k + ", "
					out_str1 += fb_invocation_func + ")"
					
					IRlines_result = IRlines_result[:i+1+added_lines] + [out_str1] + IRlines_result[i+1+added_lines:]
					added_lines += 1

			elif len(funcDeclVars[regionName].keys()) > 0:
				funcDirectVars = funcDeclVars[regionName].keys()
				for k in funcDirectVars:
					# print(k)
					# sys.exit()
					# print(regionName + ": " + k + ": " + str(funcDeclVars[regionName][k]))
					if k in globalFuncVars:
						continue
					varFields = dirctVarsDict[k][-1]
					# print(varFields)

					out_str1 = ""
					out_str1 += "(direct-variable, d" + str(d_counter) + "*, location-prefix, " + varFields[1] + ", size-prefix, "
					out_str1 += varFields[2]
					out_str1 += varFields[3]

					out_str2 = "("
					out_str2 += "var-declarations, "

					# the piece below is not correct, directt-variable pointers always get var-declarations
					# otherwise they will be confused with function parameters (FormalIn,... etc)
					# if "src" in funcDeclVars[regionName][k] and "dst" in funcDeclVars[regionName][k]:
					# 	out_str2 += "input-output-declarations, "
					# elif "src" in funcDeclVars[regionName][k]:
					# 	out_str2 += "input-declarations, "
					# elif "dst" in funcDeclVars[regionName][k]:
					# 	out_str2 += "output-declarations, "

					out_str2 += k + ", "
					out_str2 += "d" + str(d_counter)  + "*" + ", "
					varType = dirctVarsDict[k][-3]
					out_str2 += varType + ")"
					# print(out_str1)
					# print(out_str2)
					added_lines_list.append(out_str1)
					added_lines_list.append(out_str2)
					# IRlines_result = IRlines_result[:i+1+added_lines] + [out_str1 , out_str2] + IRlines_result[i+1+added_lines:]
					# added_lines += 2

					d_counter += 1
					globalFuncVars.append(k)
	IRlines_result = added_lines_list[:] + IRlines_result[:]
	return IRlines_result


def main():
	global IRlines, added_lines, ir_input, plctags_input, output_f

	ir_file = open(ir_input, "r")
	IRlines = ir_file.readlines()
	IRlines = [x.strip() for x in IRlines]
	ir_file.close()

	tree = ET.parse(plctags_input)
	root = tree.getroot()

	parseXML(root)
	# print(dirctVarsDict)
	# sys.exit()

	startEndRegions = findRegions(IRlines)

	keysList = list(startEndRegions.keys())
	declFunctions = []
	funcDeclVars = {}

	declFunctions, funcDeclVars = scanFunctionsDirectVarAccess(keysList, startEndRegions, dirctVarsDict)

	# print(funcDeclVars)
	# sys.exit()
	IRlines_result = instrument_ir_prog(IRlines, declFunctions, funcDeclVars, dirctVarsDict)
	# print("*************************************")
	# print(added_lines_list)
	result_ir_file = open(output_f, "w")
	
	for line in IRlines_result:
		result_ir_file.write(line + "\n")
	result_ir_file.close()

if __name__ == "__main__":
    main()