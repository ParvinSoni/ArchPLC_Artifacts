import networkx as nx
import matplotlib.pyplot as plt
import os
import re
import time
import xml.etree.ElementTree as ET
import pydot
from graphviz import Source
import sys
from pymodbus.client.sync import ModbusTcpClient
from datetime import datetime
import pandas as pd
import seaborn as sns
from scipy import stats
import numpy as np
from sklearn import preprocessing
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.preprocessing import MinMaxScaler
import json
import csv

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

bins = 10 # 50 # 100 # 
minSupport = 0.90 # 0.50 # 0.17 # 1.0 # 0.08  # 
minConfidence = 1.0 # 0.80 # 0.9 # 0.08 # 0.999 # 0.9 # 0.68
file_name = "1"
input_file = open("output/modbus" + file_name + ".log")
output_file1 = "output/modbus" + file_name + "_d.txt"
d_file = open(output_file1, "w")
# d_file_read = open(output_file1, "r")
output_file2 = "output/modbus" + file_name + "_ddata.txt"
output_file3 = "output/modbus" + file_name + "_rules.txt"

ddata_file = open(output_file2, "w")
rules_file = open(output_file3, "w")
pm_file = open("output/physicalModel.txt")
community_name = ""
qm_file = "output/qm/qm" + file_name + ".log"
qm_file_reader = open(qm_file, "r")

def get_column_names_list(community, column_type=[""]):
	column_names = []

	for c in community:
		for ct in column_type:
			if c.startswith(ct):
				column_names.append(c)

	return column_names

# Copyright for the Apriori algorithm implementation code is for the following repo
# https://github.com/asaini/Apriori

def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    """calculates the support for items in the itemSet and returns a subset
    of the itemSet each of whose elements satisfies the minimum support"""
    _itemSet = set()
    localSet = defaultdict(int)

    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1

    for item, count in localSet.items():
        support = float(count) / len(transactionList)

        if support >= minSupport:
            _itemSet.add(item)

    return _itemSet


def joinSet(itemSet, length):
    """Join a set with itself and returns the n-element itemsets"""
    return set(
        [i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length]
    )


def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))  # Generate 1-itemSets
    return itemSet, transactionList


def runApriori(data_iter, minSupport, minConfidence):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence)
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    assocRules = dict()
    # Dictionary which stores Association Rules

    oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)

    currentLSet = oneCSet
    k = 2
    while currentLSet != set([]):
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(
            currentLSet, transactionList, minSupport, freqSet
        )
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
        """local function which Returns the support of an item"""
        return float(freqSet[item]) / len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

    toRetRules = []
    for key, value in list(largeSet.items())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item) / getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)), confidence))
    return toRetItems, toRetRules


def printResults(items, rules):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    for item, support in sorted(items, key=lambda x: x[1]):
        print("item: %s , %.3f" % (str(item), support))
    print("\n------------------------ RULES:")
    # sys.exit()
    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))


def to_str_results(items, rules):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    i, r = [], []
    for item, support in sorted(items, key=lambda x: x[1]):
        x = "item: %s , %.3f" % (str(item), support)
        i.append(x)

    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        x = "Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence)
        r.append(x)

    return i, r


def dataFromFile(fname):
    """Function which reads from the file and yields a generator"""
    with open(fname, "rU") as file_iter:
        for line in file_iter:
            line = line.strip().rstrip(",")  # Remove trailing comma
            record = frozenset(line.split(","))
            yield record

def get_measurements(f):
	return pd.read_csv(f) # , sep=","

def save_measurements(f, df):
	# return pd.to_csv(f, df) # , sep=","
	df.to_csv(f, index=False)

	return True

def save_csv_pd(f, df):
	column_names = list(get_column_names(df))

	for index, row in df.iterrows():
		row_result = ""
		for c in column_names:
			row_result += c + "_" + str(row[c]) + ","

		row_result = row_result[:-1] + "\n"

		# print(row_result)
		f.write(row_result)

	f.close()

# def save_csv_pd(f, df):
# 	column_names = list(get_column_names(df))

# 	for index, row in df.iterrows():
# 		row_result = ""
# 		for c in column_names:
# 			row_result += c + "_" + str(row[c]) + ","

# 		row_result = row_result[:-1] + "\n"

# 		# print(row_result)
# 		f.write(row_result)

# 	f.close()

def get_column_names(results_raw, column_type=[""]):
	if len(column_type[0]) == 0:
		return results_raw.columns

	all_column_names = list(results_raw.columns)
	column_names = []

	for c in all_column_names:
		for ct in column_type:
			if c.startswith(ct):
				column_names.append(c)

	return column_names


