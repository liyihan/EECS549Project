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
import string
import os
from nltk.stem import *
import math

stemmer = SnowballStemmer("english")
isLowerCase = True
isStem = True
isRemoveStopWords = True
isRemovePunctuation = True
isUnigram = False
stopList = []
testIds = ["0", "1", "2", "3", "4"]
datasetName = "cran"
thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

def QBFunc(tfidf, qtf):
    value = tfidf * qtf
    return value

def printThresholds():
    f = open("thresholds.txt", "w")
    for threshold in thresholds:
        f.write(str(threshold) + "\n")
    f.close()


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

def bigram(doc):
    tokens = []
    for i in range(0, doc.__len__() - 1):
        tokens.append(doc[i] + ' ' + doc[i + 1])
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
            if not isUnigram:
                doc = bigram(doc)
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

def calculateTFIDF(doc, idf):
    tf = {}
    tfidf = {}
    for token in doc:
        if token not in idf:
            continue
        if token not in tf:
            tf[token] = 1
        else:
            tf[token] = tf[token] + 1
    for token in tf:
        tfidf[token] = math.log10(tf[token] + 1) * idf[token]
    return tfidf

def calculateTFIDFs(docs, idf):
    tfidfs = {}
    for id in docs:
        doc = docs[id]
        tfidfs[id] = calculateTFIDF(doc, idf)
    return tfidfs

def calculateNorms(tfidfs, qTf):
    norms = {}
    for id in tfidfs:
        total = 0
        tfidf = tfidfs[id]
        for token in tfidf:
            if token in qTf:
                total += QBFunc(tfidf[token], qTf[token])
            else:
                total += tfidf[token] * tfidf[token]
        norms[id] = total
    return norms

def calculateResult(dTfidf, qTfidf, dNorm, qTf):
    result = 0
    qNorm = 0
    for token in qTfidf:
        if token in dTfidf:
            if token in qTf:
                qNorm += QBFunc(qTfidf[token], qTf[token]) * QBFunc(qTfidf[token], qTf[token])
                result += QBFunc(qTfidf[token], qTf[token]) * QBFunc(dTfidf[token], qTf[token])
            else:
                qNorm += qTfidf[token] * qTfidf[token]
                result += qTfidf[token] * dTfidf[token]
    if dNorm != 0:
        result = result/math.sqrt(dNorm)
    if qNorm != 0:
        result = result/math.sqrt(qNorm)
    return result

def retrieve(docs, idf, tfidfs, qTf, docNorms, test, query, resultFile, threshold):
    results = {}
    for id in tfidfs:
        queryTfidf = calculateTFIDF(query, idf)
        result = calculateResult(tfidfs[id], queryTfidf, docNorms[id], qTf)
        if docs[id].__len__() == 0:
            result = 0
        results[id] = result
    sortedDocs = sorted(results.iteritems(), key=lambda (k,v): (v,k), reverse = True)
    for doc in sortedDocs:
        if doc[1] > threshold:
            resultFile.write(str(test) + " " + str(doc[0]) + " " + str(doc[1]) + "\n")
        else:
            break

def retrieveAll(docs, idf, tfidfs, qTf, norms, tests, queries, resultFile, threshhold):
    for test in tests:
        retrieve(docs, idf, tfidfs, qTf, norms, test, queries[int(test)], resultFile, threshhold)

def train(idf, tests, queries):
    qTf = {}
    for queryId in queries:
        if str(queryId) not in tests:
            for token in queries[queryId]:
                if token in idf:
                    if token in qTf:
                        qTf[token] = qTf[token] + 1
                    else:
                        qTf[token] = 1
    return qTf

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
    idf = calculateIDF(docs)
    tfidfs = calculateTFIDFs(docs, idf)
    for threshold in thresholds:
        directory = str(threshold)
        if not os.path.exists(directory):
            os.makedirs(directory)
        for testId in testIds:
            print "Retrive testID: " + testId + " with threshold: " + directory
            tests = readTests(dataset, testId)
            qTf = train(idf, tests, queries)
            docsNorms = calculateNorms(tfidfs, qTf)
            outName = directory + "/" + dataset + "QBtfidf"
            if not isUnigram:
                outName = outName + "Bi"
            outName = outName + testId + ".txt"
            resultFile = open(outName, "w")
            retrieveAll(docs, idf, tfidfs, qTf, docsNorms, tests, queries, resultFile, threshold)
            resultFile.close()

#-------------------------------------      Main     ---------------------------------------

printThresholds()
workOn(datasetName)