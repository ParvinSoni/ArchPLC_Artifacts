import networkx as nx
import matplotlib.pyplot as plt
import os
import re
import time
import xml.etree.ElementTree as ET
import pydot
from graphviz import Source
import sys
# from pymodbus.client.sync import ModbusTcpClient
from datetime import datetime
import pandas as pd
# import seaborn as sns
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

me_file = open("malicious_entries.txt")
me_lines = me_file.readlines()
malicious_entries = []
for i in me_lines:
    if len(i.strip()) == 0:
        continue
    malicious_entries.append(i.strip())


file_name = "1" # "2" # "3_normal2" # "1" # 
# input_file = open("IOtrace_normal1.csv")
# input_file = open("IOtrace_attack1.csv")
# input_file = open("IOtrace_attack1_removed_malicious.csv")
# input_file = open("IOtrace_attack2.csv")

# target_file_name = "FT_NewLog_Normal2.csv"
# target_file_name = "abnormal1_fixed.csv"
target_file_name = "datatraces.csv"
input_file = open(target_file_name)
if not "abnormal" in target_file_name and not "attack" in target_file_name and not "datatraces" in target_file_name:
    malicious_entries = []

qm_file = "rules.txt" # "output/qm/qm" + rules_file_name + ".log"
# qm_file = "rules1.txt" # ArchPLC
# qm_file = "rules-apriori1.txt"
# qm_file = "rules-nopcg1.txt"

qm_file_reader = open(qm_file, "r")
rules_lines = []
bins = 10 
minSupport = 1.0
minConfidence = 1.0


output_file2 = "ddata.txt"
ddata_file = open(output_file2, "w")
pm_file = open("../physicalModel.txt")
community_name = ""
samples_list = []

def get_measurements(f):
	return pd.read_csv(f) 

def save_measurements(f, df):
	df.to_csv(f, index=False)

	return True

def is_number(s):
    try:
        if s.isdigit():
            return True
        float(s)
        return True
    except ValueError:
        return False

def save_csv_pd(f, df):
    column_names = list(get_column_names(df))
    samples_list = []
    for index, row in df.iterrows():
        row_result = ""

        for c in column_names:
            row_result += c + "$$" + str(row[c]) + ","
        row_result = row_result[:-1] + "\n"
        samples_list.append(row_result[:-1])
        f.write(row_result)

    f.close()

    return samples_list

def qm_save_csv_pd(f, df):
    column_names = list(get_column_names(df))
    samples_list = []

    for index, row in df.iterrows():
        row_result = ""
        for c in column_names:
            row_result += c + "$$" + str(row[c]) + ","

        row_result = row_result[:-1] + "\n"
        samples_list.append(row_result[:-1])

    f.close()

    return samples_list

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

def get_column_names_list(community, column_type=[""]):
    column_names = []

    for c in community:
        for ct in column_type:
            if c.startswith(ct):
                column_names.append(c)

    return column_names

def detect_violations(rules_data, samples_list):
    v_counter = 0

    for r in rules_data:
        rule_src = r[0][0]
        rule_target = r[0][1]
        score = r[1]

        s_counter = 0
        for sample in samples_list:
            s_counter += 1
            ALL_ELEMENTS_EXIST = True
            for s in rule_src:
                if not s in sample:
                    ALL_ELEMENTS_EXIST = False
                    break
            
            if not ALL_ELEMENTS_EXIST:
                continue

            ALL_ELEMENTS_EXIST = True
            for t in rule_target:
                if not t in sample:
                    ALL_ELEMENTS_EXIST = False
                    break

            if not ALL_ELEMENTS_EXIST:
                v_counter += 1
    return v_counter

