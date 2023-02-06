import re
import xml.etree.ElementTree as ET
import sys
import time

start_time = time.time()

sys.setrecursionlimit(999999999) # 5000

input_file = 'ft.xml'
# input_file = 'chemical_plant.xml'
o_f_preprocessAST = open("preprocessAST.txt", "w")
o_f_IR = open("IR.txt", "w")
isRoot = True

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

			# if i_lstmt in j_lstmt:
			# 	if len(i_lstmt) >= len(j_lstmt):
			# 		break
			# 	blockRanges[i] = j
			# else:
			# 	break

			if (i_lstmt in j_lstmt) and (not i_lstmt == j_lstmt):
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


def isTranslatable(blockType): # "function-block-declaration", 
	transBlockTypes = ["derived-function-block-name", "var-init-decl", "expression", "assignment-statement",
	"function-call", "fb-invocation", "program-type-name", "configuration-name", "resource-name",
	"direct-variable", "program-configuration", "task-configuration", "task-initialization", "structure-type-name", "structure-element-declaration", "if-statement", "data-block-declaration"] #, "case-statement" , "statement-list", "statement-list"
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


# last_sl_Count = 0
# last_if_Count = 0
# last_as_Count = 0

# last_cs_Count = 0
# last_ce_Count = 0
# last_cl_Count = 0
# last_cle_Count = 0

