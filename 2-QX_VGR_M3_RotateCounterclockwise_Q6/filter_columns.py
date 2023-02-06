import sys
import re
import pandas as pd 

columns_f_read = open("columns.txt", "r")
model_column_names = columns_f_read.readlines()[0].split(",")

# file_name = "FT_NewLog_Normal1"
file_name = "FT_NewLog_Normal2"
# file_name = "FT_NewLog_Normal3"
# file_name = "ChemicalPlant-PressureAttack"

df = pd.read_csv(file_name + ".csv")
data_columns = list(df.columns)

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

