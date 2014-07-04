# This file contains the model for the pre-processing of the data

# Package import
import numpy as np
import csv
from datetime import datetime

class premanager (object):

	# Constructor
	def __init__(self, source, domain=None):

		# Declaring the data, data index and word index
		self.data = None  
		self.dateIndex = None
		self.wordIndex = None

		# Setting the source
		self.source = source

		# Setting the domain
		self.domain = domain

	# Loading the data
	def loadData(self, dataFile):
		print "Loading data"
		if self.domain == None:
			self.data = np.loadtxt('data/'+self.source+'/'+dataFile+'.txt',delimiter=',')
		elif self.domain == 'firstWords':
			self.data = np.loadtxt('data/'+self.source+'/'+domain+'.txt',delimiter=',')
		else:
			desired= self.searchIndexes(self.domain)
			with open('data/'+self.source+'/'+dataFile+'.txt', 'r') as fin:
			    reader=csv.reader(fin)
			    self.data=[[int(s) for s in row] for i,row in enumerate(reader) if i in desired]
			self.data = np.array(self.data)
			self.wordIndex = [self.wordIndex[i] for i in desired]

	# Loading the word index
	def loadWordIndex(self, wordIndexFile):
		# Loading the words index
		print "Loading wordIndex"
		f = open('data/'+self.source+'/'+wordIndexFile+'.txt','r')
		self.wordIndex = []
		orderedDomain = []
		for line in f.readlines():
			line = line.split(',')
			word = line[1].strip()
			self.wordIndex.append(word)
			if word in self.domain:
				orderedDomain.append(word)
		f.close()
		self.domain = orderedDomain

	# Loading the date index
	def loadDateIndex(self, dateIndexFile):
		print "Loading dateIndex"
		f = open('data/'+self.source+'/'+dateIndexFile+'.txt', 'r')
		self.dateIndex = []
		date_formatter = '%d/%m/%Y'
		for line in f.readlines():
			line = line.strip().split(',')
			self.dateIndex.append(datetime.strptime(line[1], date_formatter).date())
		f.close()

	# Search for word indexes
	def searchIndexes (self, words):
		indexes = []
		for word in words:
			if word in self.wordIndex:
				indexes.append(self.wordIndex.index(word))
			else:
				pass
		return indexes

	# Choosing the data
	def chooseCorrelated (self, setOfWords, tolerance, union=True):
		corrMatrix = np.corrcoef(self.data)
		whereNan = np.isnan(corrMatrix)
		corrMatrix[whereNan] = 0
		m = self.data.shape[0]

		newWords = []

		if union: # If we want to consider the union of the correlated subsets
					# for each word
			for word in setOfWords:
				# word = word.lower()
				if not word in self.wordIndex:
					print 'Warning: Word \''+ word +'\' not present in the database'
				else:
					pos = self.wordIndex.index(word)
					newWords.append(pos)
					for i in range (0, m):
						if abs(corrMatrix[pos,i]) >= tolerance :
							newWords.append(i)

		else: # If we want to consider the intersection of the correlated subsets
				# for each word
			corrWords = []
			for word in setOfWords:
				wordCorr = []
				if not word in self.wordIndex:
					print 'Warning: Word \''+ word +'\' not present in the database'
				else:
					pos = self.wordIndex.index(word)
					newWords.append(pos)
					for i in range (0, m):
						if abs(corrMatrix[pos,i]) >= tolerance :
							wordCorr.append(i)
					corrWords.append(wordCorr)

			newWords = corrWords[0]
			for i in range(1,len(corrWords)):
				newWords = list(set(newWords) & set(corrWords[i]))

		newWords = list(set(newWords))
		returnData(newWords)

	# Choose from domain
	# (We consider a domain to be a list of words previously related by the user)
	def chooseDomain (self, domain):

		newWords = []

		for word in domain:
			if not word in self.wordIndex:
				print 'Warning: Word \''+ word +'\' not present in the database'
			else:
				newWords.append(self.wordIndex.index(word))

		returnData (newWords)
		
	# Choose 50% of zeros with tolerance h 
	def chooseZeros (self, h):

		wordAmount = self.data.shape[0]
		timeSteps = self.data.shape[1]
		h = h

		newWords = []

		for i in range(0, wordAmount):
			alpha = 1.0-np.count_nonzero(self.data[i,:])/float(timeSteps)

			if alpha >= 0.5 - h and alpha <= 0.5 + h:
				newWords.append(i)

		returnData (newWords)

	# Returning the original data from the manager 
	def returnOriginalData (self):
		return self.data, self.wordIndex, self.dateIndex

	# Returning the modified data from the manager 
	def returnData (self, newWords):
		data = np.array([self.data[i,:] for i in newWords])
		wordIndex = [self.wordIndex[i] for i in newWords]
		dateIndex = self.dateIndex

		return data, wordIndex, dateIndex




