# This file contains the tests for the database premanager

import sys
sys.path.append ('/Users/tomasyany/Projects/tito')

from miners.premanager import premanager
import numpy as np

data = np.loadtxt('data/firstWords.txt', delimiter = ',')

f = open('data/firstWordIndex.txt')
wordIndex = []
for line in f.readlines():
	line = line.split(',')
	wordIndex.append(line[1].strip())
f.close()

f = open('data/dateIndex.txt')
dateIndex = []
for line in f.readlines():
	line = line.split(',')
	dateIndex.append(line[1].strip())
f.close()

f = open('data/countries.txt')
countries = []
for line in f.readlines():
	countries.append(line.lower().strip('\n'))
f.close()

f = open('data/csCompanies.txt')
companies = []
for line in f.readlines():
	companies.append(line.lower().strip('\n'))
f.close()

domain = companies


# data = np.array([[1,2,3],[40,5,6],[6,6,6],[0,0,1],[0,0,2]])
myManager = premanager(data, dateIndex, wordIndex)

setOfWords = ['iraq', 'obama']

# myManager.chooseDomain(domain)
# myManager.chooseZeros(0.1)
myManager.chooseCorrelated(setOfWords, 0.4, union=False)

# print myManager.data
print myManager.wordIndex
