import time
import re
import xml.etree.ElementTree as ET

input_file = 'chemical_plant.xml'
o_f_preprocessAST = open("preprocessAST.txt", "w")
o_f_IR = open("IR.txt", "w")
isRoot = True

start_time = time.time()

def parseXML(node, prefix=""):
	global isRoot, o_f_preprocessAST
	node_tag = node.tag.strip()
	node_text = ""

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
		o_f_preprocessAST.write(out_str)


	for child in node:
		parseXML(child, node_tag)

def getStmtLR(stmt):
	if not " = " in stmt:
		return "", ""

	split_stmt = stmt.split(" = ")
	if len(split_stmt) == 1:
		return split_stmt[0], ""
	elif len(split_stmt) == 2:
		return split_stmt[0], split_stmt[1]

	return "", ""


def getStmtL(stmt):
	if not " = " in stmt:
		return stmt

	split_stmt = stmt.split(" = ")

	if len(split_stmt) == 2:
		return split_stmt[0]

	return ""

def getStmtR(stmt):
	split_stmt = stmt.split(" = ")

	if len(split_stmt) == 2:
		return split_stmt[1]

	return ""


def identifyBlocks(pASTlines):
	blockRanges = {}
	
	for i in range(0, len(pASTlines)):
		i_line = pASTlines[i]
		i_lstmt = getStmtL(i_line)
		blockRanges[i] = i

		for j in range(i+1, len(pASTlines)):
			j_line = pASTlines[j]
			j_lstmt = getStmtL(j_line)
			if i_lstmt in j_lstmt:
				if len(i_lstmt) >= len(j_lstmt):
					break
				blockRanges[i] = j
			else:
				break

	return blockRanges

def getBlockType(line):
	lstmt = getStmtL(line)
	if not "::" in lstmt:
		return lstmt
	else:
		return lstmt.split("::")[-1]

	return ""


def isTranslatable(blockType):
	transBlockTypes = ["derived-function-block-name", "var-init-decl", "expression", "assignment-statement",
	"function-call", "fb-invocation", "program-type-name", "configuration-name", "resource-name",
	"direct-variable", "program-configuration", "task-configuration", "task-initialization"] # 
	if blockType in transBlockTypes:
		return True

	return False

def hasInnerBlock(line):
	if isTranslatable(getBlockType(line)):
		return True # +1 to cover up the jumped over first line in the current block
	return False

def getInnerBlockEndIndex(blockType, blockLines, index=0):
	if isTranslatable(blockType):
		innerBlockEndIndex = identifyBlocks(blockLines)[index]
		return innerBlockEndIndex
	return -1