# last_exp_Count = 0
# last_fbi_Count = 0
# last_fc_Count = 0
def processBlock(blockType, blockLines, index=0, prefix=""):
	# global last_sl_Count, last_if_Count, last_as_Count, last_cs_Count, last_ce_Count, last_cl_Count, last_cle_Count, last_exp_Count, last_fbi_Count, last_fc_Count

	currentLine = blockLines[0]

	# last_sl_Count = currentLine[:currentLine.rfind("::")].count("statement-list") # 0
	# last_if_Count = currentLine[:currentLine.rfind("::")].count("if-statement") # 0
	# last_as_Count = currentLine[:currentLine.rfind("::")].count("assignment-statement") # 0
	# last_cs_Count = currentLine[:currentLine.rfind("::")].count("case-statement") # 0
	# last_ce_Count = currentLine[:currentLine.rfind("::")].count("case-element") # 0
	# last_cl_Count = currentLine[:currentLine.rfind("::")].count("case-list") # 0
	# last_cle_Count = currentLine[:currentLine.rfind("::")].count("case-list-element") # 0
	# last_exp_Count = currentLine[:currentLine.rfind("::")].count("::expression") # 0
	# last_fbi_Count = currentLine[:currentLine.rfind("::")].count("fb-invocation") # 0
	# last_fc_Count = currentLine[:currentLine.rfind("::")].count("function-call") # 0

	firstLine_len = len(currentLine) # currentLine.rfind("::")
	last_sl_Count 	= 0 # currentLine[firstLine_len:].count("::statement-list") # 0
	last_if_Count 	= 0
	last_as_Count 	= 0
	last_cs_Count 	= 0
	last_ce_Count 	= 0
	last_cl_Count 	= 0
	last_cle_Count 	= 0
	last_exp_Count 	= 0
	last_fbi_Count 	= 0
	last_fc_Count 	= 0
	last_fs_Count 	= 0
	last_fl_Count 	= 0

	result = ""
	FirstLineInBlock = True
	blockStack = []
	currentBlockType = blockType
	currentStartIndex = 0
	CurrentEndIndex = len(blockLines)
	# blockStack.push((currentBlockType, currentStartIndex, CurrentEndIndex))
	# print("MAIN: " + blockType)
	lastCommandOutput = ""

	# print("=======")
	# print(blockLines)

	while True:
		# print(index)
		# if index == CurrentEndIndex:

		if index >= len(blockLines):
			# result += ")"
			# result = result.replace("\n, ", "\n", result.count("\n, "))
			openBracketsCount = result.count("(")
			closedBracketsCount = result.count(")")
			missingBrackets = openBracketsCount-closedBracketsCount
			for b in range(0, missingBrackets):
				result += ")"

			# if index >= CurrentEndIndex: #  and not len(blockLines) == CurrentEndIndex
			# 	result += ")"
			break

		if index == CurrentEndIndex: #  and not len(blockLines) == CurrentEndIndex
			# result += "*12)"
			# if currentBlockType == "if-statement":
			# 	result += "\n}\n"
			# print("KKKKKKKKKKKKKKK")
			# print("currentBlockType = " + currentBlockType)
			# if not currentStartIndex == 0:
			# 	result += ")"
			# if currentBlockType == "if-statement":
			# 	print("SSSS")
			# 	result += ")"
				# sys.exit()

			# if len(lastCommandOutput) > 0:
			# 	result += ")"

			if len(blockStack) > 0:
				# if "case" in currentBlockType:
				# 	print(currentBlockType)
				# 	sys.exit()

				# print("currentBlockType = " + currentBlockType)
				value = blockStack.pop()
				# print("Pop: " + str(value))
				# result += ")"
				currentBlockType = value[0]
				currentStartIndex = value[1]
				CurrentEndIndex = value[2]
				# print("currentBlockType = " + currentBlockType)
				# print("currentStartIndex = " + str(currentStartIndex))
				# print("CurrentEndIndex = " + str(CurrentEndIndex))
				# print("blockLines = " + str(blockLines[currentStartIndex:CurrentEndIndex]))
				# if index == CurrentEndIndex:
					# result += "*13)"
				# if index == CurrentEndIndex:
				# 	result += ")"
				# print("lastCommandOutput = " + lastCommandOutput)

				sl_index = result.rfind("(ASSIGNMENT")
				# if not ("statement-list" or "if-statement") in result[sl_index:]:
				# and not "ASSIGNMENT" in result[sl_index:]
				# and not "assignment-statement" in result[sl_index:]
				if not "statement-list" in result[sl_index:] and not "if-statement" in result[sl_index:] and not "function-call" in result[sl_index:] and not "EXP" in result[sl_index:]:
					openBracketsCount = result[sl_index:].count("(")
					closedBracketsCount = result[sl_index:].count(")")
					missingBrackets = openBracketsCount-closedBracketsCount

					# for b in range(0, missingBrackets):
					# 	result += ")"
		

		currentLine = blockLines[index]

		cur_sl_Count = currentLine[firstLine_len:].count("::statement-list")
		if (cur_sl_Count < last_sl_Count): #  or (cur_sl_Count == last_sl_Count and currentLine.endswith("::statement-list"))
			# result += "*1)"
			missing_brackets = last_sl_Count-cur_sl_Count
			if missing_brackets == 0:
				missing_brackets = 1

			for i in range(0, missing_brackets):
				result += ")"
		last_sl_Count = cur_sl_Count

		cur_fs_Count = currentLine[firstLine_len:].count("::for-statement")
		if (cur_fs_Count < last_fs_Count): #  or (cur_sl_Count == last_sl_Count and currentLine.endswith("::for-statement"))
			# result += "*1)"
			missing_brackets = last_fs_Count-cur_fs_Count
			if missing_brackets == 0:
				missing_brackets = 1

			for i in range(0, missing_brackets):
				result += ")"
		last_fs_Count = cur_fs_Count

		cur_fl_Count = currentLine[firstLine_len:].count("::for-list")
		if (cur_fl_Count < last_fl_Count): #  or (cur_sl_Count == last_sl_Count and currentLine.endswith("::for-statement"))
			# result += "*1)"
			missing_brackets = last_fl_Count-cur_fl_Count
			if missing_brackets == 0:
				missing_brackets = 1

			for i in range(0, missing_brackets):
				result += ")"
		last_fl_Count = cur_fl_Count

		cur_if_Count = currentLine.count("if-statement")
		if (cur_if_Count < last_if_Count) or (cur_if_Count == last_if_Count and currentLine.endswith("::if-statement")): # 
			# result += "*2)"
			missing_brackets = last_if_Count-cur_if_Count
			if missing_brackets == 0:
				missing_brackets = 1

			for i in range(0, missing_brackets):
				result += ")"
		last_if_Count = cur_if_Count
		
		cur_as_Count = currentLine.count("assignment-statement")
		if (cur_as_Count < last_as_Count) or (cur_as_Count == last_as_Count and currentLine.endswith("::assignment-statement")): # 
			# result += "*3)"
			missing_brackets = last_as_Count-cur_as_Count

			if missing_brackets == 0:
				missing_brackets = 1

			for i in range(0, missing_brackets):
				result += ")"
		last_as_Count = cur_as_Count

		cur_cs_Count = currentLine.count("case-statement")
		if (cur_cs_Count < last_cs_Count): # or (cur_cs_Count == last_cs_Count and currentLine.endswith("::case-statement"))
			# result += "*4)"
			missing_brackets = last_cs_Count-cur_cs_Count
			if missing_brackets == 0:
				missing_brackets = 1
			
			for i in range(0, missing_brackets):
				result += ")"
		last_cs_Count = cur_cs_Count

		cur_ce_Count = currentLine.count("case-element")
		if (cur_ce_Count < last_ce_Count) or (cur_ce_Count == last_ce_Count and currentLine.endswith("::case-element")): #   
			# result += "*5)"
			missing_brackets = last_ce_Count-cur_ce_Count
			if missing_brackets == 0:
				missing_brackets = 1
			
			for i in range(0, missing_brackets):
				result += ")"
		last_ce_Count = cur_ce_Count

		# cur_cl_Count = currentLine.count("case-list::")
		# if (cur_cl_Count < last_cl_Count): #  or (cur_cl_Count == last_cl_Count and currentLine.endswith("::case-list"))
		# 	# result += "*6)"
		# 	missing_brackets = last_cl_Count-cur_cl_Count
		# 	if missing_brackets == 0:
		# 		missing_brackets = 1
			
		# 	for i in range(0, missing_brackets):
		# 		result += ")"
		# last_cl_Count = cur_cl_Count

		# cur_cle_Count = currentLine.count("case-list-element::")
		# if (cur_cle_Count < last_cle_Count): #  or (cur_cle_Count == last_cle_Count and currentLine.endswith("::case-list-element"))
		# 	# result += "*7)"
		# 	missing_brackets = last_cle_Count-cur_cle_Count
		# 	if missing_brackets == 0:
		# 		missing_brackets = 1
			
		# 	for i in range(0, missing_brackets):
		# 		result += ")"
		# last_cle_Count = cur_cle_Count

		cur_exp_Count = currentLine.count("::expression")
		if (cur_exp_Count < last_exp_Count) or (cur_exp_Count == last_exp_Count and currentLine.endswith("::expression")): #  
			# result += "*8)"
			missing_brackets = last_exp_Count-cur_exp_Count
			if missing_brackets == 0:
				missing_brackets = 1

			for i in range(0, missing_brackets):
				result += ")"
		last_exp_Count = cur_exp_Count

		cur_fbi_Count = currentLine.count("::fb-invocation")
		if (cur_fbi_Count < last_fbi_Count) or (cur_fbi_Count == last_fbi_Count and currentLine.endswith("::fb-invocation")): #  
			# result += "*9)"
			missing_brackets = last_fbi_Count-cur_fbi_Count
			if missing_brackets == 0:
				missing_brackets = 1
			
			for i in range(0, missing_brackets):
				result += ")"
		last_fbi_Count = cur_fbi_Count

		cur_fc_Count = currentLine.count("::function-call")
		if (cur_fc_Count < last_fc_Count) or (cur_fc_Count == last_fc_Count and currentLine.endswith("::function-call")): #  
			# result += "*10)"
			missing_brackets = last_fc_Count-cur_fc_Count
			if missing_brackets == 0:
				missing_brackets = 1
			
			for i in range(0, missing_brackets):
				result += ")"
		last_fc_Count = cur_fc_Count

		# if currentLine.endswith("::assignment-statement"):
		# 	print("LINE ENDS WITH assignment-statement: " + currentLine)
		# 	print(blockLines)


		# if index == 0:
		# 	FirstLineInBlock = True
	
		# if index == 0:
		# 	print("===== " + blockType)
		# 	print(blockLines)
	
		# individually process inner blocks
		if index > 0: # jump over the current block's first line
			if hasInnerBlock(currentLine):
				value = (currentBlockType, currentStartIndex, CurrentEndIndex)
				# print("Push: " + str(value))
				blockStack.append(value)
				FirstLineInBlock = True
				innerBlockType = getBlockType(currentLine)
				currentBlockType = innerBlockType
				currentStartIndex = index
				CurrentEndIndex = getInnerBlockEndIndex(innerBlockType, blockLines, index)
				if CurrentEndIndex == -1:
					print("ERROR: getInnerBlockEndIndex() returned -1!")
					sys.exit()
				CurrentEndIndex += 1

				lastCommandOutput = ""

				# print("currentBlockType = " + currentBlockType)
				# print("currentStartIndex = " + str(currentStartIndex))
				# print("CurrentEndIndex = " + str(CurrentEndIndex))
				# print("blockLines = " + str(blockLines[currentStartIndex:CurrentEndIndex]))

				# result += ", " + processBlock(innerBlockType, blockLines[startIndex:endIndex+1])

				result += ", " 
	
				# index = endIndex + 1 # jump over the inner block
	
				# if index >= len(blockLines):
				# 	return result + ")"
	
				# currentLine = blockLines[index]
	
		if currentBlockType == "structure-type-name":
			if FirstLineInBlock:
				result += "(" + currentBlockType
				lastCommandOutput += currentBlockType
	
			rstmt = getStmtR(currentLine)
			if len(rstmt) > 0:
				result += ", " +  rstmt
				lastCommandOutput += rstmt
	
		if currentBlockType == "structure-element-declaration":
			# print(currentLine)
			if FirstLineInBlock:
				stmtType = currentLine.split("::")[-1]
				result += "(" + stmtType
				lastCommandOutput += stmtType
			else:
				stmtType = currentLine.split("::")[-1]
				if stmtType == "array-specification":
					result += ", ARRAY"
					lastCommandOutput += ", ARRAY"
				if stmtType == "subrange":
					result += ", SUBRANGE"
					lastCommandOutput += ", SUBRANGE"
	
			rstmt = getStmtR(currentLine)
			if len(rstmt) > 0:
				result += ", " +  rstmt
				lastCommandOutput += rstmt
	
		if currentBlockType == "if-statement":
			# print(currentLine)
	
			if FirstLineInBlock:
				# print("===== " + currentBlockType)
				# print(len(blockLines))
				# print(index)
				stmtType = currentLine.split("::")[-1]
				result += "(" + stmtType
				lastCommandOutput += stmtType
			else:
				rstmt = getStmtR(currentLine)
				if len(rstmt) > 0:
					# if not "ELSE" in rstmt:
					if True:
						result += ", " +  rstmt
						lastCommandOutput += rstmt
				else:
					operator = currentLine.split("::")[-1]
					ignoreOperators = ["expression", "param-assignment", "statement-list", "case-statement", "case-element", "case-list", "case-list-element", "if-statement", "assignment-statement", "for-statement", "for-list"] # "ELSE", 
					# print("!! " + operator)
					# if operator == "assignment-statement" or operator == "ASSIGNMENT":
					# 	print("!! " + operator)

					if not operator in ignoreOperators:
						result += ", " + operator
						lastCommandOutput += operator

					# if operator == "assignment-statement":
					# 	sl_index = result.rfind("(assignment-statement")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (assignment-statement"

					# if operator == "ASSIGNMENT":
					# 	sl_index = result.rfind("(ASSIGNMENT")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (ASSIGNMENT"

					if operator == "statement-list":
						result += ", (statement-list"
						lastCommandOutput += "(statement-list"
						# result += ")\n"
						# lastCommandOutput += ")\n"
						# result = result.replace("\n, ", "\n", result.count("\n, "))
					if operator == "for-statement":
						result += ", (for-statement"
						lastCommandOutput += "(for-statement"
					if operator == "for-list":
						result += ", (for-list"
						lastCommandOutput += "(for-list"
					if operator == "if-statement":
						result += ", (if-statement"
						lastCommandOutput += "(if-statement"
					if operator == "case-statement":
						# print("CASE: " + currentLine)
						result += ", (case-statement"
						lastCommandOutput += "(case-statement"
					if operator == "case-element":
						result += ", (case-element"
						lastCommandOutput += "(case-element"
					# if operator == "case-list":
					# 	result += ", (case-list"
					# 	lastCommandOutput += "(case-list"
					# if operator == "case-list-element":
					# 	result += ", (case-list-element"
					# 	lastCommandOutput += "(case-list-element"
					
					# if operator == "statement-list":
					# 	# result += ")\n(statement-list"
					# 	# result += "), (statement-list"

					# 	sl_index = result.rfind("(statement-list")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (statement-list"

					# 	lastCommandOutput += ", (statement-list"
					# 	# result += ")\n"
					# 	# lastCommandOutput += ")\n"
					# 	# result = result.replace("\n, ", "\n", result.count("\n, "))
					# if operator == "case-statement":
					# 	# result += ")\n(case-statement"
					# 	# result += "), (case-statement"
					# 	print("CASE: " + currentLine)
					# 	sl_index = result.rfind("(case-statement")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-statement"
					# 	lastCommandOutput += ", (case-statement"
					# if operator == "if-statement":
					# 	sl_index = result.rfind("(if-statement")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (if-statement"
					# 	lastCommandOutput += "(if-statement"
					# if operator == "case-element":
					# 	sl_index = result.rfind("(case-element")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-element"
					# 	lastCommandOutput += "(case-element"
					# if operator == "case-list":
					# 	sl_index = result.rfind("(case-list")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-list"
					# 	lastCommandOutput += "(case-list"
					# if operator == "case-list-element":
					# 	sl_index = result.rfind("(case-list-element")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-list-element"
					# 	lastCommandOutput += "(case-list-element"
					
		# if currentBlockType == "statement-list":
		# 	# print(currentLine)
	
		# 	if FirstLineInBlock:
		# 		# print("===== " + currentBlockType)
		# 		# print(len(blockLines))
		# 		# print(index)
		# 		stmtType = currentLine.split("::")[-1]
		# 		result += "(" + stmtType
		# 		lastCommandOutput += stmtType
		# 	else:
		# 		rstmt = getStmtR(currentLine)
		# 		if len(rstmt) > 0:
		# 			result += ", " +  rstmt
		# 			lastCommandOutput += rstmt
		# 		else:
		# 			operator = currentLine.split("::")[-1]
		# 			ignoreOperators = ["expression", "param-assignment"] #, "statement-list"
		# 			# print("!! " + operator)
		# 			if not operator in ignoreOperators:
		# 				result += ", " + operator
		# 				lastCommandOutput += operator

		# if currentBlockType == "case-statement":
		# 	# print(currentLine)
			
		# 	if FirstLineInBlock:
		# 		# print("===== " + currentBlockType)
		# 		# print(blockLines)
		# 		stmtType = currentLine.split("::")[-1]
		# 		result += "(" + stmtType
	
		# 	rstmt = getStmtR(currentLine)
		# 	if len(rstmt) > 0:
		# 		result += ", " +  rstmt
	
		if currentBlockType == "derived-function-block-name":
			if FirstLineInBlock:
				rstmt = getStmtR(currentLine)
				result += "(FUNC, " +  rstmt # + processBlock(blockType, blockLines, index+1)
				# return result
		
		if currentBlockType == "data-block-declaration":
			if FirstLineInBlock:
				rstmt = getStmtR(currentLine)
				result += "\n(DATA_BLOCK" +  rstmt # + processBlock(blockType, blockLines, index+1)
				lastCommandOutput += rstmt
				# print(blockLines)
				# sys.exit()
			else:
				rstmt = getStmtR(currentLine)
				if len(rstmt) > 0:
					result += ", " + rstmt
					lastCommandOutput += rstmt

		if currentBlockType == "configuration-name":
			if FirstLineInBlock:
				rstmt = getStmtR(currentLine)
				result += "(CONFIG, " +  rstmt # + processBlock(blockType, blockLines, index+1)
				lastCommandOutput += rstmt
				# return result
	
		if currentBlockType == "resource-name":
			if FirstLineInBlock:
				rstmt = getStmtR(currentLine)
				result += "(RES, " +  rstmt # + processBlock(blockType, blockLines, index+1)
				lastCommandOutput += rstmt
				# return result
	
		if currentBlockType == "expression":
			if FirstLineInBlock:
				result += "(EXP"
			else:
				rstmt = getStmtR(currentLine)
				if len(rstmt) > 0:
					result += ", " + rstmt
					lastCommandOutput += rstmt
				else:
					# operator = currentLine.split("expression::")[-1]
					operator = currentLine.split("::")[-1]
					# print("*: " + operator)
					# if operator == "assignment-statement" or operator == "ASSIGNMENT":
					# 	print("!!2 " + operator)

					ignoreOperators = ["expression", "function-call::param-assignment", "time-literal", "time-literal::duration", "statement-list", "case-statement", "case-element", "case-list", "case-list-element", "if-statement", "assignment-statement", "for-statement", "for-list"] #, "statement-list"
					if not operator in ignoreOperators:
						# print("**: " + operator.split("::")[-1])
						result += ", " + operator.split("::")[-1]
						lastCommandOutput += operator.split("::")[-1]
					
					if operator == "statement-list":
						# result += ")\n(statement-list"
						# result += "), (statement-list"

						sl_index = result.rfind("(statement-list")
						openBracketsCount = result[sl_index:].count("(")
						closedBracketsCount = result[sl_index:].count(")")
						missingBrackets = openBracketsCount-closedBracketsCount
						# for b in range(0, missingBrackets):
						# 	if not "(if-statement" in result[sl_index:]:
						# 		result += ")"
						result += ", (statement-list"
						lastCommandOutput += ", (statement-list"

					if operator == "for-statement":
						result += ", (for-statement"
						lastCommandOutput += ", (for-statement"
					if operator == "for-list":
						result += ", (for-list"
						lastCommandOutput += ", (for-list"

					# if operator == "case-statement":
					# 	print("CASE: " + currentLine)
					# 	sl_index = result.rfind("(case-statement")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-statement"
					# 	lastCommandOutput += ", (case-statement"
					# if operator == "if-statement":
					# 	sl_index = result.rfind("(if-statement")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (if-statement"
					# 	lastCommandOutput += "(if-statement"
					# if operator == "case-element":
					# 	sl_index = result.rfind("(case-element")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-element"
					# 	lastCommandOutput += "(case-element"
					# if operator == "case-list":
					# 	sl_index = result.rfind("(case-list")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-list"
					# 	lastCommandOutput += "(case-list"
					# if operator == "case-list-element":
					# 	sl_index = result.rfind("(case-list-element")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-list-element"
					# 	lastCommandOutput += "(case-list-element"

					# if operator == "statement-list":
					# 	result += ", (statement-list"
					# 	lastCommandOutput += "(statement-list"
					# 	# result += ")\n"
					# 	# lastCommandOutput += ")\n"
					# 	# result = result.replace("\n, ", "\n", result.count("\n, "))
					# if operator == "if-statement":
					# 	result += ", (if-statement"
					# 	lastCommandOutput += "(if-statement"
					# if operator == "case-statement":
					# 	result += ", (case-statement"
					# 	lastCommandOutput += "(case-statement"
					# if operator == "case-element":
					# 	result += ", (case-element"
					# 	lastCommandOutput += "(case-element"
					# if operator == "case-list":
					# 	result += ", (case-list"
					# 	lastCommandOutput += "(case-list"
					# if operator == "case-list-element":
					# 	result += ", (case-list-element"
					# 	lastCommandOutput += "(case-list-element"
					
		
		if currentBlockType == "function-call":
			if FirstLineInBlock:
				stmtType = currentLine.split("::")[-1]
				result += "(" + stmtType
				lastCommandOutput += stmtType
			else:
				rstmt = getStmtR(currentLine)
				if len(rstmt) > 0:
					result += ", " + rstmt
					lastCommandOutput += rstmt
				else:
					# operator = currentLine.split("expression::")[-1]
					# if operator == "assignment-statement" or operator == "ASSIGNMENT":
					# 	print("!! " + operator)

					operator = currentLine.split("::")[-1]
					ignoreOperators = ["expression", "function-call::param-assignment", "param-assignment", "statement-list", "case-statement", "case-element", "case-list", "case-list-element", "if-statement", "assignment-statement", "for-statement", "for-list"] #, "statement-list"
					if not operator in ignoreOperators:
						# print("**: " + operator.split("::")[-1])
						result += ", " + operator.split("::")[-1]
						lastCommandOutput += operator.split("::")[-1]
					if operator == "assignment-statement":
						sl_index = result.rfind("(assignment-statement")
						openBracketsCount = result[sl_index:].count("(")
						closedBracketsCount = result[sl_index:].count(")")
						missingBrackets = openBracketsCount-closedBracketsCount
						# for b in range(0, missingBrackets):
						# 	result += ")"
						result += ", (assignment-statement"
						lastCommandOutput += ", (assignment-statement"

					if operator == "statement-list":
						# result += ")\n(statement-list"
						# result += "), (statement-list"

						sl_index = result.rfind("(statement-list")
						openBracketsCount = result[sl_index:].count("(")
						closedBracketsCount = result[sl_index:].count(")")
						missingBrackets = openBracketsCount-closedBracketsCount
						# for b in range(0, missingBrackets):
						# 	if not "(if-statement" in result[sl_index:]:
						# 		result += ")"
						result += ", (statement-list"

						lastCommandOutput += ", (statement-list"
						# result += ")\n"
						# lastCommandOutput += ")\n"
						# result = result.replace("\n, ", "\n", result.count("\n, "))
					if operator == "for-statement":
						result += ", (for-statement"
						lastCommandOutput += ", (for-statement"
					if operator == "for-list":
						result += ", (for-list"
						lastCommandOutput += ", (for-list"
					# if operator == "case-statement":
					# 	print("CASE: " + currentLine)
					# 	sl_index = result.rfind("(case-statement")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-statement"
					# 	lastCommandOutput += ", (case-statement"
					# if operator == "if-statement":
					# 	sl_index = result.rfind("(if-statement")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (if-statement"
					# 	lastCommandOutput += "(if-statement"
					# if operator == "case-element":
					# 	sl_index = result.rfind("(case-element")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-element"
					# 	lastCommandOutput += "(case-element"
					# if operator == "case-list":
					# 	sl_index = result.rfind("(case-list")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-list"
					# 	lastCommandOutput += "(case-list"
					# if operator == "case-list-element":
					# 	sl_index = result.rfind("(case-list-element")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-list-element"
					# 	lastCommandOutput += "(case-list-element"

					# if operator == "statement-list":
					# 	result += ", (statement-list"
					# 	lastCommandOutput += "(statement-list"
					# 	# result += ")\n"
					# 	# lastCommandOutput += ")\n"
					# 	# result = result.replace("\n, ", "\n", result.count("\n, "))
					# if operator == "if-statement":
					# 	result += ", (if-statement"
					# 	lastCommandOutput += "(if-statement"
					# if operator == "case-statement":
					# 	result += ", (case-statement"
					# 	lastCommandOutput += "(case-statement"
					# if operator == "case-element":
					# 	result += ", (case-element"
					# 	lastCommandOutput += "(case-element"
					# if operator == "case-list":
					# 	result += ", (case-list"
					# 	lastCommandOutput += "(case-list"
					# if operator == "case-list-element":
					# 	result += ", (case-list-element"
					# 	lastCommandOutput += "(case-list-element"
		
		if currentBlockType == "fb-invocation":
			if FirstLineInBlock:
				stmtType = currentLine.split("::")[-1]
				result += "(" + stmtType
				lastCommandOutput += stmtType
			else:
				rstmt = getStmtR(currentLine)
				if len(rstmt) > 0:
					result += ", " + rstmt
					lastCommandOutput += rstmt
				else:
					operator = currentLine.split("::")[-1]
					# if operator == "assignment-statement" or operator == "ASSIGNMENT":
					# 	print("!! " + operator)
					ignoreOperators = ["expression", "param-assignment", "statement-list", "case-statement", "case-element", "case-list", "case-list-element", "if-statement", "for-statement", "for-list"]
					if not operator in ignoreOperators:
						result += ", " + operator
						lastCommandOutput += operator
					
					if operator == "statement-list":
						result += ", (statement-list"
						lastCommandOutput += "(statement-list"
						# result += ")\n"
						# lastCommandOutput += ")\n"
						# result = result.replace("\n, ", "\n", result.count("\n, "))
					if operator == "for-statement":
						result += ", (for-statement"
						lastCommandOutput += ", (for-statement"
					if operator == "for-list":
						result += ", (for-list"
						lastCommandOutput += ", (for-list"
					if operator == "if-statement":
						result += ", (if-statement"
						lastCommandOutput += "(if-statement"
					if operator == "case-statement":
						result += ", (case-statement"
						lastCommandOutput += "(case-statement"
					if operator == "case-element":
						result += ", (case-element"
						lastCommandOutput += "(case-element"
					# if operator == "case-list":
					# 	result += ", (case-list"
					# 	lastCommandOutput += "(case-list"
					# if operator == "case-list-element":
					# 	result += ", (case-list-element"
					# 	lastCommandOutput += "(case-list-element"
					
					# if operator == "statement-list":
					# 	# result += ")\n(statement-list"
					# 	# result += "), (statement-list"

					# 	sl_index = result.rfind("(statement-list")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (statement-list"

					# 	lastCommandOutput += ", (statement-list"
					# 	# result += ")\n"
					# 	# lastCommandOutput += ")\n"
					# 	# result = result.replace("\n, ", "\n", result.count("\n, "))
					# if operator == "case-statement":
					# 	# result += ")\n(case-statement"
					# 	# result += "), (case-statement"
					# 	print("CASE: " + currentLine)
					# 	sl_index = result.rfind("(case-statement")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-statement"
					# 	lastCommandOutput += ", (case-statement"
					# if operator == "if-statement":
					# 	sl_index = result.rfind("(if-statement")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (if-statement"
					# 	lastCommandOutput += "(if-statement"
					# if operator == "case-element":
					# 	sl_index = result.rfind("(case-element")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-element"
					# 	lastCommandOutput += "(case-element"
					# if operator == "case-list":
					# 	sl_index = result.rfind("(case-list")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-list"
					# 	lastCommandOutput += "(case-list"
					# if operator == "case-list-element":
					# 	sl_index = result.rfind("(case-list-element")
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	for b in range(0, missingBrackets):
					# 		result += ")"
					# 	result += ", (case-list-element"
					# 	lastCommandOutput += "(case-list-element"
					

		if currentBlockType == "program-type-name":
			if "program-declaration::program-type-name" in currentLine:
				rstmt = getStmtR(currentLine)
				result += "(PROG, " +  rstmt # + processBlock(blockType, blockLines, index+1)
				lastCommandOutput += rstmt
			else:
				lstmt, rstmt = getStmtLR(currentLine)
				if len(lstmt) > 0 and len(rstmt) > 0:
					result += lstmt.split("::")[-1] + ", " + rstmt.split("::")[-1]
					lastCommandOutput += lstmt.split("::")[-1] + ", " + rstmt.split("::")[-1]
			# return result		
	
		if currentBlockType == "program-configuration": 
			if FirstLineInBlock:
				stmtType = currentLine.split("::")[-1]
				result += "(" + stmtType
				lastCommandOutput += stmtType
			else:
				lstmt, rstmt = getStmtLR(currentLine)
				if len(lstmt) > 0 and len(rstmt) > 0:
					result += ", " + lstmt.split("::")[-1] + ", " + rstmt.split("::")[-1]
					lastCommandOutput += lstmt.split("::")[-1] + ", " + rstmt.split("::")[-1]
	
		if currentBlockType == "task-configuration" or currentBlockType == "task-initialization":
			if FirstLineInBlock:
				stmtType = currentLine.split("::")[-1]
				result += "(" + stmtType
				lastCommandOutput += stmtType
			else:
				lstmt, rstmt = getStmtLR(currentLine)
				if len(lstmt) > 0 and len(rstmt) > 0:
					result += ", " + lstmt.split("::")[-1] + ", " + rstmt.split("::")[-1]
					lastCommandOutput += lstmt.split("::")[-1] + ", " + rstmt.split("::")[-1]
	
		if currentBlockType == "direct-variable":
			if FirstLineInBlock:
				# print("----")
				# print(blockLines)
				stmtType = currentLine.split("::")[-1]
				result += "(" + stmtType
				lastCommandOutput += stmtType
			else:
				lstmt, rstmt = getStmtLR(currentLine)
				if len(lstmt) > 0 and len(rstmt) > 0:
					result += ", " + lstmt.split("::")[-1] + ", " + rstmt.split("::")[-1]
					lastCommandOutput += lstmt.split("::")[-1] + ", " + rstmt.split("::")[-1]
	
		if currentBlockType == "assignment-statement":
			# if result.endswith(", "):
			# 	print("@@: " + result)
			if FirstLineInBlock:
				sl_index = result.rfind("(ASSIGNMENT")
				# if not ("statement-list" or "if-statement") in result[sl_index:]:
				# and not "ASSIGNMENT" in result[sl_index:]
				# and not "assignment-statement" in result[sl_index:]
				# if not "statement-list" in result[sl_index:] and not "if-statement" in result[sl_index:] and not "function-call" in result[sl_index:] and not "EXP" in result[sl_index:]:

				result_temp = ""
				if len(result) > 0:
					result_temp = result[:-2]
					openBracketsCount = result[sl_index:].count("(")
					closedBracketsCount = result[sl_index:].count(")")
					missingBrackets = openBracketsCount-closedBracketsCount
					
					# for b in range(0, missingBrackets):
					# 	result_temp += ")"

					result = result_temp + ", "
				result += "(ASSIGNMENT, "
	
			rstmt = getStmtR(currentLine)

			# if len(rstmt) > 0 and not rstmt == "ELSE":
			# 	result += rstmt
			# 	lastCommandOutput += rstmt

			if len(rstmt) > 0: # and not rstmt == "ELSE":
				if result[-1] == ")":
					result += ", "
				if not result[-1] == " ":
					result += ", "
				result += rstmt
				lastCommandOutput += rstmt

			elif "-type-name::type-" in currentLine:
				result += ", " + currentLine.split("-type-name::type-")[-1]
				lastCommandOutput += currentLine.split("-type-name::type-")[-1]
			else:
				operator = currentLine.split("::")[-1]
				ignoreOperators = ["multi-element-variable", "field-selector", "statement-list", "case-statement", "case-element", "case-list", "case-list-element", "if-statement", "for-statement", "for-list"] # , "case-element", "case-list", "case-list-element", "if-statement" , "function-call"
				# print("!! " + operator)
				
				# if operator == "statement-list":
				# 		result += ", (statement-list"
				# 		lastCommandOutput += "(statement-list"
				# 		# result += ")\n"
				# 		# lastCommandOutput += ")\n"
				# 		# result = result.replace("\n, ", "\n", result.count("\n, "))
				# if operator == "if-statement":
				# 	result += ", (if-statement"
				# 	lastCommandOutput += "(if-statement"
				# if operator == "case-statement":
				# 	result += ", (case-statement"
				# 	lastCommandOutput += "(case-statement"
				# if operator == "case-element":
				# 	result += ", (case-element"
				# 	lastCommandOutput += "(case-element"
				# if operator == "case-list":
				# 	result += ", (case-list"
				# 	lastCommandOutput += "(case-list"
				# if operator == "case-list-element":
				# 	result += ", (case-list-element"
				# 	lastCommandOutput += "(case-list-element"
				if operator == "statement-list":
					result += ", (statement-list"
					lastCommandOutput += ", (statement-list"
					# result += ")\n(statement-list"
					# result += "), (statement-list"
					# sl_index = result.rfind("(statement-list")
					# if not "statement-list" in operator and not "if-statement" in operator and not "function-call" in operator and not "EXP" in operator:
					# 	openBracketsCount = result[sl_index:].count("(")
					# 	closedBracketsCount = result[sl_index:].count(")")
					# 	missingBrackets = openBracketsCount-closedBracketsCount
					# 	# for b in range(0, missingBrackets):
					# 	# 	result += ")"
					# 	result += ", (statement-list"
					# 	lastCommandOutput += ", (statement-list"
					# 	# result += ")\n"
					# 	# lastCommandOutput += ")\n"
					# 	# result = result.replace("\n, ", "\n", result.count("\n, "))
				if operator == "multi-element-variable":
					result += "multi-element-variable"
					lastCommandOutput += "multi-element-variable"
				if operator == "field-selector":
					result += ", field-selector"
					lastCommandOutput += ", field-selector"
				if operator == "for-statement":
					result += ", (for-statement"
					lastCommandOutput += ", (for-statement"
				if operator == "for-list":
					result += ", (for-list"
					lastCommandOutput += ", (for-list"
				if operator == "case-statement":
					# result += ")\n(case-statement"
					# result += "), (case-statement"
					# print("CASE: " + currentLine)
					sl_index = result.rfind("(case-statement")
					openBracketsCount = result[sl_index:].count("(")
					closedBracketsCount = result[sl_index:].count(")")
					missingBrackets = openBracketsCount-closedBracketsCount
					# for b in range(0, missingBrackets):
					# 	result += ")"
					result += ", (case-statement"
					lastCommandOutput += ", (case-statement"
				if operator == "if-statement":
					sl_index = result.rfind("(if-statement")
					openBracketsCount = result[sl_index:].count("(")
					closedBracketsCount = result[sl_index:].count(")")
					missingBrackets = openBracketsCount-closedBracketsCount
					# for b in range(0, missingBrackets):
					# 	result += ")"
					result += ", (if-statement"
					lastCommandOutput += "(if-statement"
				if operator == "case-element":
					sl_index = result.rfind("(case-element")
					openBracketsCount = result[sl_index:].count("(")
					closedBracketsCount = result[sl_index:].count(")")
					missingBrackets = openBracketsCount-closedBracketsCount
					# for b in range(0, missingBrackets):
					# 	result += ")"
					result += ", (case-element"
					lastCommandOutput += "(case-element"
				# if operator == "case-list":
				# 	sl_index = result.rfind("(case-list")
				# 	openBracketsCount = result[sl_index:].count("(")
				# 	closedBracketsCount = result[sl_index:].count(")")
				# 	missingBrackets = openBracketsCount-closedBracketsCount
				# 	# for b in range(0, missingBrackets):
				# 	# 	result += ")"
				# 	result += ", (case-list"
				# 	lastCommandOutput += "(case-list"
				# if operator == "case-list-element":
				# 	sl_index = result.rfind("(case-list-element")
				# 	openBracketsCount = result[sl_index:].count("(")
				# 	closedBracketsCount = result[sl_index:].count(")")
				# 	missingBrackets = openBracketsCount-closedBracketsCount
				# 	# for b in range(0, missingBrackets):
				# 	# 	result += ")"
				# 	result += ", (case-list-element"
				# 	lastCommandOutput += "(case-list-element"
				
		if currentBlockType == "var-init-decl":
			if FirstLineInBlock:
				varType = currentLine.split("::")[-2]
				result += "(" + varType
				lastCommandOutput += varType
	
			rstmt = getStmtR(currentLine)
			if len(rstmt) > 0:
				result += ", " +  rstmt
				lastCommandOutput += rstmt
			elif "-type-name::type-" in currentLine:
				result += ", " + currentLine.split("-type-name::type-")[-1]
				lastCommandOutput += currentLine.split("-type-name::type-")[-1]
			elif "-type-name = " in currentLine:
				result += ", " + currentLine.split("-type-name = ")[-1]
				lastCommandOutput += currentLine.split("-type-name = ")[-1]
		
		FirstLineInBlock = False 
		index += 1
	# print("ret2")
	return result # + ")" # + processBlock(blockType, blockLines, index+1)

