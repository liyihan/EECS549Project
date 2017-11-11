__author__ = 'liyihan'

def readDocsCran():
    docs = []
    return docs

def readDocsNpl():
    docs = []
    return docs

def readDocs(filename):
    '''
    1
    doc 1 is this
    2
    doc 2 is this
    '''
    '''
    [cranDoc]
    '''

    docs = []
    if filename == 'cran':
        return readDocsCran()
    elif filename == 'npl':
        return readDocsNpl()

def readQueries(filename):
    queries = []
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