def qm_filter_rules(rules_data):
    global minSupport, minConfidence

    r_counter = 0
    min_support = minSupport 
    min_conf = minConfidence
    allowDiscreteValRules = True
    onlyConsiderSensor2AactuatorRules = True
    tolerance_thresh = 0
    rules = []

    for r in rules_data:
        rule_src = r[0]
        rule_target = r[1]
        support = r[2]
        conf = r[3]
        escape_rule = False
        if support < min_support or conf < min_conf:
            continue

        if not allowDiscreteValRules:
            for rs in rule_src:
                rs_value = rs[1]
                if rs_value[0] == rs_value[1]:
                    escape_rule = True
                    break
            
            if escape_rule:
                continue

            for rt in rule_target:
                rt_value = rt[1]
                if rt_value[0] == rt_value[1]:
                    escape_rule = True
                    break
            
            if escape_rule:
                continue

        if onlyConsiderSensor2AactuatorRules:
            for rs in rule_src:
                rs_name = rs[0]
                if rs_name.startswith("Q"):
                    escape_rule = True
                    break
            
            if escape_rule:
                continue

            for rt in rule_target:
                rt_name = rt[0]
                if rt_name.startswith("I"):
                    escape_rule = True
                    break
            
            if escape_rule:
                continue

        rules.append(r)
        r_counter += 1
    
    print("We only considered: " + str(r_counter) + " rules out of the entire rules set.")

    return rules

def getVarsRuleRelated(sample, r):
    result = []
    rule_vars = []
    r_conditions = r[0]
    for r_cond in r_conditions:
        r_cond_var = r_cond[0]
        if not r_cond_var in rule_vars:
            rule_vars.append(r_cond_var)

    r_targets = r[1]
    for r_target in r_targets:
        r_target_var = r_target[0]
        if not r_target_var in rule_vars:
            rule_vars.append(r_target_var)

    split_sample = sample.split(",")
    for e in split_sample:
        for v in rule_vars:
            if v in e and not v in result:
                result.append(e)
    
    return result


violated_rules = []
false_violated_rules = []
true_violated_rules = []
def qm_detect_violations(rules_data, samples_list):
    global violated_rules

    v_counter = 0
    r_counter = 0
    min_support = 50
    min_conf = 100
    allowDiscreteValRules = True
    onlyConsiderSensor2AactuatorRules = True
    tolerance_thresh = 0

    violation_samples = []

    for r in rules_data:
        rule_src = r[0]
        rule_target = r[1]
        support = r[2]
        conf = r[3]
        
        s_counter = 0
        for sample in samples_list:
            s_counter += 1
            ALL_ELEMENTS_EXIST = True
            for rs in rule_src:
                rs_name = rs[0]
                rs_value = rs[1]
                row_value = sample[sample.find(rs_name + "$$") + len(rs_name + "$$"):]

                if "," in row_value:
                    row_value = row_value[:row_value.find(",")]

                if row_value == "nan":
                    ALL_ELEMENTS_EXIST = False

                insideInterval = None
                if is_number(row_value):
                    row_value = float(row_value)
                    # print("======")
                    if isinstance(rs_value[0], str):
                    	continue
                    # print(rs_value)
                    # print(type(rs_value))
                    # print(row_value)
                    # print(type(row_value))
                    insideInterval = row_value >=  rs_value[0] and row_value <= rs_value[1]
                else:
                    insideInterval = row_value ==  rs_value[0] or row_value == rs_value[1]
                if not insideInterval:
                    ALL_ELEMENTS_EXIST = False
                    break

            if ALL_ELEMENTS_EXIST:
                for rt in rule_target:
                    rt_name = rt[0]
                    rt_value = rt[1]
                    row_value = sample[sample.find(rt_name + "$$") + len(rt_name + "$$"):]
                    if "," in row_value:
                        row_value = row_value[:row_value.find(",")]

                    insideInterval = None
                    if is_number(row_value):
                        row_value = float(row_value)
                        insideInterval = row_value >=  rt_value[0]-tolerance_thresh and row_value <=  rt_value[1]+tolerance_thresh
                    else:
                        insideInterval = row_value ==  rt_value[0] or row_value ==  rt_value[1]
                    if not insideInterval:
                        ALL_ELEMENTS_EXIST = False
                        break
                    
                if not ALL_ELEMENTS_EXIST:
                    result = getVarsRuleRelated(sample, r)
                    print("Violation: Sample " + str(s_counter)+ ": " + str(result) + ", does not match the rule: " + str(r))

                    if not str(s_counter) in malicious_entries:
                        # print("FALSE POSITIVE")
                        if not str(r) in false_violated_rules:
                            false_violated_rules.append(str(r))

                    if str(s_counter) in malicious_entries:
                        # print("FALSE POSITIVE")
                        if not str(r) in true_violated_rules:
                            true_violated_rules.append(str(r))

                    if not s_counter in violation_samples:
                        violation_samples.append(s_counter)

                    if not str(r) in violated_rules:
                        violated_rules.append(str(r))

                    v_counter += 1

    print("\nTotal violation samples: " + str(len(violation_samples)))

    return v_counter