ivar_c = 0
operators = ["elevated-by", "plus", "minus", "logical-not", "multiply-with", "divide-by", "modulo", "adding",
	"subtracting", "equals", "equals-not", "less-or-equal", "greater-or-equal", "less-than", "greater-than",
	"logical-or", "logical-xor", "logical-and"]

def subOperator(stmt, nested=False):
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
			new_stmt = ""
			if not nested:
				new_stmt = "(IVAR, " + ivarName + ", " + splittedStmt[oIndex] + ", " + splittedStmt[oIndex+1] + ")\n"
			else:
				new_stmt = "(IVAR, " + ivarName + ", " + splittedStmt[oIndex] + ", " + ', '.join(splittedStmt[oIndex+2:]) + ")\n"
			mod_stmt = ', '.join(splittedStmt[:oIndex]) + ", " + ivarName# + "\n"
		else:
			new_stmt = "(IVAR, " + ivarName + ", " + splittedStmt[oIndex-1] + ", " + splittedStmt[oIndex] + ", " + splittedStmt[oIndex+1] + ")\n"
			mod_stmt = ', '.join(splittedStmt[:oIndex-1])
		if not nested:
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

def simplifyExpressionOperators(stmt, level=0, nested=False):
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
	    	tmp_new_stmt, tmp_mod_stmt = subOperator(expression, nested)
	    	new_stmt += tmp_new_stmt
	    	mod_stmt = stmt[:matchedPattern.start()] + tmp_new_stmt + matchedPattern.group(1) + tmp_mod_stmt + matchedPattern.group(3) + stmt[matchedPattern.end():]

	    	nOperators = countOperators(expression)
	    	if nOperators > 1:
	    		mod_stmt = simplifyExpressionOperators(mod_stmt, level+1, nested)
	
	return mod_stmt