def processBlock(blockType, blockLines, index=0, prefix=""):
	result = ""

	if index >= len(blockLines):
		# if blockType == "direct-variable":
		# 	return ""
		return ")"

	currentLine = blockLines[index]

	if index > 0: # jump over the current block's first line
		if hasInnerBlock(currentLine):
			innerBlockType = getBlockType(currentLine)
			startIndex = index
			endIndex = getInnerBlockEndIndex(innerBlockType, blockLines, index)
			if endIndex == -1:
				print("ERROR: getInnerBlockEndIndex() returned -1!")

			result += ", " + processBlock(innerBlockType, blockLines[startIndex:endIndex+1])

			index = endIndex + 1 # jump over the inner block
			if index >= len(blockLines):
				return result + ")"
			currentLine = blockLines[index]

	if blockType == "derived-function-block-name":
		if index == 0:
			rstmt = getStmtR(currentLine)
			result += "(FUNC, " +  rstmt + processBlock(blockType, blockLines, index+1)
			return result

	if blockType == "configuration-name":
		if index == 0:
			rstmt = getStmtR(currentLine)
			result += "(CONFIG, " +  rstmt + processBlock(blockType, blockLines, index+1)
			return result

	if blockType == "resource-name":
		if index == 0:
			rstmt = getStmtR(currentLine)
			result += "(RES, " +  rstmt + processBlock(blockType, blockLines, index+1)
			return result

	if blockType == "expression":
		if index == 0:
			result += "(EXP"
		else:
			rstmt = getStmtR(currentLine)
			if len(rstmt) > 0:
				result += ", " + rstmt
			else:
				operator = currentLine.split("expression::")[-1]
				ignoreOperators = ["expression", "function-call::param-assignment", "time-literal", "time-literal::duration"]
				if not operator in ignoreOperators:
					result += ", " + operator.split("::")[-1]

	if blockType == "function-call":
		if index == 0:
			stmtType = currentLine.split("::")[-1]
			result += "(" + stmtType
		else:
			rstmt = getStmtR(currentLine)
			if len(rstmt) > 0:
				result += ", " + rstmt
			else:
				operator = currentLine.split("expression::")[-1]
				ignoreOperators = ["expression", "function-call::param-assignment", "param-assignment"]
				if not operator in ignoreOperators:
					result += ", " + operator
	
	if blockType == "fb-invocation":
		if index == 0:
			stmtType = currentLine.split("::")[-1]
			result += "(" + stmtType
		else:
			rstmt = getStmtR(currentLine)
			if len(rstmt) > 0:
				result += ", " + rstmt
			else:
				operator = currentLine.split("::")[-1]
				ignoreOperators = ["expression", "param-assignment"]
				if not operator in ignoreOperators:
					result += ", " + operator

	if blockType == "program-type-name":
		if "program-declaration::program-type-name" in currentLine:
			rstmt = getStmtR(currentLine)
			result += "(PROG, " +  rstmt + processBlock(blockType, blockLines, index+1)
		else:
			lstmt, rstmt = getStmtLR(currentLine)
			if len(lstmt) > 0 and len(rstmt) > 0:
				result += lstmt.split("::")[-1] + ", " + rstmt.split("::")[-1]
		return result		

	if blockType == "program-configuration": 
		if index == 0:
			stmtType = currentLine.split("::")[-1]
			result += "(" + stmtType # + processBlock(blockType, blockLines, index+1)
		else:
			lstmt, rstmt = getStmtLR(currentLine)
			if len(lstmt) > 0 and len(rstmt) > 0:
				result += ", " + lstmt.split("::")[-1] + ", " + rstmt.split("::")[-1]

	if blockType == "task-configuration" or blockType == "task-initialization":
		if index == 0:
			stmtType = currentLine.split("::")[-1]
			result += "(" + stmtType # + processBlock(blockType, blockLines, index+1)
		else:
			lstmt, rstmt = getStmtLR(currentLine)
			if len(lstmt) > 0 and len(rstmt) > 0:
				result += ", " + lstmt.split("::")[-1] + ", " + rstmt.split("::")[-1]

	if blockType == "direct-variable":
		if index == 0:
			# print("----")
			# print(blockLines)
			stmtType = currentLine.split("::")[-1]
			result += "(" + stmtType  # + processBlock(blockType, blockLines, index+1)
		else:
			lstmt, rstmt = getStmtLR(currentLine)
			if len(lstmt) > 0 and len(rstmt) > 0:
				result += ", " + lstmt.split("::")[-1] + ", " + rstmt.split("::")[-1]

	if blockType == "assignment-statement":
		if index == 0:
			result += "(ASSIGNMENT, "

		rstmt = getStmtR(currentLine)
		if len(rstmt) > 0:
			result += rstmt

		if "-type-name::type-" in currentLine:
			result += ", " + currentLine.split("-type-name::type-")[-1]

	if blockType == "var-init-decl":
		if index == 0:
			varType = currentLine.split("::")[-2]
			result += "(" + varType

		rstmt = getStmtR(currentLine)
		if len(rstmt) > 0:
			result += ", " +  rstmt

		if "-type-name::type-" in currentLine:
			result += ", " + currentLine.split("-type-name::type-")[-1]
		elif "-type-name = " in currentLine:
			result += ", " + currentLine.split("-type-name = ")[-1]

	return result + processBlock(blockType, blockLines, index+1)

