# This file contains the framework test

import sys, os
sys.path.append ('/Users/tomasyany/Projects/tito')


# Package import 
import numpy as np
from time import time
from datetime import datetime
import pickle
from collections import OrderedDict
from scipy.stats import pearsonr

from analyzers.plotter import plotter
from analyzers.errors import errors
from analyzers.confusion import confusion

from predictors.autoregression import autoregression
from predictors.constant import constant
from predictors.esn import esn
from predictors.random import randomPred

from miners.premanager import premanager
# from miners.postmanager import postmanager TODO

class allTests(object):

	# Constructor
	def __init__ (self):

		self.source = 'nyTimes'
		self.domain = 'countries'

		# Setting the data premanager
		if not self.domain==None:
			self.myPremanager = premanager(self.source, domain=self.openDomain(self.domain))
		else:
			self.myPremanager = premanager(self.source)

		# Loading all the data into the premanager (ORDER IS IMPORTANT)
		self.myPremanager.loadWordIndex('wordIndex')
		self.myPremanager.loadDateIndex('dateIndex')
		self.myPremanager.loadData('wordDate')

		self.data, self.wordIndex, self.dateIndex = self.myPremanager.returnOriginalData()

		# Setting the errors names
		self.errorsNames = ['MSE', 'RMSE']

	# Function for turning real values into integers
	@staticmethod
	def getIntegerVersion(myArray):
		aux =  myArray.round()
		aux[aux<0] = 0
		return aux

	# Function for returning the contents of a file containing a list of words
	def openDomain (self, fileName):
		f = open('data/setOfWords/'+ fileName+'.txt')
		contents = []
		for line in f.readlines():
			contents.append(line.strip().lower())
		f.close()
		return contents

	# Function for showing the word list by id
	def showWords(self):
		print '\nWord list ordered by index:'
		for index, word in enumerate(self.wordIndex):
			print index, word

	# Function to ask for a wordID
	def askWordID(self):
		wordID = input("WordID (-1 to see the list of available words) = ")
		if wordID == -1:
			self.showWords()
			print('')
			wordID = input("WordID = ")
		return wordID

	# Function to get word by its ID
	def getWordByID(self, wordID):
		return self.wordIndex[wordID]

	# Function to ask for initial and delta timeStep
	@staticmethod
	def askInitDeltaTS():
		initTimeStep = input("Initial timeStep = ")
		deltaTimeStep = input("Delta timeStep = ")
		return initTimeStep, deltaTimeStep

	# Function to ask for trainOnce and integerVersion
	@staticmethod
	def askTrainInteger():
		trainOnce = input("Train only one time ? (1/0) : ")
		integerVersion = input("Integer version ? (1/0) : ")
		return trainOnce, integerVersion

	# Function to train the predictors
	@staticmethod
	def trainPredictors(predictorsList, timeSteps):
		for predictor in predictorsList:
			predictor.train(timeSteps)

	# Function to get the predicted vector for each predictor
	@staticmethod
	def predict(predictorsList, predTimeSteps):
		for predictor in predictorsList:
			predictor.predict(predTimeSteps)

	# Function to get the predicted vector for each predictor
	@staticmethod
	def getPredictedVectors(predictorsList, integerVersion):
		vectors = []

		for predictor in predictorsList:

			if integerVersion:
				vectors.append(allTests.getIntegerVersion(predictor.predictedVector))
			else:
				vectors.append(predictor.predictedVector)

		return vectors

	# Function to print the progress of the test
	@staticmethod
	def printProgress(initTimeStep, T, timeSteps):
		p = (timeSteps-initTimeStep)/float((T-1-initTimeStep)) * 100
		output = "%d%% of the prediction completed" % p
		Printer(output)

	# This function plots informations from results already stored in a file
	def getFromFile(self, filename):
		f = open('outputs/predictions/'+filename, 'r')
		allPredictions, allErrors, predTime, realTime, realValues, predictorsNames, errorsNames = pickle.load(f)
		f.close()

		return allPredictions, allErrors, predTime, realTime, realValues, predictorsNames, errorsNames

	# This function saves information to a file
	def saveToFile(self, filename, allPredictions, allErrors, predTime, realTime, realValues, predictorsNames, errorsNames, parameters, metrics):
		f = open('outputs/predictions/'+filename, 'w')
		pickle.dump([allPredictions, allErrors, predTime], f)
		f.close()

		allTests.saveParametersToFile(filename, parameters)
		allTests.saveMetricsToFile(filename, metrics)

	# This functions saves a dictionnary into a file
	@staticmethod
	def saveParametersToFile(filename, parameters):
		f = open('outputs/parameters/'+filename+'-parameters.csv', 'w')
		for i in parameters:
			f.write(str(i) + ','+str(parameters[i])+'\n')
		f.close()

	# This functions saves performance metrics into a CSV file
	@staticmethod
	def saveMetricsToFile(filename, metrics):
		f = open('outputs/metrics/'+filename+'-metrics.csv', 'w')
		for i in metrics:
			f.write(str(i) + ','+str(metrics[i])+'\n')
		f.close()

	# This functions generates a timestamp
	@staticmethod
	def getTimeStamp():
		return datetime.fromtimestamp(time()).strftime	('%d_%m_%Y-%H_%M_%S')

	# This function plots everything
	def plotEverything(self,realTime, predTime, realValues, allPredictions, predictorsNames, allErrors, errorsNames, wordID, word):
		myPlotter = plotter(realTime, predTime, realValues, allPredictions, predictorsNames, allErrors, errorsNames)
		myPlotter.plotRealPredTime(wordID, word)
		myPlotter.plotErrorTime()
		myPlotter.generatePlot()

	# Function to get the predicted vector for each predictor
	def getEverything(self, predictorsList, initTimeStep, T, deltaTimeStep, inputSet, trainOnce = False, integerVersion = False, nPreds=None):
		print '\n-- Training & Predicting --'
		allPredictions = []
		predTime = []
		predsUpToi = []

		allErrors = []
		for i in range(0,self.numPredictors):
			allErrors.append(errors())

		if not nPreds == None:
			predsUpToi = [0]
			predsUpToi.extend(np.cumsum(nPreds))
			predsUpToi.pop()
		else:
			for i in range(0, self.numPredictors):
				predsUpToi.append(i)

		counter = 0
		for timeSteps in range(initTimeStep, T-deltaTimeStep, deltaTimeStep):

			if trainOnce:
				if timeSteps == initTimeStep: 
					allTests.trainPredictors(predictorsList, timeSteps) # Training the predictors
			else:
				allTests.trainPredictors(predictorsList, timeSteps) # Training the predictors

			predTimeSteps = timeSteps
			allTests.predict(predictorsList, predTimeSteps) # Doing the predictions
			pVecTS = allTests.getPredictedVectors(predictorsList, integerVersion) # Getting the predictions
			realVector = inputSet[:,timeSteps]
			for i in range(0, self.numPredictors):
				if not nPreds == None and nPreds[i]>1:
					aux = 0
					for j in range(predsUpToi[i], predsUpToi[i] + nPreds[i]):
						aux += pVecTS[j]
					aux = aux/float(nPreds[i])
				else:
					aux = pVecTS[predsUpToi[i]]

				if timeSteps == initTimeStep:
					allPredictions.append(aux.transpose())
					allErrors[i].updateErrors(aux, realVector)
				else:
					allPredictions[i] = np.append(allPredictions[i],aux.transpose(),axis=1)
					allErrors[i].updateErrors(aux, realVector)

			predTime.append(self.dateIndex[timeSteps])

			allTests.printProgress(initTimeStep, T, timeSteps)

		allTests.printProgress(initTimeStep, T, T-1)
		print '\n'

		return allPredictions, allErrors, predTime # allPredictions is a list of length numPredictors, where each element is
								# an array of size m x (T-initTimeStep)/deltaTimeStep containing all the
								# predictions for that predictor


	# This test does the following:
	# 	- allows the user to choose the parameters for each predictor
	# 	- allows the user to choose the word to plot (by choosing the id from a list)
	# 	- plot all the differents types of plots in the plotter class
	def test1(self):
		print '\n---- TEST 1 ----\n'

		# Getting ESN parameters
		# neurons,sigma,kappa,gamma = esn.askESN()
		neurons,sigma,kappa,gamma = 500,1,1,0.001

		# Getting autoregression parameters
		# lag, gammaAR = autoregression.askAR()
		lag, gammaAR = 5,0.001

		print '\n-- General parameters --'
		# Getting the wordID
		# wordID = self.askWordID()
		wordID = 0
		word = self.getWordByID(wordID)

		# Getting initTimeStep and deltaTimeStep
		# initTimeStep, deltaTimeStep = allTests.askInitDeltaTS()
		initTimeStep, deltaTimeStep = 4000,1

		inputSet = self.data # Setting the inputSet
		T = inputSet.shape[1] # Setting the total time

		print '\n-- Setting predictors --'
		# Setting the predictors
		myESN = esn(neurons, inputSet, sigma, kappa, gamma)
		myAutoRegression = autoregression(inputSet, lag, gammaAR)
		myRandom = randomPred(inputSet)
		myConstant = constant(inputSet)

		# Setting the predictors names
		self.predictorsNames = ['ESN', 'Autoregression', 'Random', 'Constant']

		predictorsList = [myESN, myAutoRegression, myRandom, myConstant]

		# Setting the number of predictors models
		self.numPredictors = len(predictorsList)

		realTime = self.dateIndex
		realValues = inputSet

		allPredictions, allErrors, predTime = self.getEverything(predictorsList, initTimeStep, T, deltaTimeStep, inputSet, trainOnce = True, integerVersion = True, nPreds=None)

		avgErrors = []
		for i in range(0, self.numPredictors):
			avgErrors.append(allErrors[i].getAvgErrors())

		for i in range(0, self.numPredictors):
			allErrors[i] = allErrors[i].getAllErrors()

		# Plotting
		myPlotter = plotter(realTime, predTime, realValues, allPredictions, self.predictorsNames, allErrors, self.errorsNames, avgErrors)
		myPlotter.plotRealPredTime(wordID, word)
		myPlotter.plotErrorTime()
		myPlotter.generatePlots()

	# This test does the following:
	# 	- takes an average of multiple ESN's
	# 	- allows the user to choose the parameters for each predictor
	# 	- allows the user to choose the word to plot (by choosing the id from a list)
	# 	- plot all the differents types of plots in the plotter class
	def test2(self):
		print '\n---- TEST 2 ----\n'

		# Getting ESN parameters
		nESN = input('Number of ESN\'s = ')
		print ''
		neurons,sigma,kappa,gamma = esn.askESN()
		
		# Getting autoregression parameters
		lag, gammaAR = autoregression.askAR()

		print '\n-- General parameters --'
		# Getting the wordID
		wordID = self.askWordID()
		word = self.getWordByID(wordID)

		# Getting initTimeStep and deltaTimeStep
		initTimeStep, deltaTimeStep = allTests.askInitDeltaTS()

		inputSet = self.data # Setting the inputSet
		T = inputSet.shape[1] # Setting the total time

		print '\n-- Setting predictors --'
		# Setting the predictors
		predictorsList = []
		for i in range(0, nESN):
			myESN = esn(neurons, inputSet, sigma, kappa, gamma)
			predictorsList.append(myESN)
		myAutoRegression = autoregression(inputSet, lag, gammaAR)
		myRandom = randomPred(inputSet)
		myConstant = constant(inputSet)

		predictorsList.extend([myAutoRegression, myRandom, myConstant])

		realTime = self.dateIndex
		realValues = inputSet

		nPreds = [nESN]
		nPreds.extend([1 for i in range(1, self.numPredictors)])

		allPredictions, allErrors, predTime = self.getEverything(predictorsList, initTimeStep, T, deltaTimeStep, inputSet, nPreds)

		# Plotting
		myPlotter = plotter(realTime, predTime, realValues, allPredictions, self.predictorsNames, allErrors, self.errorsNames)
		myPlotter.plotRealPredTime(wordID,word)
		myPlotter.plotErrorTime()
		myPlotter.savePlots()
		myPlotter.generatePlots()

	# This test does the following:
	# 	- chooses correlated words (union)
	# 	- allows the user to choose the parameters for each predictor
	# 	- allows the user to choose the word to plot
	# 	- plot all the differents types of plots in the plotter class
	def test3(self):

		print '\n---- TEST 3 ----\n'

		# Getting the set of words  
		setOfWords = []
		setOfWordsFile = 'nasdaqCompanies'
		f = open ('data/setOfWords/'+setOfWordsFile+'.txt', 'r')
		for line in f.readlines():
			setOfWords.append(line.strip())

		# Getting ESN parameters
		neurons,sigma,kappa,gamma = esn.askESN()
		# neurons,sigma,kappa,gamma = 100,1,1,0.001

		# Getting autoregression parameters
		lag, gammaAR = autoregression.askAR()
		# lag, gammaAR = 4,0.001

		print '\n-- General parameters --'
		# Getting the wordID
		wordID = self.askWordID()
		word = self.getWordByID(wordID)

		# Getting the tolerance
		tolerance = input('Choose the correlation tolerance (union) = ')

		# Getting initTimeStep and deltaTimeStep
		initTimeStep, deltaTimeStep = allTests.askInitDeltaTS()		

		# Choosing correlated words (union)
		self.myPremanager.chooseCorrelated(setOfWords, tolerance, union = True)
		inputSet = self.myPremanager.data
		T = inputSet.shape[1] # Setting the total time
		self.wordIndex = self.myPremanager.wordIndex

		print '\n-- Setting predictors --'
		# Setting the predictors
		myESN = esn(neurons, inputSet, sigma, kappa, gamma)
		myAutoRegression = autoregression(inputSet, lag, gammaAR)
		myRandom = randomPred(inputSet)
		myConstant = constant(inputSet)

		predictorsList = [myESN, myAutoRegression, myRandom, myConstant]

		realTime = self.dateIndex
		realValues = inputSet

		allPredictions, allErrors, predTime = self.getEverything(predictorsList, initTimeStep, T, deltaTimeStep, inputSet)

		# Plotting
		myPlotter = plotter(realTime, predTime, realValues, allPredictions, self.predictorsNames, allErrors, self.errorsNames)
		myPlotter.plotRealPredTime(wordID, word)
		myPlotter.plotErrorTime()
		myPlotter.generatePlots()
		myPlotter.savePlots()

	# This test does the following:
	# 	- chooses correlated words (intersection)
	# 	- automatically chooses the word to plot
	# 	- plot all the differents types of plots in the plotter class
	def test4(self): 

		print '\n---- TEST 4 ----\n'

		# Getting the set of words  
		setOfWords = []
		setOfWordsFile = 'csCompanies'
		f = open ('data/setOfWords/'+setOfWordsFile+'.txt', 'r')
		for line in f.readlines():
			setOfWords.append(line)

		# Getting ESN parameters
		neurons,sigma,kappa,gamma = esn.askESN()

		# Getting autoregression parameters
		lag, gammaAR = autoregression.askAR()

		print '\n-- General parameters --'
		# Getting the wordID
		wordID = 240 # Corresponds to word 'iraq'
		word = self.getWordByID(wordID)

		# Getting the tolerance
		tolerance = input('Choose the correlation tolerance (intersection) = ')

		# Getting initTimeStep and deltaTimeStep
		initTimeStep, deltaTimeStep = allTests.askInitDeltaTS()

		T = inputSet.shape[1] # Setting the total time

		# Choosing correlated words (union)
		self.myPremanager.chooseCorrelated(setOfWords, tolerance, union = False)
		inputSet = self.myPremanager.data
		self.wordIndex = self.myPremanager.wordIndex

		print '\n-- Setting predictors --'
		# Setting the predictors
		myESN = esn(neurons, inputSet, sigma, kappa, gamma)
		myAutoRegression = autoregression(inputSet, lag, gammaAR)
		myRandom = randomPred(inputSet)
		myConstant = constant(inputSet)

		predictorsList = [myESN, myAutoRegression, myRandom, myConstant]

		realTime = self.dateIndex
		realValues = inputSet

		allPredictions, allErrors, predTime = self.getEverything(predictorsList, initTimeStep, T, deltaTimeStep, inputSet)

		# Plotting
		myPlotter = plotter(realTime, predTime, realValues, allPredictions, self.predictorsNames, allErrors, self.errorsNames)
		myPlotter.plotRealPredTime(wordID, word)
		myPlotter.plotErrorTime()
		myPlotter.generatePlot()
		myPlotter.savePlots()

	# This test does the following:
	# 	- chooses domain
	# 	- automatically chooses the word to plot
	# 	- plot all the differents types of plots in the plotter class
	def test5(self):

		print '\n---- TEST 5 ----\n'

		# Getting the set of words  
		domain = []
		domainFile = 'csCompanies'
		f = open ('data/setOfWords/'+setOfWordsFile+'.txt', 'r')
		for line in f.readlines():
			domain.append(line)

		# Getting ESN parameters
		neurons,sigma,kappa,gamma = esn.askESN()

		# Getting autoregression parameters
		lag, gammaAR = autoregression.askAR()

		print '\n-- General parameters --'
		# Getting the wordID
		wordID = 240 # Corresponds to word 'iraq'
		word = self.getWordByID(wordID)

		# Getting initTimeStep and deltaTimeStep
		initTimeStep, deltaTimeStep = allTests.askInitDeltaTS()

		T = inputSet.shape[1] # Setting the total time

		# Choosing correlated words (union)
		self.myPremanager.chooseDomain(domain)
		inputSet = self.myPremanager.data
		self.wordIndex = self.myPremanager.wordIndex

		print '\n-- Setting predictors --'
		# Setting the predictors
		myESN = esn(neurons, inputSet, sigma, kappa, gamma)
		myAutoRegression = autoregression(inputSet, lag, gammaAR)
		myRandom = randomPred(inputSet)
		myConstant = constant(inputSet)

		predictorsList = [myESN, myAutoRegression, myRandom, myConstant]

		realTime = self.dateIndex
		realValues = inputSet

		allPredictions, allErrors, predTime = self.getEverything(predictorsList, initTimeStep, T, deltaTimeStep, inputSet)

		# Plotting
		myPlotter = plotter(realTime, predTime, realValues, allPredictions, self.predictorsNames, allErrors, self.errorsNames)
		myPlotter.plotRealPredTime(wordID, word)
		myPlotter.plotErrorTime()
		myPlotter.generatePlot()
		myPlotter.savePlots()

	# This test does the following:
	# 	- chooses words with 50% of zeros
	# 	- allows user to choose the word to plot (by choosing the if form a list)
	# 	- plot all the differents types of plots in the plotter class
	def test6(self):

		print '\n---- TEST 6 ----\n'

		# Getting ESN parameters
		neurons,sigma,kappa,gamma = esn.askESN()

		# Getting autoregression parameters
		lag, gammaAR = autoregression.askAR()

		print '\n-- General parameters --'
		# Getting the wordID
		wordID = 240 # Corresponds to word 'iraq'
		word = self.getWordByID(wordID)

		# Getting the tolerance
		h = input('Choose the tolerance h = ')

		# Getting initTimeStep and deltaTimeStep
		initTimeStep, deltaTimeStep = allTests.askInitDeltaTS()

		T = inputSet.shape[1] # Setting the total time

		# Choosing correlated words (union)
		self.myPremanager.chooseZeros(h)
		inputSet = self.myPremanager.data
		self.wordIndex = self.myPremanager.wordIndex

		print '\n-- Setting predictors --'
		# Setting the predictors
		myESN = esn(neurons, inputSet, sigma, kappa, gamma)
		myAutoRegression = autoregression(inputSet, lag, gammaAR)
		myRandom = randomPred(inputSet)
		myConstant = constant(inputSet)

		predictorsList = [myESN, myAutoRegression, myRandom, myConstant]

		realTime = self.dateIndex
		realValues = inputSet

		allPredictions, allErrors, predTime = self.getEverything(predictorsList, initTimeStep, T, deltaTimeStep, inputSet)

		# Plotting
		myPlotter = plotter(realTime, predTime, realValues, allPredictions, self.predictorsNames, allErrors, self.errorsNames)
		myPlotter.plotRealPredTime(wordID, word)
		myPlotter.plotErrorTime()
		myPlotter.generatePlot()
		myPlotter.savePlots()

	# This test does the following:
	# 	- tests for different values of n, sigma, kappa, gamma, gammaVAR, etc.
	# 	- saves the information to a file to be able to load it later
	def test7(self):

		print '\n---- TEST 7 ----\n'

	

		# Getting ESN parameters
		neurons,sigma,kappa,gamma = esn.askESN()
		# neurons,sigma,kappa,gamma = 500,1,1,0.001

		# Getting autoregression parameters
		lag, gammaAR = autoregression.askAR()
		# lag, gammaAR = 5,0.001

		print '\n-- General parameters --'
		# Getting the wordID
		# wordID = self.askWordID()
		wordID = 0
		word = self.getWordByID(wordID)

		# Getting initTimeStep and deltaTimeStep
		# initTimeStep, deltaTimeStep = allTests.askInitDeltaTS()
		initTimeStep, deltaTimeStep = 3500,1

		# Getting trainOnce and integerVersion
		# trainOnce, integerVersion = self.askTrainInteger()
		trainOnce, integerVersion = True, True

		inputSet = self.data # Setting the inputSet
		T = inputSet.shape[1] # Setting the total time

		print '\n-- Setting predictors --'
		# Setting the predictors
		myESN = esn(neurons, inputSet, sigma, kappa, gamma)
		myAutoRegression = autoregression(inputSet, lag, gammaAR)
		myRandom = randomPred(inputSet)
		myConstant = constant(inputSet)

		# Setting the predictors names
		predictorsNames = ['ESN', 'Autoregression', 'Constant']

		predictorsList = [myESN, myAutoRegression, myConstant]

		# Setting the number of predictors models
		self.numPredictors = len(predictorsList)

		realTime = self.dateIndex
		realValues = inputSet

		allPredictions, allErrors, predTime = self.getEverything(predictorsList, initTimeStep, T, deltaTimeStep, inputSet, trainOnce = trainOnce, integerVersion = integerVersion, nPreds=None)

		# Getting timestamp
		ts = allTests.getTimeStamp()

		filename = 'TEST7-'+ ts

		# Storing parameters
		parameters = OrderedDict()
		parameters['-- ESN --'] = ''
		parameters['neurons'] = neurons
		parameters['sigma'] = sigma
		parameters['kappa'] = kappa
		parameters['gamma'] = gamma
		parameters[''] = '\n' 
		parameters['-- VAR --'] = ''
		parameters['lag'] = lag
		parameters['gammaAR'] = gammaAR
		parameters[' '] = '\n ' 
		parameters['-- General Parameters --'] = ''
		parameters['source']= self.source
		parameters['domain']= self.domain

		parameters['wordID'] = wordID
		parameters['word'] = word
		parameters['initTimeStep'] = initTimeStep
		parameters['deltaTimeStep'] = deltaTimeStep
		parameters['predictorsNames'] = predictorsNames
		
		# Storing metrics
		metrics = OrderedDict()
		avgErrors=[]
		predTimeIndexes = []
		for i in range(0,self.numPredictors):
			metrics['-- '+predictorsNames[i]+' --']=''
			for j in range(0,len(self.errorsNames)):
				metrics[predictorsNames[i]+'_Avg'+self.errorsNames[j]] = allErrors[i].getAvgErrors()[j]

			corr = 0
			k=0
			for j in range(initTimeStep, T-deltaTimeStep, deltaTimeStep):
				realCorr = realValues[:,j]
				predCorr = allPredictions[i][:,k]
				corr = corr + pearsonr(realCorr, predCorr)[0]
				k += 1

				if i==0:
					predTimeIndexes.append(j)

			corr = corr/float(k)
			metrics[predictorsNames[i]+'_'+'PearsonCorrAvgTIME'] = corr

			avgErrors.append(allErrors[i].getAvgErrors()) # Appending the avg errors
			allErrors[i] = allErrors[i].getAllErrors() # Getting the matrix of errors from the object

			metrics[' '*i]='\n'

		# Saving everything to different files
		self.saveToFile(filename, allPredictions, allErrors, predTime, realTime, realValues, predictorsNames, self.errorsNames, parameters, metrics)			

		# Plotting
		myPlotter = plotter(realTime, predTime, realValues, allPredictions, predictorsNames, allErrors, self.errorsNames, avgErrors)
		myPlotter.plotRealPredTime(wordID, word)
		myPlotter.plotRealPred(predTimeIndexes)
		myPlotter.plotErrorTime()
		myPlotter.savePlots(filename)
		myPlotter.generatePlots()
		myPlotter.closeFigures()

		



class Printer():
	def __init__(self, data):
		sys.stdout.write("\r\x1b[K"+data.__str__())
		sys.stdout.flush()

if __name__ == '__main__':

	t = allTests()

	answer = 1
	while answer == 1:
		os.system('clear')
		t.test7()
		os.system('clear')
		answer = input ("Would you like to do it again? (1/0): ")