toSimplify = [", (if-statement, ", ", (case-element, ", ", (statement-list, ", ", (function-call, ", ", (task-initialization, ", ", (direct-variable, ", ", (fb-invocation, ", ", (case-statement, ", ", (ASSIGNMENT, ", ", (for-statement, ", ", (for-list, "]
# toSimplify = [", (statement-list, ", ", (if-statement, ", ", (case-statement, ", ", (case-element, ", ", (function-call, ", ", (task-initialization, ", ", (direct-variable, ", ", (fb-invocation, ", ", (ASSIGNMENT, "]

def toSimplifyExp(stmt):
	global toSimplify

	for expType in toSimplify:
		if expType in stmt:
			return expType
	return False

def isSimplifiable(stmt):
	global toSimplify

	for expType in toSimplify:
		if expType in stmt: #  and not stmt.startswith("(IVAR, ")
			return True, 
	return False

def getNestedExp_Start_End_value(stmt, expType="(EXP, "):
	# find opening bracket and closing bracket and delete them
	if expType in stmt:
		exp_start_index = stmt.rfind(expType)
		exp_end_index = 0
		exp_substr = stmt[exp_start_index:]
		openBracketsCount = 0
		closedBracketsCount = 0
		exp_counter = 0

		while exp_counter < len(exp_substr):
			if exp_substr[exp_counter] == "(":
				openBracketsCount += 1
			if exp_substr[exp_counter] == ")":
				closedBracketsCount += 1

			if openBracketsCount == closedBracketsCount:
				exp_end_index = exp_start_index+exp_counter
				break

			exp_counter += 1
		return exp_start_index, exp_end_index+1, stmt[exp_start_index:exp_end_index+1]
	
	return 0, 0, ""

