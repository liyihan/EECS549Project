__author__ = 'liyihan'

'''
input: dataset
'''

'''
[cranOtfidf1]
queryID docID result
(sorted)

[cranOtfidf2]

...

[cranOtfidf5]
'''

import nltk
import math
import string
from nltk.stem import *

stemmer = SnowballStemmer("english")
isLowerCase = True
isStem = True
isRemoveStopWords = True
isRemovePunctuation = True
isUnigram = True
stopList = []
testIds = ["0", "1", "2", "3", "4"]
datasetName = "cran"
threshold = -1000

def lowerCase(doc):
    tokens = []
    for token in doc:
        tokens.append(token.lower())
    return tokens

def stem(doc):
    tokens = []
    for token in doc:
        tokens.append(stemmer.stem(token))
    return tokens

def removeStopWords(doc):
    tokens = []
    for token in doc:
        if token not in stopList:
            tokens.append(token)
    return tokens

def removePunctuation(doc):
    tokens = []
    for token in doc:
        if token not in string.punctuation:
            if token != "..":
                tokens.append(token)
    return tokens

def readFiles(fileName):
    docs = {}
    f = open(fileName)
    count = 0
    for line in f.readlines():
        count += 1
        if count % 2 == 0:
            doc = nltk.word_tokenize(line.strip())
            if isLowerCase:
                doc = lowerCase(doc)
            if isStem:
                doc = stem(doc)
            if isRemoveStopWords:
                doc = removeStopWords(doc)
            if isRemovePunctuation:
                doc = removePunctuation(doc)
            docs[count / 2] = doc
    return docs

def readDocs(dataset):
    docs = readFiles(dataset + 'Docs.txt')
    return docs

def readQueries(dataset):
    queries = readFiles(dataset + 'Queries.txt')
    return queries

def readTests(dataset, testId):
    f = open(dataset + "Test" + testId + ".txt")
    return f.readline().split()

def calculateIDF(docs):
    idf = {}
    n = len(docs)
    for id in docs:
        doc = docs[id]
        for token in set(doc):
            if token not in idf:
                idf[token] = 1
            else:
                idf[token] = idf[token] + 1
    for token in idf:
        idf[token] = 1 + math.log10(n/idf[token])
    return idf

def calculateTFIDF(docs, idf):
    tfidfs = {}
    for id in docs:
        doc = docs[id]
        tf = {}
        tfidf = {}
        for token in doc:
            if token not in tf:
                tf[token] = 1
            else:
                tf[token] = tf[token] + 1
        for token in tf:
            tfidf[token] = math.log10(tf[token] + 1) * idf[token]
        tfidfs[id] = tfidf
    return tfidfs

def calculateResult(tfidf, query):
    result = 0
    for token in query:
        if token in tfidf:
            result += tfidf[token]
    return result

def retrive(docs, tfidfs, test, query, resultFile):
    results = {}
    for id in tfidfs:
        result = calculateResult(tfidfs[id], query)
        if docs[id].__len__() == 0:
            result = 0
        else:
            result /= docs[id].__len__()
        results[id] = result
    sortedDocs = sorted(results.iteritems(), key=lambda (k,v): (v,k), reverse = True)
    for doc in sortedDocs:
        if doc[1] > threshold:
            resultFile.write(str(test) + " " + str(doc[0]) + " " + str(doc[1]) + "\n")
        else:
            break

def retriveAll(docs, tfidfs, tests, queries, resultFile):
    for test in tests:
        retrive(docs, tfidfs, test, queries[int(test)], resultFile)

def workOn(dataset):
    f = open("stoplist.txt", "r")
    for line in f:
        if isStem:
            stopList.append(stemmer.stem(line.strip()))
        else:
            stopList.append(line.strip())
    f.close()
    docs = readDocs(dataset)
    queries = readQueries(dataset)
    for testId in testIds:
        tests = readTests(dataset, testId)
        #tests = [1]
        idf = calculateIDF(docs)
        tfidfs = calculateTFIDF(docs, idf)
        resultFile = open(dataset + "Otfidf" + testId + ".txt", "w")
        retriveAll(docs, tfidfs, tests, queries, resultFile)
        resultFile.close()

#-------------------------------------      Main     ---------------------------------------

workOn(datasetName)