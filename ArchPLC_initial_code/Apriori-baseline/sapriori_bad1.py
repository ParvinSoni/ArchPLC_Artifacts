"""
Description     : Simple Python implementation of the Apriori Algorithm

Usage:
    $python apriori.py -f DATASET.csv -s minSupport  -c minConfidence

    $python apriori.py -f DATASET.csv -s 0.15 -c 0.6
"""

import sys

from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser
actuator_f_read = open("input/actuator.txt", "r")
actuator = ""
actuator = actuator_f_read.readlines()[0].strip()
data_columns = []

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
            if set(item).issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1

    for item, count in localSet.items():
        support = float(count) / len(transactionList)

        if support >= minSupport:
            _itemSet.add(item)

    return _itemSet


def joinSet(itemSet, length, actuator_itemSet, actuator_transactionList):
    """Join a set with itself and returns the n-element itemsets"""
    res = []

    print(actuator_transactionList)
    for i in itemSet:
        joinedSet = [i]
        # print("actuator_itemSet: " + str(actuator_itemSet))
        for j in actuator_itemSet:
            joinedSet.append(j)
            # print(joinedSet)
            # print("*")
            # sys.exit()
            
            if len(joinedSet) == length:
                print("2222222")
                print(joinedSet)
                res.append(tuple(joinedSet))

    return set(res)

    # for k in itemSet:
    #     print(k)
    # print(type(itemSet))
    # print(itemSet)
    # # return set([set(i).union(set(j)) for i in itemSet for j in itemSet if len(set(i).union(set(j))) == length])
    # return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()

    FIRST_LINE = True
    for record in data_iterator:
        if FIRST_LINE:
            FIRST_LINE = False
            continue
        transaction = tuple(record[:-1])
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(tuple([item]))  # Generate 1-itemSets
    return itemSet, transactionList


def getActuatorItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()

    FIRST_LINE = True

    for record in data_iterator:
        if FIRST_LINE:
            FIRST_LINE = False
            continue
        transaction = record[-1:]
        print(transaction)
        if not transaction in transaction:
            transactionList.append(transaction)
            for item in transaction:
                itemSet.add(tuple([item]))  # Generate 1-itemSets
    return set(itemSet), set(transactionList)

def runApriori(data_iter, minSupport, minConfidence, data_iter2):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence)
    """
    global data_columns

    itemSet, transactionList = getItemSetTransactionList(data_iter)
    actuator_itemSet, actuator_transactionList = getActuatorItemSetTransactionList(data_iter2)
    # print("itemSet: " + str(itemSet))
    print("transactionList: " + str(transactionList))
    # sys.exit()
    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    assocRules = dict()
    # Dictionary which stores Association Rules

    
    oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)
    print("oneCSet: " + str(oneCSet))
    print("actuator_transactionList: " + str(actuator_transactionList))
    # sys,exit()
    currentLSet = oneCSet
    k = 2
    while currentLSet != set([]):
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k, actuator_itemSet, actuator_transactionList)
        print("A: " + str(currentLSet))
        # sys.exit()
        currentCSet = returnItemsWithMinSupport(currentLSet, transactionList, minSupport, freqSet)
        currentLSet = currentCSet
        k = k + 1

        # print("currentLSet: " + str(currentLSet))
        # print("transactionList: " + str(transactionList))
        # print("minSupport: " + str(minSupport))
        # print("freqSet: " + str(freqSet))
        # sys.exit()
    def getSupport(item):
        """local function which Returns the support of an item"""
        return float(freqSet[item]) / len(transactionList)

    toRetItems = []
    print("largeSet: " + str(largeSet))
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

    toRetRules = []
    for key, value in list(largeSet.items())[1:]:
        # print("key: " + str(key))
        # print("value: " + str(value))
        for item in value:
            # print("item: " + str(item))
            _subsets = map(tuple, [x for x in subsets(item)])
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
                                print("R: " + str(((tuple(element), tuple(remain)), confidence)))
                                toRetRules.append(((tuple(element), tuple(remain)), confidence))
    return toRetItems, toRetRules


def printResults(items, rules):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    # for item, support in sorted(items, key=lambda x: x[1]):
    #     print("item: %s , %.3f" % (str(item), support))
    # print("\n------------------------ RULES:")
    global data_columns

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
    global data_columns

    with open(fname, "rU") as file_iter:
        FIRST_LINE = True
        for line in file_iter:
            line = line.strip().rstrip(",")  # Remove trailing comma
            record = tuple(line.split(","))
            print(record)
            if FIRST_LINE:
                data_columns = list(record)[:]
                # for c in line.split(","):
                    # data_columns.append(c.strip())
                # print(data_columns)
                # print(line)

            FIRST_LINE = False

            yield record

            



if __name__ == "__main__":

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
    inFile2 = None
    if options.input is None:
        inFile = sys.stdin
    elif options.input is not None:
        inFile = dataFromFile(options.input)
        inFile2 = dataFromFile(options.input)
    else:
        print("No dataset filename specified, system with exit\n")
        sys.exit("System will exit")

    minSupport = options.minS
    minConfidence = options.minC

    items, rules = runApriori(inFile, minSupport, minConfidence, inFile2)

    printResults(items, rules)