ivar_c = 0
operators = ["elevated-by", "plus", "minus", "logical-not", "multiply-with", "divide-by", "modulo", "adding",
	"subtracting", "equals", "equals-not", "less-or-equal", "greater-or-equal", "less-than", "greater-than",
	"logical-or", "logical-xor", "logical-and"]

def subOperator(stmt):
	global operators
	global ivar_c
	oIndex = 0
	foundOperator = ""
	splittedStmt = stmt.split(", ")
	new_stmt = ""
	mod_stmt = ""

	for operator in operators:
		oIndex = 0
		if operator in splittedStmt:
			for word in splittedStmt:
				if word == operator:
					foundOperator = word
					break
				oIndex += 1
			if len(foundOperator) > 0:
				break

	if len(foundOperator) > 0:
		ivarName = "r" + str(ivar_c)
		ivar_c += 1
		if foundOperator in ["plus", "minus", "logical-not"]: # unary operators
			new_stmt = "(IVAR, " + ivarName + ", " + splittedStmt[oIndex] + ", " + splittedStmt[oIndex+1] + ")\n"
			mod_stmt = ', '.join(splittedStmt[:oIndex]) + ", " + ivarName# + "\n"
		else:
			new_stmt = "(IVAR, " + ivarName + ", " + splittedStmt[oIndex-1] + ", " + splittedStmt[oIndex] + ", " + splittedStmt[oIndex+1] + ")\n"
			mod_stmt = ', '.join(splittedStmt[:oIndex-1])
		if oIndex+2 < len(splittedStmt):
			mod_stmt += ivarName + ", " + ', '.join(splittedStmt[oIndex+2:])
		else:
			 mod_stmt += ", " + ivarName# + "\n"
		# mod_stmt += ', '.join(splittedStmt[oIndex+2:])
	return new_stmt, mod_stmt

def countOperators(stmt):
	global operators
	operators_c = 0

	for word in stmt.split(", "):
		if word in operators:
			operators_c += 1
			continue

	return operators_c

def simplifyExpressionOperators(stmt, level=0):
	global ivar_c
	new_stmt = ""
	mod_stmt = stmt

	if not "(IVAR, " in stmt:
		return stmt

	pattern = '(\(IVAR, r[0-9]+, )([^\(\)]+)(\))'
	reCompiler = re.compile(pattern)
	for matchedPattern in reCompiler.finditer(stmt):
	    expression = matchedPattern.group(2)
	    nOperators = countOperators(expression)
	    if nOperators > 1:
	    	splittedExpression = expression.split(", ")
	    	tmp_new_stmt, tmp_mod_stmt = subOperator(expression)
	    	new_stmt += tmp_new_stmt
	    	mod_stmt = stmt[:matchedPattern.start()] + tmp_new_stmt + matchedPattern.group(1) + tmp_mod_stmt + matchedPattern.group(3) + stmt[matchedPattern.end():]

	    	nOperators = countOperators(expression)
	    	if nOperators > 1:
	    		mod_stmt = simplifyExpressionOperators(mod_stmt, level+1)
	
	return mod_stmt
	
toSimplify = [", (function-call, ", ", (task-initialization, ", ", (direct-variable, "]

def toSimplifyExp(stmt):
	global toSimplify

	for expType in toSimplify:
		if expType in stmt:
			return expType
	return False

def isSimplifiable(stmt):
	global toSimplify

	for expType in toSimplify:
		if expType in stmt:
			return True, 
	return False

