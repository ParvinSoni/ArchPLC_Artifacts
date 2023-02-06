"""
Description     : Simple Python implementation of the Apriori Algorithm

Usage:
    $python apriori.py -f DATASET.csv -s minSupport  -c minConfidence

    $python apriori.py -f DATASET.csv -s 0.15 -c 0.6
"""

import sys
from os.path import exists
import os

cwd = os.getcwd()
sys.path.append(cwd)


from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser
actuator_f_read = open("input/actuator.txt", "r")
actuator = ""
actuator = actuator_f_read.readlines()[0].strip()
data_columns = []
data_set = {}
outputFile = open("output/rules2.txt", "w")

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
    global data_columns, data_set

    itemSet, transactionList = getItemSetTransactionList(data_iter)
    # print("itemSet: " + str(itemSet))
    # print("transactionList: " + str(transactionList))
    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    assocRules = dict()
    # Dictionary which stores Association Rules

    oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)
    # print("oneCSet: " + str(oneCSet))
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

        # print("currentLSet: " + str(currentLSet))
        # print("transactionList: " + str(transactionList))
        # print("minSupport: " + str(minSupport))
        # print("freqSet: " + str(freqSet))
    def getSupport(item):
        """local function which Returns the support of an item"""
        return float(freqSet[item]) / len(transactionList)

    toRetItems = []
    # print("largeSet: " + str(largeSet))
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

    toRetRules = []
    for key, value in list(largeSet.items())[1:]:
        # print("key: " + str(key))
        # print("value: " + str(value))
        for item in value:
            # print("item: " + str(item))
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                # print("element: " + str(list(element)))

                SKIP = False
                for c in data_columns:
                    if c in list(element) or c in list(item):
                        SKIP = True
                        break
                if SKIP:
                    continue

                remain = item.difference(element)
                # print("remain: " + str(remain))

                if len(remain) > 0:
                    # print(list(item))
                    if list(remain)[0] in list(item):
                        postIndex = list(item).index(list(remain)[0])
                        # print("---")
                        # print("remain: " + str(list(remain)[0]))
                        # print("item: " + str(item))
                        # print("postIndex: " + str(postIndex))
                        # print(data_columns[postIndex])
                        # print(data_columns)
                        # print("---")
                        if data_columns[postIndex] == actuator:
                            # print("GGG")
                            # print(data_columns[postIndex] + " AND " + actuator)
                            # continue
                            # break
                            confidence = getSupport(item) / getSupport(element)
                            if confidence >= minConfidence:
                                # print("R: " + str(((tuple(element), tuple(remain)), confidence)))
                                toRetRules.append(((tuple(element), tuple(remain)), confidence))
    return toRetItems, toRetRules


def printResults(items, rules):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    global outputFile

    # for item, support in sorted(items, key=lambda x: x[1]):
    #     print("item: %s , %.3f" % (str(item), support))
    # print("\n------------------------ RULES:")
    global data_columns, data_set

    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        
        if pre[0] in data_set[data_columns[0]] and post[0] in data_set[data_columns[1]]:
            # print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))
            # 1. support = 1 (1%) , confidence = 100 %  :  gtyp_VGR.di_Pos_DSI_rotate in [0; 0]   -->   QX_VGR_ValveVacuum_Q8 = True
            outputLine = "1. support = 1 (1%) , confidence = 100 %  :  " + str(data_columns[0])
            if str(pre[0]).isnumeric():
                outputLine += " in "
                outputLine += "[" + str(pre[0]) + "; " + str(pre[0]) + "]"
            elif str(pre[0]).lower() == "true" or str(pre[0]).lower() == "false":
                outputLine += " = "
                outputLine += str(pre[0])
            else: 
                # string compare
                outputLine += " = '"
                outputLine += str(pre[0])
                outputLine += "'"
            outputLine += "   -->   "
            outputLine += str(data_columns[1])
            if str(post[0]).isnumeric():
                outputLine += " in "
                outputLine += "[" + str(post[0]) + "; " + str(post[0]) + "]"
            elif str(post[0]).lower() == "true" or str(post[0]).lower() == "false":
                outputLine += " = "
                outputLine += str(post[0])
            else: 
                # string compare
                outputLine += " = '"
                outputLine += str(post[0])
                outputLine += "'"
            print(outputLine)
            outputFile.write(outputLine + "\n")

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


# def dataFromFile(fname):
#     """Function which reads from the file and yields a generator"""
#     global data_columns, data_set
    
#     with open(fname, "rU") as file_iter:
#         FIRST_LINE = True
#         for line in file_iter:
#             if FIRST_LINE:
#                 for c in line.strip().split(","):
#                     data_columns.append(c)
#                     data_set[c] = []
#                 FIRST_LINE = False
#                 continue

#             line = line.strip().rstrip(",")  # Remove trailing comma
#             record = frozenset(line.split(","))
#             splitted_line = line.split(",")
#             for i in range(0, len(splitted_line)):
#                 if not splitted_line[i] in data_set[data_columns[i]]:
#                     data_set[data_columns[i]].append(splitted_line[i])

#             yield record


def dataFromFile(fname):
    """Function which reads from the file and yields a generator"""
    global data_columns, data_set
    
    file_iter = open(fname, "r")
    FIRST_LINE = True
    records = []
    for line in file_iter:
        if FIRST_LINE:
            for c in line.strip().split(","):
                data_columns.append(c)
                data_set[c] = []
            FIRST_LINE = False
            continue

        line = line.strip().rstrip(",")  # Remove trailing comma
        record = frozenset(line.split(","))

        splitted_line = line.split(",")
        for i in range(0, len(splitted_line)):
            if not splitted_line[i] in data_set[data_columns[i]]:
                data_set[data_columns[i]].append(splitted_line[i])
                records.append(record)

    return records
            
def tt():
    print("VV")

def main():
    global data_columns, data_set

    input_path = 'input'
    files = os.listdir(input_path)
    minSupport = 0.01
    minConfidence = 1.0


    for f in files:
        if f.endswith(".txt"):
            continue

        
        path = cwd + "\\" + input_path + "\\" + f
        # print("Processing the file: " + path + "\n")

        data_columns = []
        data_set = {}
        inFile = dataFromFile(path)

        # print(data_columns)
        # continue

        items, rules = runApriori(inFile, minSupport, minConfidence)

        printResults(items, rules)


    '''
    optparser = OptionParser()
    optparser.add_option(
        "-f", "--inputFile", dest="input", help="filename containing csv", default=None
    )
    optparser.add_option(
        "-s",
        "--minSupport",
        dest="minS",
        help="minimum support value",
        default=0.15,
        type="float",
    )
    optparser.add_option(
        "-c",
        "--minConfidence",
        dest="minC",
        help="minimum confidence value",
        default=0.6,
        type="float",
    )

    (options, args) = optparser.parse_args()

    inFile = None
    if options.input is None:
        inFile = sys.stdin
    elif options.input is not None:
        inFile = dataFromFile(options.input)
    else:
        print("No dataset filename specified, system with exit\n")

    minSupport = options.minS
    minConfidence = options.minC

    items, rules = runApriori(inFile, minSupport, minConfidence)

    printResults(items, rules)
    '''

if __name__ == "__main__":
    main()