def get_qm_conditions(rule_condition):
    result = []
    rule_conditions = []

    if "  AND  " in rule_condition:
        rule_conditions = rule_condition.split("  AND  ")
    else:
        rule_conditions.append(rule_condition)

    for rc in rule_conditions:
        rule_condition_column = None
        rule_condition_value = None
        rule_condition_value_start = None
        rule_condition_value_end = None

        if " in " in rc:
            rule_condition_column, rule_condition_value = rc.split(" in ")
            rule_condition_value_start, rule_condition_value_end = rule_condition_value.split("; ")
            rule_condition_value_start = float(rule_condition_value_start[1:])
            rule_condition_value_end = float(rule_condition_value_end[:rule_condition_value_end.find("]")])
        else:
            rule_condition_column, rule_condition_value = rc.split(" = ")
            rule_condition_value_start = rule_condition_value
            rule_condition_value_end = rule_condition_value

        result.append([rule_condition_column, (rule_condition_value_start, rule_condition_value_end)])

    return result


def get_qm_rules():
    global qm_file_reader, rules_lines

    rules = []
    one_rule = []

    rules_data = qm_file_reader.read()
    rules_lines = rules_data.split("\n")

    for l in rules_lines:
        if not "   -->   " in l:
            break

        rule_part_1, rule_part_2 = l.split("   -->   ")
        rule_support_conf, rule_condition = rule_part_1.split("  :  ")
        
        rule_support = int(rule_support_conf[rule_support_conf.find("(")+1:rule_support_conf.find("%")])
        rule_conf = int(rule_support_conf[rule_support_conf.find("confidence = ")+len("confidence = "):rule_support_conf.find(" %")])
        rule_condition_list = get_qm_conditions(rule_condition)
        rule_result_list = get_qm_conditions(rule_part_2)
        
        one_rule = [rule_condition_list, rule_result_list, rule_support, rule_conf]

        rules.append(one_rule)

    qm_file_reader.close()

    return rules

def main():
    global pm_file, community_name, d_file, ddata_file, violated_rules, rules_lines

    results_raw  = get_measurements(input_file)
    column_names = list(results_raw.columns)
    df = pd.DataFrame(results_raw, columns=column_names) # index=ts.index, 

    # remove var types row
    df = df.drop(index=0)

    samples_list = save_csv_pd(ddata_file, df)

    rules_data = get_qm_rules()

    violations = qm_detect_violations(rules_data, samples_list)

    # if violations > 0:
    print("Number of rules: " + str(len(rules_lines)))
    print("Detected: " + str(violations) + " violations.")
    print("Detected: " + str(len(violated_rules)) + " violated rules.")
    print("Falsly detected: " + str(len(false_violated_rules)) + " false violated rules.")
    print("Truly detected: " + str(len(true_violated_rules)) + " true violated rules.")
    print("Number of samples: " + str(len(samples_list)))
    

if __name__ == "__main__":
    main()
    