def simplifyExpression(stmt, level=0):
	global ivar_c, toSimplify
	new_stmt = stmt

	if not isSimplifiable(stmt) and not "(EXP, " in stmt:
		return stmt
	
	if "(EXP, " in stmt:
		pattern = '(\(EXP, )([^\(\)]+)(\))'
		reCompiler = re.compile(pattern)
		for matchedPattern in reCompiler.finditer(stmt):
		    ivarName = "r" + str(ivar_c)
		    ivar_c += 1
		    '''
		    new_stmt = "(IVAR, " + ivarName + ", " + matchedPattern.group(2) + ")"
		    if not (len(stmt[:matchedPattern.start()]) == 0 and len(stmt[matchedPattern.end():]) == 0):
		    	new_stmt += "\n" + stmt[:matchedPattern.start()] + ivarName + stmt[matchedPattern.end():]
		    # comment this, and uncomment the above if you want more IVARs!
		    # if not (len(stmt[:matchedPattern.start()]) == 0 and len(stmt[matchedPattern.end():]) == 0):
		    # 	new_stmt = stmt[:matchedPattern.start()] + matchedPattern.group(2) + stmt[matchedPattern.end():]
		    '''
		    if len(matchedPattern.group(2).split()) == 1:
		    	if not (len(stmt[:matchedPattern.start()]) == 0 and len(stmt[matchedPattern.end():]) == 0):
		    		new_stmt = stmt[:matchedPattern.start()] + matchedPattern.group(2) + stmt[matchedPattern.end():]
		    else:
		    	new_stmt = "(IVAR, " + ivarName + ", " + matchedPattern.group(2) + ")"
		    	if not (len(stmt[:matchedPattern.start()]) == 0 and len(stmt[matchedPattern.end():]) == 0):
		    		new_stmt += "\n" + stmt[:matchedPattern.start()] + ivarName + stmt[matchedPattern.end():]

	if  isSimplifiable(stmt):
		toSimplifyExpression = toSimplifyExp(stmt)
		pattern = "(\(" + toSimplifyExpression[3:] + ")([^\(\)]+)(\))"
		reCompiler = re.compile(pattern)
		for matchedPattern in reCompiler.finditer(stmt):
			ivarName = "r" + str(ivar_c)
			ivar_c += 1
			new_stmt = toSimplifyExpression[2:] + ivarName + ", " + matchedPattern.group(2) + ")\n"
			new_stmt += stmt[:matchedPattern.start()] + ivarName + stmt[matchedPattern.end():]

	if isSimplifiable(stmt) or "(EXP, " in stmt:
		new_stmt = simplifyExpression(new_stmt, level+1)

	if level == 0:
		new_stmt_list = new_stmt.splitlines(True)
		new_stmt_list.reverse()
		new_stmt = ''.join(new_stmt_list[1:])
		new_stmt += new_stmt_list[0]
		new_stmt = simplifyExpressionOperators(new_stmt)

	return new_stmt

def genIR(pASTlines):
	global o_f_IR

	blockRanges = identifyBlocks(pASTlines)
	lastIndexParsed = 0

	for i in range(0, len(pASTlines)):
		line = pASTlines[i]
		blockType = getBlockType(line)
		if i >= lastIndexParsed:
			if isTranslatable(blockType):
				lastIndexParsed = blockRanges[i]+1
				blockLines = pASTlines[i:lastIndexParsed]
				stmt = processBlock(blockType, blockLines)
				# if "location-prefix, Q" in stmt:
				# 	print(stmt)

				stmt = simplifyExpression(stmt)

				if "location-prefix, Q" in stmt:
					print("====")
					print(stmt)

				# toClean = "), "
				# if toClean in stmt:
				# 	print("====")
				# 	print(stmt)
				# 	stmt = stmt.replace(toClean, ", ")
				# 	print(stmt)
				o_f_IR.write(stmt + "\n")

def scanDefinedFunctions(irLines):
	defFunctions = []

	for line in irLines:
		lineTuple = tuple(line[1:-1].split(", "))
		if lineTuple[0] == "FUNC" or lineTuple[1] == "PROG":
			if not lineTuple[0] in defFunctions:
				defFunctions.append(lineTuple[1])
	
	return defFunctions