def simplifyExpression(stmt, level=0, nested=False):
	global ivar_c, toSimplify
	new_stmt = stmt
	
	while True:
		# if not isSimplifiable(stmt) and not "(EXP, " in stmt:
		# 	return stmt

		# print(stmt.count("(EXP, "))

		# if stmt.count("(EXP, ") == 1:
		# 	print(stmt)
		# 	sys.exit()

		if not "(EXP, " in stmt:
			break
	
		# if "(EXP, " in stmt:
		# 	pattern = '(\(EXP, )([^()]+)(\))'
		# 	reCompiler = re.compile(pattern)
		# 	expMatched = False

		# 	for matchedPattern in reCompiler.finditer(stmt):
		# 	    expMatched = True
		# 	    ivarName = "r" + str(ivar_c)
		# 	    ivar_c += 1

		# 	    if len(matchedPattern.group(2).split()) == 1:
		# 	    	if not (len(stmt[:matchedPattern.start()]) == 0 and len(stmt[matchedPattern.end():]) == 0):
		# 	    		new_stmt = stmt[:matchedPattern.start()] + matchedPattern.group(2) + stmt[matchedPattern.end():]
		# 	    else:
		# 	    	new_stmt = "\n(IVAR, " + ivarName + ", " + matchedPattern.group(2) + ")"
		# 	    	if not (len(stmt[:matchedPattern.start()]) == 0 and len(stmt[matchedPattern.end():]) == 0):
		# 	    		new_stmt += "\n" + stmt[:matchedPattern.start()] + ivarName + stmt[matchedPattern.end():]
		# 	if not expMatched:
		# 		pattern = '(\(EXP, )(\([^()]+\))(\))'
		# 		reCompiler = re.compile(pattern)
	
		# 		for matchedPattern in reCompiler.finditer(stmt):
		# 			ivarName = "r" + str(ivar_c)
		# 			ivar_c += 1
		# 			if len(matchedPattern.group(2).split()) == 1:
		# 				if not (len(stmt[:matchedPattern.start()]) == 0 and len(stmt[	matchedPattern.end():]) == 0):
		# 					new_stmt = stmt[:matchedPattern.start()] + matchedPattern.group(2) + 	stmt[matchedPattern.end():]
		# 			else:
		# 				new_stmt = "(IVAR, " + ivarName + ", " + matchedPattern.group(2) + ")"
		# 				if not (len(stmt[:matchedPattern.start()]) == 0 and len(stmt[matchedPattern.end():]) == 0):
		# 					new_stmt += "\n" + stmt[:matchedPattern.start()] + ivarName + stmt[	matchedPattern.end():]
		# 	stmt = new_stmt

		if "(EXP, " in stmt:
			pattern = '(\(EXP, )([^()]+)(\))'
			reCompiler = re.compile(pattern)
			
			expMatched = False
			if not expMatched:
				for matchedPattern in reCompiler.finditer(stmt):
					expMatched = True
					ivarName = "r" + str(ivar_c)
					ivar_c += 1
					
					if len(matchedPattern.group(2).split()) == 1:
						if not (len(stmt[:matchedPattern.start()]) == 0 and len(stmt[matchedPattern.end():]) == 0):
							new_stmt = stmt[:matchedPattern.start()] + matchedPattern.group(2) + stmt[matchedPattern.end():]
					else:
						if nested:
							new_stmt = "\n(IVAR, " + ivarName + ", " + matchedPattern.group(2) + ")"
							if not (len(stmt[:matchedPattern.start()]) == 0 and len(stmt[matchedPattern.end():]) == 0):
								new_stmt += "\n" + stmt[:matchedPattern.start()] + ivarName + stmt[matchedPattern.end():]
							
							# new_stmt = ""
							# new_stmt += "\n" + stmt[:matchedPattern.start()] + ivarName + ")"
							# new_stmt += "\n(IVAR, " + ivarName + ", " + matchedPattern.group(2) + ")*\n"
							# new_stmt += stmt[matchedPattern.end():]

							# new_stmt = ""
							# new_stmt += "\n" + "@1" + stmt[:matchedPattern.start()] + ivarName + stmt[matchedPattern.end():]
							# new_stmt += "\n(IVAR, " + ivarName + ", " + matchedPattern.group(2) + ")*" + "@2" 

							# print("$$$$")
							# print(new_stmt)
							# sys.exit()

							# if not (len(stmt[:matchedPattern.start()]) == 0 and len(stmt[matchedPattern.end():]) == 0):
							# 	new_stmt = ""
							# 	new_stmt += "\n" + stmt[:matchedPattern.start()] + ivarName
							# 	new_stmt += "\n(IVAR, " + ivarName + ", " + matchedPattern.group(2) + ")*\n"
							# 	new_stmt += stmt[matchedPattern.end():]

								

								# after_part = stmt[matchedPattern.end():]
								# # print(after_part[:after_part.find(")")+1])
								# # sys.exit()
								# new_stmt += after_part[:after_part.find(")")+1]
						else:
							new_stmt = "\n(IVAR, " + ivarName + ", " + matchedPattern.group(2) + ")"
							if not (len(stmt[:matchedPattern.start()]) == 0 and len(stmt[matchedPattern.end():]) == 0):
								new_stmt += "\n" + stmt[:matchedPattern.start()] + ivarName + stmt[matchedPattern.end():]
			if not expMatched:
				pattern = '(\(EXP, )(\([^()]+\))(\))'
				reCompiler = re.compile(pattern)
	
				for matchedPattern in reCompiler.finditer(stmt):
					ivarName = "r" + str(ivar_c)
					ivar_c += 1
					if len(matchedPattern.group(2).split()) == 1:
						if not (len(stmt[:matchedPattern.start()]) == 0 and len(stmt[	matchedPattern.end():]) == 0):
							new_stmt = stmt[:matchedPattern.start()] + matchedPattern.group(2) + stmt[matchedPattern.end():]
					else:
						new_stmt = "(IVAR, " + ivarName + ", " + matchedPattern.group(2) + ")"
						if not (len(stmt[:matchedPattern.start()]) == 0 and len(stmt[matchedPattern.end():]) == 0):
							new_stmt += "\n" + stmt[:matchedPattern.start()] + ivarName + stmt[	matchedPattern.end():]
			if not expMatched:
				# print(toSimplifyExpression)
				expMatched = True
				expStartIndex, expEndIndex, expValue = getNestedExp_Start_End_value(stmt, "(EXP, ")
				# print(expValue)
				# sys.exit()
				ivarName = "r" + str(ivar_c)
				ivar_c += 1
				new_stmt = "\n" + "(IVAR, " + ivarName + ", " + expValue[len("(EXP, "):-1] + ")\n"
				new_stmt += stmt[:expStartIndex] + ivarName + stmt[expEndIndex:]

			stmt = new_stmt
		
		# if isSimplifiable(new_stmt) or "(EXP, " in new_stmt:
		# 	new_stmt = simplifyExpression(new_stmt, level+1, nested)
	# print("DONE1")

	while True:
		if not isSimplifiable(stmt):
			break

		if  isSimplifiable(stmt):
			toSimplifyExpression = toSimplifyExp(stmt)

			pattern = "(\(" + toSimplifyExpression[3:] + ")([^()]+)(\))"
			reCompiler = re.compile(pattern)
	
			expMatched = False
			if not expMatched:
				# print(toSimplifyExpression)
				expMatched = True
				expStartIndex, expEndIndex, expValue = getNestedExp_Start_End_value(stmt, toSimplifyExpression[2:])
				# print(expValue)
				ivarName = "r" + str(ivar_c)
				ivar_c += 1
				new_stmt = ""
				if nested:
					new_stmt += "\n" + toSimplifyExpression[2:] + ivarName + ", " + expValue[len(toSimplifyExpression[2:]):-1] + ")\n"
					
					# new_stmt += expValue[len(toSimplifyExpression[2:]):-1] + ")\n"
					# new_stmt += "\n" + toSimplifyExpression[2:] + ivarName + ", " + expValue[len(toSimplifyExpression[2:]):-1] + ")\n"
					# print(new_stmt)
					# sys.exit()
				else:
					new_stmt += "\n" + toSimplifyExpression[2:] + ivarName + ", " + expValue[len(toSimplifyExpression[2:]):-1] + ")\n"
				new_stmt += stmt[:expStartIndex] + ivarName + stmt[expEndIndex:]
				# new_stmt = "\n" + stmt[:expStartIndex] + ivarName + stmt[expEndIndex:] + "\n"
				# new_stmt += toSimplifyExpression[2:] + ivarName + ", " + expValue[len(toSimplifyExpression[2:]):-1] + ")\n"

			if not expMatched:
				for matchedPattern in reCompiler.finditer(stmt):
					# print(toSimplifyExpression)
					expMatched = True
					ivarName = "r" + str(ivar_c)
					ivar_c += 1
					new_stmt = toSimplifyExpression[2:] + ivarName + ", " + matchedPattern.group(2) + ")\n"
					new_stmt += stmt[:matchedPattern.start()] + ivarName + stmt[matchedPattern.end():]
					# new_stmt = stmt[:matchedPattern.start()] + ivarName + stmt[matchedPattern.end():] + "\n"
					# new_stmt += toSimplifyExpression[2:] + ivarName + ", " + matchedPattern.group(2) + ")"
					
			if not expMatched:
				# print(toSimplifyExpression)
				pattern = "(\(" + toSimplifyExpression[3:] + ")(\([^()]+\))(\))"
				reCompiler = re.compile(pattern)
				for matchedPattern in reCompiler.finditer(stmt):
					expMatched = True
					ivarName = "r" + str(ivar_c)
					ivar_c += 1
					new_stmt = toSimplifyExpression[2:] + ivarName + ", " + matchedPattern.group(2) + ")\n"
					new_stmt += stmt[:matchedPattern.start()] + ivarName + stmt[matchedPattern.end():]
					# new_stmt = stmt[:matchedPattern.start()] + ivarName + stmt[matchedPattern.end():] + "\n"
					# new_stmt += toSimplifyExpression[2:] + ivarName + ", " + matchedPattern.group(2) + ")"
			
			stmt = new_stmt

	new_stmt_list = new_stmt.splitlines(True)

	if not nested:
		new_stmt_list.reverse()

	new_stmt = ''.join(new_stmt_list[1:])
	new_stmt += new_stmt_list[0]
	# new_stmt = simplifyExpressionOperators(new_stmt, nested=nested)
	
	# if nested, reverse IVARs only
	if nested:
		new_stmt2 = ""
	
		new_stmt_list = new_stmt.splitlines(True)
		new_stmt_list.reverse()

		# for line in new_stmt_list:
		# 	if line.startswith("(IVAR, "):
		# 		new_stmt2 += line + "\n"
	
		# new_stmt_list = new_stmt.splitlines(True)
	
		# for line in new_stmt_list:
		# 	if not line.startswith("(IVAR, "):
		# 		new_stmt2 += line
	
		# new_stmt = new_stmt2

		new_stmt = '\n'.join(new_stmt_list)
	
	# clean empty lines
	new_stmt = clean_empty_lines(new_stmt)

	return new_stmt

