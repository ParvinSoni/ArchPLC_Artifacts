import sys
import re
import pandas as pd 

actuator_f_read = open("actuator.txt", "r")
actuator = ""
actuator = actuator_f_read.readlines()[0].strip()
split_size = 40 # 2 # 30 # 100 # 1 # 400 # 150

FILTER_COLUMNS = True # False # 
columns_f_read = open("columns.txt", "r")
model_column_names = columns_f_read.readlines()[0].split(",")

file_name = "FT_NewLog_Normal1"
df = pd.read_csv(file_name + ".csv")
data_columns = list(df.columns)
# model_column_names = data_columns

if FILTER_COLUMNS:
	tempCurrentSet = []

	for c in data_columns:
		if c == actuator or c in model_column_names:
			tempCurrentSet.append(c)

	data_columns = tempCurrentSet[:]
	
columnsSetNbr = int(len(data_columns)/split_size)
if len(data_columns)/split_size > columnsSetNbr:
	columnsSetNbr += 1

for i in range(0, columnsSetNbr):

	startIndex = i*split_size
	endIndex = startIndex+split_size
	
	# last set of columns
	if i >= columnsSetNbr-1:
		endIndex = len(data_columns)

	currentSet = data_columns[i*split_size:endIndex]

	if not actuator in currentSet:
		currentSet.append(actuator)

	filteredCurrentSet = []
	for c in currentSet:
		if not c.endswith("_ts"):
			filteredCurrentSet.append(c)

	current_df = df[filteredCurrentSet]

	# display 
	print("\nCSV Data shape after extracting a column subset: " + str(current_df.shape) + "\n")
	
	output_filename = "input/" + file_name + "_" + str(i) + ".csv"
	current_df.to_csv(output_filename, index=False)
	
	print("File: " + output_filename + " is written!")
	
	print("finished!")