def scanNonDefFunctions(irLines, defFunctions):
	nonDefFunctions = []

	for i in range(0, len(irLines)):
		lineTuple = tuple(irLines[i][1:-1].split(", "))
		if "-declarations" in lineTuple[0]:
			if not lineTuple[2] in defFunctions and not lineTuple[2] in nonDefFunctions:
				for j in range(i+1, len(irLines)):
					jLineTuple = tuple(irLines[j][1:-1].split(", "))
					# new region, escape
					if jLineTuple[0] == "FUNC" or jLineTuple[0] == "PROG":
						break

					if jLineTuple[0] == "fb-invocation":
						if jLineTuple[1] == lineTuple[1]:
							nonDefFunctions.append(lineTuple[2])
							break
	
	return nonDefFunctions


def getFuncIRLines(irLines, func):
	funcIRLines = []
	funcPointers = []
	funcInVars = []
	funcOutVars = []

	for line in irLines:
		lineTuple = tuple(line[1:-1].split(", "))

		# new region, reset collected pointers
		if lineTuple[0] == "FUNC" or lineTuple[0] == "PROG":
			funcPointers = []

		if "-declarations" in lineTuple[0]:
			if lineTuple[2] == func:
				funcPointers.append(lineTuple[1])

		if lineTuple[0] == "fb-invocation":
			for p in funcPointers:
				if p == lineTuple[1]:
					for i in range(2, len(lineTuple), 2):
						if not lineTuple[i] in funcInVars:
							funcInVars.append(lineTuple[i])
					break

		if lineTuple[0] == "IVAR":
			if len(lineTuple) == 6:
				if lineTuple[2] == "multi-element-variable":
					for p in funcPointers:
						if p == lineTuple[3]:
							if not lineTuple[5] in funcOutVars:
								funcOutVars.append(lineTuple[5])
							break

	funcIRLines.append("(FUNC, " + func + ")")

	if not len(funcInVars) == 0 or not len(funcOutVars) == 0:
		for inVar in funcInVars:
			funcIRLines.append("(input-declarations, " + inVar + ", type)")
		for outVar in funcOutVars:
			funcIRLines.append("(output-declarations, " + outVar + ", type)")
	
	return funcIRLines

def genLibFunctionsIRStmts():
	global o_f_IR

	o_f_IR.close()
	
	i_f_IR = open("IR.txt", "r")
	irLines = i_f_IR.readlines()
	i_f_IR.close()
	irLines = [x.strip() for x in irLines]
	libFuncsIRLines = []

	defFunctions = scanDefinedFunctions(irLines)

	nonDefFunctions = scanNonDefFunctions(irLines, defFunctions)
	for f in nonDefFunctions:
		funcIRLines = getFuncIRLines(irLines, f)
		libFuncsIRLines += funcIRLines

	return libFuncsIRLines

def prependLibIRlines(libFuncsIRLines):
	i_f_IR = open("IR.txt", "r")
	irLines = i_f_IR.readlines()
	i_f_IR.close()

	o_f_IR = open("IR.txt", "w")
	for stmt in libFuncsIRLines:
		o_f_IR.write(stmt + "\n")
	for stmt in irLines:
		o_f_IR.write(stmt)

	o_f_IR.close()



def main():
	global o_f_preprocessAST, input_file

	tree = ET.parse(input_file)
	# tree = ET.parse('simplified_te.xml') # requires if-else implementation
	root = tree.getroot()
	
	parseXML(root) # generate preprocessAST
	o_f_preprocessAST.close()
	
	o_f_preprocessAST = open("preprocessAST.txt", "r")
	pASTlines = o_f_preprocessAST.readlines()
	pASTlines = [x.strip() for x in pASTlines]
	
	genIR(pASTlines)

	libFuncsIRLines = genLibFunctionsIRStmts()

	prependLibIRlines(libFuncsIRLines)

if __name__ == "__main__":
    main()

print("--- %s seconds ---" % (time.time() - start_time))