def get_qm_conditions(rule_condition):
	result = []
	rule_conditions = []

	# print(rule_condition)
	if "  AND  " in rule_condition:
		rule_conditions = rule_condition.split("  AND  ")
	else:
		rule_conditions.append(rule_condition)

	# print(rule_conditions)
	for rc in rule_conditions:
		rule_condition_column, rule_condition_value = rc.split(" in ")
		# print(rule_condition_value)
		rule_condition_value_start, rule_condition_value_end = rule_condition_value.split("; ")
		rule_condition_value_start = float(rule_condition_value_start[1:])
		rule_condition_value_end = float(rule_condition_value_end[:rule_condition_value_end.find("]")])
		# print(rule_condition_value_end)
		result.append([rule_condition_column, (rule_condition_value_start, rule_condition_value_end)])
		# print(rule_condition_column)
		# print(rule_condition_value)

	return result


def get_qm_rules():
	global qm_file_reader

	rules = []
	one_rule = []

	rules_data = qm_file_reader.read()
	rules_lines = rules_data.split("\n")
	# l = rules_lines[1107][:-1]

	for l in rules_lines:
		if not "   -->   " in l:
			break

		# print(l)
		rule_part_1, rule_part_2 = l.split("   -->   ")
		rule_support_conf, rule_condition = rule_part_1.split("  :  ")
		
		rule_support = int(rule_support_conf[rule_support_conf.find("(")+1:rule_support_conf.find("%")])
		rule_conf = int(rule_support_conf[rule_support_conf.find("confidence = ")+len("confidence = "):rule_support_conf.find(" %")])
		rule_condition_list = get_qm_conditions(rule_condition)
		rule_result_list = get_qm_conditions(rule_part_2)
		
		one_rule = [rule_condition_list, rule_result_list, rule_support, rule_conf]
		# print(one_rule)
		
		rules.append(one_rule)

	qm_file_reader.close()

	return rules


def main():
	global d_file, ddata_file, output_file2, minSupport, minConfidence

	results_raw  = get_measurements(input_file)
	column_names = list(get_column_names(results_raw, ["I", "Q"]))
	# print(column_names)
	df = pd.DataFrame(results_raw, columns=column_names) # index=ts.index, 
	# print(df)

	rules = get_qm_rules()
	print(rules[0])

	sys.exit()

	'''
	# discretization transform the raw data
	kbins = KBinsDiscretizer(n_bins=bins, encode='ordinal', strategy='uniform')
	# kbins = KBinsDiscretizer(n_bins=bins, encode='ordinal', strategy='quantile')

	data_trans = kbins.fit_transform(df)

	# summarize first few rows
	# print(data_trans[:10, :])

	# histogram of the transformed data
	# plt.hist(data_trans, bins=bins)
	# plt.show()

	df_trans = pd.DataFrame(data_trans, columns=column_names, dtype="int") # index=ts.index, 
	save_measurements(d_file, df_trans)

	save_csv_pd(ddata_file, df_trans)

	inFile = dataFromFile(output_file2)
	items, rules = runApriori(inFile, minSupport, minConfidence)
	printResults(items, rules)
	'''

	json.dump(rules, rules_file)

	sys.exit()

	minSupport = 0.01 # 0.05 # 0.17 # 0.08 # 
	minConfidence = 1.0 # 0.08 # 0.999 # 0.9 # 0.68
	
	# generate subcommunities rules for sensors and actuators
	csv_reader = csv.reader(pm_file) # , delimiter=','
	community_counter = 0
	for row in csv_reader:
		community_name = "_" + str(community_counter)
		community = list(row)
		column_names = get_column_names_list(community, ["I", "Q"])
		community_path = "output/modbus" + file_name + community_name + "_rules.txt"
		community_file = open(community_path, "w")
		output_file1 = "output/modbus" + file_name + community_name + "_d.txt"
		d_file = open(output_file1, "w")
		output_file2 = "output/modbus" + file_name + community_name + "_ddata.txt"
		ddata_file = open(output_file2, "w")

		print("\n ************************** \n")
		print(column_names)
		df = pd.DataFrame(results_raw, columns=column_names) # index=ts.index, 
		# print(df)
		# discretization transform the raw data
		kbins = KBinsDiscretizer(n_bins=bins, encode='ordinal', strategy='uniform')
		data_trans = kbins.fit_transform(df)
		
		# summarize first few rows
		# print(data_trans[:10, :])
		
		df_trans = pd.DataFrame(data_trans, columns=column_names, dtype="int") # index=ts.index, 
		save_measurements(d_file, df_trans)
		
		save_csv_pd(ddata_file, df_trans)
		
		inFile = dataFromFile(output_file2)
		items, rules = runApriori(inFile, minSupport, minConfidence)
		
		printResults(items, rules)
		# print(rules)
		json.dump(rules, community_file)

		# histogram of the transformed data
		plt.hist(data_trans, bins=bins)
		plt.show()

		community_counter += 1
	

	

if __name__ == "__main__":
    main()
    

