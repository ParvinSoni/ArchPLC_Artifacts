import sys
import re
import pandas as pd 

actuator_f_read = open("actuator.txt", "r")
actuator = ""
actuator = actuator_f_read.readlines()[0].strip()
split_size = 1 # 400 # 150

FILTER_COLUMNS = True # False # 
columns_f_read = open("columns.txt", "r")
model_column_names = columns_f_read.readlines()[0].split(",")

file_name = "normal_all_removed_types"
df = pd.read_csv(file_name + ".csv")
data_columns = list(df.columns)

if FILTER_COLUMNS:
	tempCurrentSet = []

	for c in data_columns:
		if c == actuator or c in model_column_names:
			tempCurrentSet.append(c)

	data_columns = tempCurrentSet[:]

columnsSetNbr = int(len(data_columns)/split_size)
for i in range(0, columnsSetNbr):
	startIndex = i*split_size
	endIndex = startIndex+split_size
	
	# last set of columns
	if i == columnsSetNbr-1:
		endIndex = len(data_columns)

	currentSet = data_columns[i*split_size:endIndex]

	if not actuator in currentSet:
		currentSet.append(actuator)

	filteredCurrentSet = []
	for c in currentSet:
		if not c.endswith("_ts"):
			filteredCurrentSet.append(c)

	if len(filteredCurrentSet) <= split_size:
		continue

	current_df = df[filteredCurrentSet]

	# display 
	print("\nCSV Data shape after extracting a column subset: " + str(current_df.shape) + "\n")
	
	output_filename = "input/" + file_name + "_" + str(i) + ".csv"
	current_df.to_csv(output_filename, index=False)
	
	print("File: " + output_filename + " is written!")
	
	print("finished!")

	# sys.exit()

'''
# print(df.iloc[1].values)
first_column_values = list(df.iloc[0])

if "Float" in first_column_values or "String" in first_column_values:
	df = df.drop(labels=0, axis=0)

missing_columns = []
found_columns = []
ignored_columns = []

for c in model_column_names:
	FOUND_C = False
	for cc in data_columns:
		if c in cc:
			FOUND_C = True
			if not cc.endswith("_ts"):
				found_columns.append(cc)
			else:
				if not cc in ignored_columns:
					ignored_columns.append(cc)
	if FOUND_C:
		continue
	else:
		missing_columns.append(c)

print("\nData trace missing model columns: " + str(missing_columns) + "\n")
print("\nData trace ignored columns: " + str(ignored_columns) + "\n")

# remove missing columns
# model_column_names = set(model_column_names)-set(missing_columns)

# remove non-related columns
# model_column_names = set(model_column_names)-set(found_columns)

# display 
print("Original " + file_name + ".csv Data shape: " + str(df.shape))

df = df[found_columns]

# display 
print("\nCSV Data shape after extracting a column subset: " + str(df.shape) + "\n")

output_filename = file_name + "_filtered.csv"
df.to_csv(output_filename, index=False)

print("File: " + output_filename + " is written!")

print("finished!")

'''