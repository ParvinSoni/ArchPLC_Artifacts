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

INPUT_VARIABLE = False
# qm_file = "rules_pcg_genetic.txt"
# qm_file = "rules_noPCG_genetic.txt"
qm_file = "rules.txt"
qm_file_reader = open(qm_file, "r")

bins = 10 # 50 # 100 # 
minSupport = 1.0 # 0.17 # 0.08 # 
minConfidence = 1.0 # 0.08 # 0.999 # 0.9 # 0.68

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


def qm_filter_rules(rules_data):
    global minSupport, minConfidence

    r_counter = 0
    min_support = minSupport # 50 # 100 # 
    min_conf = minConfidence # 100 # 90 # 
    allowDiscreteValRules = True # False
    onlyConsiderSensor2AactuatorRules = True
    tolerance_thresh = 0 # 16
    rules = []

    for r in rules_data:
        rule_src = r[0]  # [0]
        rule_target = r[1] # [0]
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
    # print(len(rules))

    return rules

def get_corrective_value(t):
    t_tuple = tuple(t)

    return t_tuple[1]


def getVarsRuleRelated(sample, r):
    result = []
    rule_vars = []
    # print(sample)
    # sys.exit()
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
        # print(rule_condition_value)
        
        # print(rule_condition_value_end)
        result.append([rule_condition_column, (rule_condition_value_start, rule_condition_value_end)])
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
        # sys.exit()
        
        rules.append(one_rule)

    qm_file_reader.close()

    return rules

def is_number(s):
    try:
        if s.isdigit():
            return True
        float(s)
        return True
    except ValueError:
        return False

def genCode(rules_data):
    global INPUT_VARIABLE

    v_counter = 0
    r_counter = 0
    tolerance_thresh = 0 # 16
    codeLines = []
    FIRST_RULE = True
    actuator = None

    line = "#newValue := *value*;"
    codeLines.append(line)
    line = ""

    line = "#correctValue := TRUE;"
    codeLines.append(line)
    line = ""

    line += "#foundViolations := FALSE;"
    codeLines.append(line)
    line = ""

    for r in rules_data:
        rule_src = r[0]  # [0]
        rule_target = r[1] # [0]
        support = r[2]
        conf = r[3]
        
        s_counter = 0
        s_counter += 1

        
        line += "IF "

        FIRST_RULE_COND = True
        for rs in rule_src:
            rs_name = rs[0]
            rs_value = rs[1]


            if FIRST_RULE_COND:
                FIRST_RULE_COND = False
            else:
                line += " AND "
            # line += rs_name + " >= " + str(rs_value[0]) + " and "+ rs_name + " <= " + str(rs_value[1])

            new_rs_name = rs_name
            if "." in new_rs_name:
                new_rs_name = '"' + new_rs_name[:new_rs_name.find(".")] + '"' + new_rs_name[new_rs_name.find("."):]
            else:
                new_rs_name = '"' + new_rs_name + '"'

            if is_number(str(rs_value[0])):
                line += new_rs_name + " >= " + str(rs_value[0]) + " AND " + new_rs_name + " <= " + str(rs_value[1])
            else:
                line += new_rs_name + " = " + str(rs_value[0].upper())

        line += " THEN"
        codeLines.append(line)
        line = ""

        line += "\tIF ("
        FIRST_RULE_TARGET = True
        for rt in rule_target:
            rt_name = rt[0]
            rt_value = rt[1]

            new_rt_name = rt_name
            if "." in new_rt_name:
                new_rt_name = '"' + new_rt_name[:new_rt_name.find(".")] + '"' + new_rt_name[new_rt_name.find("."):]
            else:
                new_rt_name = '"' + new_rt_name + '"'

            if actuator == None:
                actuator = new_rt_name

            if FIRST_RULE_TARGET:
                FIRST_RULE_TARGET = False
            else:
                line += " AND "
            # line += "newValue >= " + str(rt_value[0]) + " and newValue <= " + str(rt_value[1])
            if is_number(str(rt_value[0])):
                line += "#newValue >= " + str(rt_value[0]) + " AND #newValue <= " + str(rt_value[1]) + ""
            else:
                line += "#newValue = " + str(rt_value[0].upper())

        line += ") = FALSE THEN"
        codeLines.append(line)
        line = ""

        line += "\t\t#foundViolations := TRUE;"
        codeLines.append(line)
        line = ""

        if isinstance(rt_value[0], str):
            if rt_value[0].startswith("("):
                line += "\t\t#correctValue := " + str(get_corrective_value(rt_value[0]))
            else:
                line += "\t\t#correctValue := " + str(rt_value[0].upper())
        else:
            line += "\t\t#correctValue := " + str(rt_value[1])
        codeLines.append(line)
        line = ""

        line = "\tEND_IF;"
        codeLines.append(line)
        line = ""
        
        line = "END_IF;"
        codeLines.append(line)
        line = ""
    
    if not INPUT_VARIABLE:
        line += "IF #foundViolations = FALSE THEN"
        codeLines.append(line)
        line = ""
        line += "\t" + actuator + " := #newValue;"
        codeLines.append(line)
        line = ""
        line = "END_IF;"
        codeLines.append(line)

        line = "ELSE"
        line += "\n\t" + actuator + " := #correctValue;"
        codeLines.append(line)
        line = ""
        line = "END_IF;"
        codeLines.append(line)

    line = ""

    return codeLines

def main():
    rules_data = get_qm_rules()
    codeLines = genCode(rules_data)
    print("\n".join(codeLines))
    

if __name__ == "__main__":
    main()
    

# GENERAL FORM OF PATCH
# RULE: x=[0,2] and y=[3,5] --> actuator=[7,9]
# new_value = value
# if x >= 0 and x <= 2 and y >=3 and y<= 5:
#   if new_value >= 7 and new_value <= 9:
#       actuator = new_value
# elif another_rule:
#   None
# else:
#   actuator = new_value