def clean_empty_lines(new_stmt):
	new_stmt_lines = new_stmt.split("\n")
	new_stmt_non_empty_lines = [line for line in new_stmt_lines if line.strip() != ""]
	new_stmt_without_empty_lines = ""
	for line in new_stmt_non_empty_lines:
		new_stmt_without_empty_lines += line + "\n"
	new_stmt = new_stmt_without_empty_lines

	return new_stmt

def clean_empty_lines2(new_stmt):
	new_stmt_without_empty_lines = ""

	new_stmt_lines = new_stmt.split("\n")
	for line in new_stmt_lines:
		if len(line) > 2:
			# print("Line: " + line + ", len: " + str(len(line)))
			new_stmt_without_empty_lines += line

			# last_char = line[-1]
			# if not last_char == ")" and not last_char == "*":
			# 	new_stmt_without_empty_lines += ")"
			# 	if "))" in new_stmt_without_empty_lines:
			# 		print(last_char)
			# 		print(new_stmt_without_empty_lines)
			# 		sys.exit()

			new_stmt_without_empty_lines += "\n"
	new_stmt = new_stmt_without_empty_lines

	return new_stmt

def genIR(pASTlines):
	global o_f_IR, ivar_c

	blockRanges = identifyBlocks(pASTlines)
	lastIndexParsed = 0
	# print(len(pASTlines))
	line_no = 0
	for i in range(0, len(pASTlines)):
		line_no += 1
		# print(line_no)

		line = pASTlines[i]
		
		blockType = getBlockType(line)
		# print(blockType)
		if i >= lastIndexParsed:
			if isTranslatable(blockType):
				# print(line)
				lastIndexParsed = blockRanges[i]+1
				blockLines = pASTlines[i:lastIndexParsed]
				
				# print("blockType = " + blockType)
				# if blockType == "function-block-declaration":
				# 	print(blockLines)

				stmt = processBlock(blockType, blockLines)
				# print(stmt)
				# sys.exit()

				print("##: " + stmt)
				ADD_PREFIX = False

				if stmt.startswith("\n(structure-element-declaration, ") and len(stmt.split(", ")) > 3:
					ADD_PREFIX = True

				# if "date-and-time, date-literal, year, 1970, month, 01, day, 01, day-hour, 00, day-minute, 00, day-second, 00.00" in stmt:
				
				# if "inr_Y1" in stmt and stmt.startswith("(if-statement, (EXP, lr_y_delta"):
				# 	print("=====")
				# 	print("before ##: " + str(blockLines))
				# 	print("blockType2 = " + blockType)
				# 	sys.exit()

				# if stmt.startswith(", "):
				# 	print("=====")
				# 	print("before ##: " + str(blockLines))
				# 	print("blockType2 = " + blockType)
				# 	sys.exit()

				# if "(if-statement, (EXP, lx_Init), (statement-list, (fb-invocation, lfb_TON_Wait, IN, (EXP, lx_Start_TON_Wait), PT, (EXP, lt_TON_Wait)), (fb-invocation, lfb_R_Trig_Start_Park_Pos," in stmt:
				# 	print("=====")
				# 	print("before ##: " + str(blockLines))
				# 	print("blockType2 = " + blockType)
				# 	sys.exit()

				if stmt.startswith("(if-statement"): #  
					stmt = simplifyExpression(stmt, nested=True)
					# if "(if-statement, r905140," in stmt:
					# 	print(stmt)
					# 	print("1-")
					# 	sys.exit()
					# if ", t, " in stmt:
					if stmt.startswith("(if-statement"):
						# print(stmt)
						# print("1-")
						ivarName = "r" + str(ivar_c)
						ivar_c += 1
						# (if-statement, t, lx_esv_timer, r90)
						# stmt = stmt[:15] + "t, " + stmt[15:]
						stmt = stmt[:15] + ivarName + ", " + stmt[15:]
						# print(stmt)
						# sys.exit()
				else:
					stmt = simplifyExpression(stmt)
					
					# if "(if-statement, r905140," in stmt:
					# 	print(stmt)
					# 	print("2-")
					# 	sys.exit()

				if "(DATA_BLOCK, " in stmt and not stmt.startswith("(DATA_BLOCK, "):
					# print("PPPPPPPPPPPPPP")
					# print(stmt)
					splitted_stmt = stmt.split("\n")
					cleaned_splitted_stmt = []
					for st in splitted_stmt:
						if len(st) > 0:
							cleaned_splitted_stmt.append(st)
					# print(splitted_stmt)
					if len(cleaned_splitted_stmt) > 1 and cleaned_splitted_stmt[-1].startswith("(DATA_BLOCK, "):
						cleaned_splitted_stmt.reverse()
						new_stmt = '\n'.join(cleaned_splitted_stmt)
						stmt = new_stmt
						# print(new_stmt)
						# sys.exit()


				# expstmt = False
				# if "fb-invocation" in stmt:
				# 	expstmt = True
				# if "location-prefix, Q" in stmt:
				# 	print(stmt)

				# stmt = simplifyExpression(stmt)

				# if stmt.startswith("(if-statement, (EXP, lx_Init), (statement-list, (fb-invocation, lfb_TON_Wait, IN, (EXP, lx_Start_TON_Wait), PT, (EXP, lt_TON_Wait)), (fb-invocation, lfb_R_Trig_Start_Park_Pos, CLK"):
				# 	print("000000000000000000000000000")
				# 	# print(blockLines)
				# 	sys.exit()

				# if not stmt.startswith("(if-statement") or len(stmt) < 3000: #  
				# 	stmt = simplifyExpression(stmt)
				# 	print("$$: " + stmt)
					

				# 	print("$$$$$$$$")
				# 	print(stmt)

				

				# if "location-prefix, Q" in stmt:
				# 	print("====")
				# 	print(stmt)

				# toClean = "), "
				# if toClean in stmt:
				# 	print("====")
				# 	print(stmt)
				# 	stmt = stmt.replace(toClean, ", ")
				# 	print(stmt)
				
				if ADD_PREFIX:
					# stmt = "(DATA_BLOCK_START)\n" + stmt
					
					stmt_list_temp = stmt.split("\n")
					stmt_list = []
					for line in stmt_list_temp:
						if len(line) > 0:
							stmt_list.append(line)

					stmt = "\n" + stmt_list[-1] + "\n" + '\n'.join(stmt_list[:-1])

				stmt = clean_empty_lines2(stmt)
				# if "(structure-element-declaration, s_id, String)" in stmt:
				# 	print("&&")
				# 	print(stmt)
				# 	print("^^")
				# 	sys.exit()

				

				o_f_IR.write(stmt) #  + "\n"

				# if blockType == "function-block-declaration":
				# 	o_f_IR.write("(FUNC_END)\n")

				# if expstmt:
				# 	sys.exit()

