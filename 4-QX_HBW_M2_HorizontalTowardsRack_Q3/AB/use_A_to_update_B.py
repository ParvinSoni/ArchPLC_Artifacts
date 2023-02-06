import csv
import pandas as pd

file_name_A = "datatraces_A"
file_name_B = "datatraces_B"

df_A = pd.read_csv(file_name_A + ".csv")
data_columns_A = list(df_A.columns)

first_column_values_A = list(df_A.iloc[0])
if "Float" in first_column_values_A or "String" in first_column_values_A:
	df_A = df_A.drop(labels=0, axis=0)

df_B = pd.read_csv(file_name_B + ".csv")
data_columns_B = list(df_B.columns)

first_column_values_B = list(df_B.iloc[0])
if "Float" in first_column_values_B or "String" in first_column_values_B:
	df_B = df_B.drop(labels=0, axis=0)


# display 
print("\nCSV Data shape after extracting a column subset A: " + str(df_A.shape) + "\n")
print("\nCSV Data shape after extracting a column subset B: " + str(df_B.shape) + "\n")

result = df_B[data_columns_B]
for c in data_columns_B:
	if c in data_columns_A:
		result[c] = df_A[c]

output_filename = file_name_A + "_" + file_name_B + ".csv"
result.to_csv(output_filename, index=False)

print("File: " + output_filename + " is written!")

print("finished!")