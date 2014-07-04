# This file contains the tests for the ESN model OBSOLETE

# Package import
from analyzers.confusion import confusion
from analyzers.plotter import plotter
from analyzers.errors import errors
from predictors.esn import esn
import numpy as np
import sys

class Printer():
	def __init__(self, data):
		sys.stdout.write("\r\x1b[K"+data.__str__())
		sys.stdout.flush()

class esnTest (object):

	# Constructor
	def __init__(self):

		self.wordID = 239
		# wordID = input("Choose wordID: ")

		print('Getting input from text\n')

		# self.dataSet = np.loadtxt('data/wordDate.txt', delimiter=',')
		self.dataSet = np.loadtxt('data/firstWords.txt', delimiter=',')
		# self.dataSet = np.loadtxt('data/fakeWordDate.txt', delimiter=',')

		self.inputSet = self.dataSet.copy()


		# If wanted, we start from a certain point in time
		decTemps = 0
		self.dataSet = self.dataSet[:,decTemps:]

		# Searching the word corresponding to wordID
		wordIndex = open('data/wordIndex.txt', 'r')
		for i in range(0,self.wordID):
			wordIndex.readline()
		self.word = wordIndex.readline().split(',')[1]
		wordIndex.close()

	# Test for 1 ESN
	def test1(self):

		neurons = 100
		sigma = 1
		kappa = 1
		gamma = 0.001
		numberOfWords = 300

		# neurons = input("Choose the number of neurons: ")
		# sigma = input("Choose sigma: ")
		# kappa = input("Choose kappa: ")
		# gamma = input("Choose gamma: ")
		# numberOfWords = input("Choose the number of words: ")

		print ('Building the ESN')

		conf = confusion()
		errorSet = errors()
		predVectors = []
		realVectors = []
		time = []

		myESN = esn(neurons, self.inputSet.copy(), sigma, kappa, gamma=gamma)

		realVectors = np.array()

		i=0
		for tF in range (1, 100, 1):
			# tF = tF / 10.0
			tF = tF/100.0

			conf.goZero()

			# print('Prediction '+str(i)+':')

			myESN.train(timeFraction = tF)

			# print ('Training = DONE (with '+str(tF*100)+'% of the total time)')
			
			myESN.predict()

			realVector = #TODO
			predVector = myESN.predictedVector.copy()

			conf.updateConfMatrix(predVector, realVector)
			errorSet.updateErrors(predVector, realVector) 

			predVectors.append(predVector[:numberOfWords])
			# realVectors.append(realVector[:numberOfWords])
			np.concatenate((realVectors,realVector([:numberOfWords])),1)
			time.append(myESN.trainTimeSteps + 1)
			
			# conf.dumpInfo()
			# errorSet.dumpInfo()

			# print ('------------------------------------------------------')

			p = tF * 100
			output = "%d%% of the test completed" % p
			Printer(output)

			i+=1

		error = errorSet.RMSE

		print realVectors

		myPlotter = plotter(10,10)
		myPlotter.plotRealPred(realVectors, predVectors)
		myPlotter.plotRealPredTime(realVectors[239,:], predVectors[239,:], time)
		myPlotter.plotErrorTime(error,time)
		myPlotter.generatePlot()


	# Test for multiple ESN's 
	def test2(self):

		neurons = 100
		nESN = 10
		sigma = 1
		kappa = 1
		gamma = 0.001
		numberOfWords = 300

		# neurons = input("Choose the number of neurons: ")
		# nESN = input("Choose the amount of ESN's: ")
		# sigma = input("Choose sigma: ")
		# kappa = input("Choose kappa: ")
		# gamma = input("Choose gamma: ")
		# wordID = input("Choose wordID: ")
		# numberOfWords = input("Choose the number of words: ")

		conf = confusion()
		errorSet = errors()
		predVectors = []
		realVectors = []
		time = []
		esnSet = []

		for i in range (0, nESN):
			esnSet.append(esn(neurons, self.inputSet.copy(), sigma, kappa, gamma=gamma))

		for tF in range(1, 100, 1):
			tF = tF / 100.0
			conf.goZero()
			predVector = 0
			for i in range (0, nESN):
				currentEsn = esnSet[i]
				currentEsn.train(timeFraction = tF)
				currentEsn.predict()
				predVector += currentEsn.predictedVector.copy()
				
			realVector = currentEsn.realVector.copy()
			predVector = predVector / float(nESN)

			conf.updateConfMatrix(predVector, realVector)
			errorSet.updateErrors(predVector, realVector)

			predVectors.append(predVector[:numberOfWords])
			realVectors.append(realVector[:numberOfWords])
			time.append(currentEsn.trainTimeSteps + 1)

			p = tF * 100
			output = "%d%% of the test completed" % p
			Printer(output)

		error = errorSet.RMSE

		myPlotter = plotter(10,10)
		myPlotter.plotRealPred(realVectors, predVectors)
		myPlotter.plotErrorTime(error,time)
		myPlotter.generatePlot()


	# Test for multiple ESN's 
	def test3(self):

		neurons = 100
		maxSigma = 10
		kappa = 1
		gamma = 0.001
		numberOfWords = 300

		# neurons = input("Choose the number of neurons: ")
		# nESN = input("Choose the amount of ESN's: ")
		# gamma = input("Choose gamma: ")
		# wordID = input("Choose wordID: ")
		# numberOfWords = input("Choose the number of words: ")

		error = []
		sigmas = []

		for sigma in range (0, 100, 1):
			sigma = sigma/10.0
			currentEsn = esn(neurons, self.inputSet.copy(), sigma, kappa, gamma=gamma)
			errorSet = errors()

			for tF in range(1, 100, 2):
				tF = tF / 100.0
				currentEsn.train(timeFraction = tF)
				currentEsn.predict()

				predVector = currentEsn.predictedVector.copy()	
				realVector = currentEsn.realVector.copy()

				errorSet.updateErrors(predVector, realVector)

			p = sigma * 10
			output = "%d%% of the test completed" % p
			Printer(output)

			meanError = sum(errorSet.RMSE)/len(errorSet.RMSE)
			error.append(meanError)
			sigmas.append(sigma)

		myPlotter = plotter(10,10)
		myPlotter.plotErrorSigma(error,sigmas)
		myPlotter.generatePlot()

	# Test for one ESN and inputSet = 1 word 
	def test4(self):

		neurons = 100
		sigma = 1
		kappa = 1
		gamma = 0.001
		numberOfWords = 1

		# neurons = input("Choose the number of neurons: ")
		# sigma = input("Choose sigma: ")
		# kappa = input("Choose kappa: ")
		# gamma = input("Choose gamma: ")
		# numberOfWords = input("Choose the number of words: ")

		print ('Building the ESN')

		conf = confusion()
		errorSet = errors()
		predVectors = []
		realVectors = []
		time = []

		self.changeInputSet([239])
		myESN = esn(neurons, self.inputSet, sigma, kappa, gamma=gamma)

		i=0
		for tF in range (1, 100, 1):
			# tF = tF / 10.0
			tF = tF/100.0

			conf.goZero()

			# print('Prediction '+str(i)+':')

			myESN.train(timeFraction = tF)

			# print ('Training = DONE (with '+str(tF*100)+'% of the total time)')
			
			myESN.predict()

			realVector = myESN.realVector.copy()
			predVector = myESN.predictedVector.copy()

			conf.updateConfMatrix(predVector, realVector)
			errorSet.updateErrors(predVector, realVector) 

			predVectors.append(predVector[:numberOfWords])
			realVectors.append(realVector[:numberOfWords])
			time.append(myESN.trainTimeSteps + 1)
			
			# conf.dumpInfo()
			# errorSet.dumpInfo()

			# print ('------------------------------------------------------')

			p = tF * 100
			output = "%d%% of the test completed" % p
			Printer(output)

			i+=1

		error = errorSet.RMSE

		myPlotter = plotter(10,10)
		myPlotter.plotRealPred(realVectors, predVectors)
		myPlotter.generatePlot()
		myPlotter.plotRealPredTime(realVectors, predVectors, time)
		myPlotter.generatePlot()
		myPlotter.plotErrorTime(error,time)
		myPlotter.generatePlot()