def scanDefinedFunctions(irLines):
	defFunctions = []

	for line in irLines:
		lineTuple = tuple(line[1:-1].split(", "))
		# print(lineTuple)
		if len(lineTuple) <= 1:
			continue
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
						# if jLineTuple[1] == lineTuple[1]:
						if jLineTuple[2] == lineTuple[1]:
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
				# if p == lineTuple[1]:
				if p == lineTuple[2]:
					# for i in range(2, len(lineTuple), 2):
					for i in range(3, len(lineTuple), 2):
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
	
	inoutvar = []
	if not len(funcInVars) == 0 or not len(funcOutVars) == 0:
		for inVar in funcInVars:
			if inVar in funcOutVars:
				inoutvar.append(inVar)
			else:
				funcIRLines.append("(input-declarations, " + inVar + ", type)")
		for outVar in funcOutVars:
			if not outVar in funcInVars:
				funcIRLines.append("(output-declarations, " + outVar + ", type)")
		for inOutVar in inoutvar:
			funcIRLines.append("(input-output-declarations, " + inOutVar + ", type)")
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
	# print(defFunctions)
	# print(nonDefFunctions)
	# sys.exit()

	# ['FB_Blinker', 'FB_Axis', 'FC_Scale_linear', 'PRG_VGR_Ablauf', 'PRG_Order', 'PRG_MPO_Set_Park_Position', 'PRG_HBW_Ablauf', 'PRG_VGR_Axis_rotate', 'PRG_SSC_Calibration_Color', 'PRG_VGR_Axis_horizontal', 'PRG_MPO_Ablauf', 'PRG_VGR_Axis_vertical', 'PRG_HBW_Axis_Vertical', 'PRG_DSI_Status', 'PRG_SLD_Ablauf', 'PRG_HBW_Axis_Horizontal', 'PRG_SSC_Light', 'PRG_DSO_Status', 'PRG_SSC_Set_Positioning', 'PRG_HBW_Set_Positioning', 'PRG_VGR_Set_Positioning', 'PRG_SSC_Ablauf', 'PRG_SLD_Calibration_Color', 'PRG_SSC_Axis_Vertical', 'PRG_SSC_Set_Park_Position', 'PRG_SLD_Set_Counter_Values', 'PRG_VGR_Set_Park_Position', 'PRG_SSC_Axis_Horizontal', 'PRG_HBW_Set_Park_Position', 'PRG_Acknowledge', 'PRG_NFC']
	# ['R_TRIG', 'TON_TIME', 'TOF_TIME', 'F_TRIG']

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