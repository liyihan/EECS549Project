__author__ = 'changliu'

def readDocsCran():
    f = open("dataSet/cran/cran.all.1400")
    preprossedDoc = ""
    index = 1

    readText = False
    for line in f.readlines():
        if line[0] == '.' and line[1] == 'I':
            preprossedDoc = preprossedDoc + '\n' + str(index) + '\n'
            index = index + 1
            readText = False
        elif line[0] == '.' and line[1] == 'W':
            readText = True
        elif readText:
            preprossedDoc = preprossedDoc + line[:-1]

    return preprossedDoc[1:]

def readDocsNpl():
    f = open("dataSet/npl/doc-text")
    preprossedDoc = ""
    newLine = True
    for line in f.readlines():
        if line[0] == " ":
            preprossedDoc = preprossedDoc + '\n'
            newLine = True
        else:
            if newLine:
                preprossedDoc = preprossedDoc + line
                newLine = False
            else:
                preprossedDoc = preprossedDoc + line[:-1]

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


###################################################################################################


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


###################################################################################################


def readRelNpl():
    f = open("dataSet/npl/rlv-ass")
    preprossedRel = ""

    query_rel = dict()
    relArrary = []

    Index = 1
    whetherIndex = True
    for line in f.readlines():
        if whetherIndex:
            query_rel[Index] = []
            whetherIndex = False
        else:
            if line[3] == '/':
                whetherIndex = True
                Index = Index + 1;
            else:
                query_rel[Index].extend([int(x) for x in line.split()])

    rel = ""
    for key in query_rel:
        for n in query_rel[key]:
            rel = rel + str(key) + ' ' + str(n) + ' ' + str(1) + '\n'

    return rel

class cranRel:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __gt__(self, other):
        if self.a != other.a:
            return self.a > other.a
        else:
            if self.c != other.c:
                return self.c > other.c
            else:
                return self.b > other.b



def readRelCran():
    f = open("dataSet/cran/cranqrel")
    arr = []
    for line in f.readlines():
        temp = [int(x) for x in line.split()]
        arr.append(cranRel(temp[0], temp[1], temp[2]))

    arr.sort()

    res = ""
    for ele in arr:
        res = res + str(ele.a) + " " + str(ele.b) + " " + str(ele.c) + "\n"

    return res


def readRel(filename):
    if filename == 'npl':
        return readRelNpl()
    elif filename == 'cran':
        return readRelCran()
    '''
    queryID docID rel
    (irrelevant docs exclusive)
    [cranRel]
    '''


###################################################################################################


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
'''
cranQueries = readQueries('cran')
cranQueriesFile = open("cranQueries.txt", 'w')
cranQueriesFile.write(cranQueries)

nplQuries = readQueries('npl')
nplQuriesFile = open("nplQuries.txt", 'w')
nplQuriesFile.write(nplQuries)
'''
nplRel = readRel('npl')
nplRelFile = open("nplRel.txt", 'w')
nplRelFile.write(nplRel)

cranRel = readRel('cran')
cranRelFile = open("cranRel.txt", 'w')
cranRelFile.write(cranRel)



