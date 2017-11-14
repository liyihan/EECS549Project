__author__ = 'liyihan'

'''
input: test result and ground truth
'''

'''
[cranOtfidf1]
queryID docID result
(sorted)

[cranOtfidf2]

...

[cranOtfidf5]
'''

import numpy as np
import pdb

# in this funciton the score of relevant documents = 1
def MAP(datasetName, fold):
	goldDir = 'dataSet/pDataSet/' + datasetName + '/' + datasetName + 'Test'
	ResultDir = 'dataSet/pDataSet/' + datasetName + '/' + datasetName + 'Otfidf'
	MAPs = []
	# for each fold
	for i in range(fold):
		resultFile = ResultDir + str(i+1) + '.txt'
		goldFile = goldDir + str(i+1) + '.txt'
		result = open(resultFile, 'r').read().split('\n')
		gold = open(goldFile, 'r').read().split('\n')
		gold_dict = {}
		for line in gold:
			[qid, docid, _] = line.split()
			if qid in gold_dict.keys():
				gold_dict[qid].append(docid)
			else:
				gold_dict[qid] = [docid]
		result_dict = {}
		for line in result:
			[qid, docid, _] = line.split()
			if qid in result_dict.keys():
				result_dict[qid].append(docid)
			else:
				result_dict[qid] = [docid]
		avePs = []
		# for each query calculate aveP
		for qid, res in result_dict.items():
			num, corr, avg = 0.0, 0.0, 0.0
			for docid in res:
				num += 1	
				if docid in gold_dict[qid]:
					corr += 1
				avg += corr/num
			avg /= len(res)
			avePs.append(avg)
		MAPs.append(np.mean(avePs))
	return np.mean(MAPs)

print MAP('cran', 3)
