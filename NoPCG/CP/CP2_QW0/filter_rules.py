import sys
import re
import pandas as pd 

actuator_f_read = open("actuator.txt", "r")
actuator = actuator_f_read.readlines()[0].strip()
columns_f_read = open("columns.txt", "r")
model_column_names = columns_f_read.readlines()[0].split(",")

mixed_rules_file = open("mixed_rules.txt", "r")
mixed_rules = mixed_rules_file.readlines()

archplc_rules_file = open("rules_archplc.txt", "r")
archplc_rules_lines = archplc_rules_file.readlines()

rules_file = open("rules.txt", "w")

# archplc_rules = {}

# for r in archplc_rules_lines:
# 	r = r.strip()
# 	splitted_r = r.split("   -->   ")
# 	r_left, r_right = splitted_r[0], splitted_r[1]
# 	r_left = r_left.split("  :  ")[-1]
# 	r_left_name = ""

# 	if " in " in r_left:
# 		r_left_name = r_left.split(" in ")[0]
# 	elif " = " in r_left:
# 		r_left_name = r_left.split(" = ")[0]

# 	print(r_left_name)
# 	if not r_left_name in list(archplc_rules.keys()):
# 		archplc_rules[r_left_name] = [r]
# 	else:
# 		archplc_rules[r_left_name].append(r)

# print(archplc_rules)

for r in mixed_rules:
	r = r.strip()
	substr = "   -->   "
	if not substr in r:
		continue
	splitted_r = r.split(substr)
	r_left, r_right = splitted_r[0], splitted_r[1]
	r_left = r_left.split("  :  ")[-1]

	r_left_name = ""
	if " in " in r_left:
		r_left_name = r_left.split(" in ")[0]
	elif " = " in r_left:
		r_left_name = r_left.split(" = ")[0]

	if r_left_name in model_column_names:
		continue

	if actuator in r_right:
		rules_file.write(r + "\n")

for r in archplc_rules_lines:
	rules_file.write(r)
