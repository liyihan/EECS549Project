__author__ = 'changliu'

def readDocsCran():
    f = open("dataSet/cran/cran.all.1400")
    preprossedDoc = ""
    index = 1

    readText = False
    for line in f.readlines():
        if line[0] == '.' and line[1] == 'I':
            preprossedDoc = preprossedDoc + str(index) + '\n'
            index = index + 1
            readText = False
        elif line[0] == '.' and line[1] == 'W':
            readText = True
        elif readText:
            preprossedDoc = preprossedDoc + line

    return preprossedDoc

def readDocsNpl():
    f = open("dataSet/npl/doc-text")
    preprossedDoc = ""
    for line in f.readlines():
        if line[0] == " ":
            continue
        else:
            preprossedDoc = preprossedDoc + line

    return preprossedDoc

def readDocs(filename):
    if filename == 'cran':
        return readDocsCran()
    elif filename == 'npl':
        return readDocsNpl()

    '''
    1
    doc 1 is this
    2
    doc 2 is this
    '''
    '''
    [cranDoc]
    '''
    return docs


def readQueriesCran():
    f = open("dataSet/cran/cran.qry")
    preprossedQuery = ""
    index = 1

    readText = False
    for line in f.readlines():
        if line[0] == '.' and line[1] == 'I':
            preprossedQuery = preprossedQuery + str(index) + '\n'
            index = index + 1
            readText = False
        elif line[0] == '.' and line[1] == 'W':
            readText = True
        elif readText:
            preprossedQuery = preprossedQuery + line

    return preprossedQuery


def readQueriesNpl():
    f = open("dataSet/npl/query-text")
    preprossedQuery = ""
    for line in f.readlines():
        if line[0] == "/":
            continue
        else:
            preprossedQuery = preprossedQuery + line

    return preprossedQuery

def readQueries(filename):
    if filename == 'cran':
        return readQueriesCran()
    elif filename == 'npl':
        return readQueriesNpl()

    '''
    1
    query 1 is this
    2
    query 2 is this
    '''
    '''
    [cranQuery]

    'project/dataset/pDataset/'+datasetName+'/'+datasetName+'Query'
    '''
    return queries

def readRel(filename):
    rels = []
    '''
    queryID docID rel
    (irrelevant docs exclusive)
    [cranRel]
    '''
    return rels

def xFoldValidation(x):
    result = []
    '''
    [cranTrain1]
    1 4 7 9

    [cranTest1]
    1 2 3 5

    [cranTrain2]
    1 6 23

    [cranTest2]
    12 34 35
    '''
    return result


cranDocs = readDocs('cran')
cranDocsFile = open("cranDocs.txt", 'w')
cranDocsFile.write(cranDocs)

nplDocs = readDocs('npl')
nplDocsFile = open("nplDocs.txt", 'w')
nplDocsFile.write(nplDocs)

cranQueries = readQueries('cran')
cranQueriesFile = open("cranQueries.txt", 'w')
cranQueriesFile.write(cranQueries)

nplQuries = readQueries('npl')
nplQuriesFile = open("nplQuries.txt", 'w')
nplQuriesFile.write(nplQuries)