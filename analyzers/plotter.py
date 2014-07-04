# This file contains the plotting class

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

class plotter (object):

	# Constructor
	def __init__ (self, realTime, predTime, realValues, predictedValues, predictorsNames, errors, errorsNames, avgErrors):

		# Setting the real vector and predicted list of matrices 
		self.realValues = realValues # Contains an array where each row is a word and each column a time step
		self.predictedValues = predictedValues # Contains a list of arrays of predicted values by predictor
												# where each row is a word and each column a time step

		# Setting the errors and errors names
		self.errors = errors # The errors instance contains a list of arrays, where each array corresponds to a predictor,
							# each row of the array to an error type and each column to a timestep
		self.errorsNames = errorsNames

		# Setting the average errors values
		self.avgErrors = avgErrors

		# Setting the number of errors
		self.numErrors = errors[0].shape[0]

		# Setting the time
		self.realTime = realTime
		self.predTime = predTime
		self.years = mdates.YearLocator() # Every year
		self.months = mdates.MonthLocator() # Every month
		self.days = mdates.DayLocator() # Every day

		# Setting the number of predictors
		self.numPredictors = len(predictedValues)

		# Setting the predictor names
		self.predictorsNames = predictorsNames

		# Declaring the figures
		self.figures = []

		# Setting the figures size
		self.figsize = (60,45)
		
	# Plotting real values against predicted ones
	def plotRealPred(self, predTimeIndexes):
		# The predicted values contains a list of arrays, where each array correspond to predicted values for several words
		# through time and each element of the list corresponds to a predictor
		f, ax = plt.subplots(self.numPredictors, 1, sharex=True, sharey=True, figsize=self.figsize)

		amountOfWords = self.predictedValues[0].shape[0]

		for i in range(0, self.numPredictors): # For each predictor a subplot
			for j in range(0, amountOfWords): # For each word a scattering
				realValuesPlot = [self.realValues[j,k] for k in predTimeIndexes]
				ax[i].plot(realValuesPlot, self.predictedValues[i][j,:], 'o')

			if i == self.numPredictors-1:
				ax[i].set_xlabel('Real')

			ax[i].set_ylabel('Predicted')
			ax[i].set_title(self.predictorsNames[i])
			plt.grid()
		f.suptitle('Predicted values against real values')

		self.figures.append(f)

	# Plotting values against time
	def plotRealPredTime(self, wordID, word):
		f1, ax = plt.subplots(self.numPredictors, 1, sharex=True, sharey=True,  figsize=self.figsize)
		for i in range(0, self.numPredictors):
			ax[i].plot(self.realTime, self.realValues[wordID,:], color='b')
			ax[i].plot(self.predTime, self.predictedValues[i][wordID,:], 'r--', label = self.predictorsNames[i])
			ax[i].set_ylabel('Ocurrences')
			plt.grid()
			ax[i].legend()
		f1.suptitle('Predicted & real values through time for \''+word+'\'')


		f2 = plt.figure(figsize=self.figsize)
		ax2 = f2.add_subplot(111)
		ax2.plot(self.realTime, self.realValues[wordID,:], linewidth=2, label = 'Real values')
		for i in range (0,self.numPredictors):
			ax2.plot(self.predTime, self.predictedValues[i][wordID,:], label=self.predictorsNames[i])
		f2.suptitle('Predicted & real values though time for \''+word+'\'')
		ax2.set_ylabel('Ocurrences')
		plt.grid()
		ax2.legend()

		self.figures.append(f1)
		self.figures.append(f2)

	# Plotting error against time
	def plotErrorTime(self):

		f, ax = plt.subplots(self.numErrors, 1, sharex=True, sharey=True,  figsize=self.figsize)
		meanError = 0
		x = range (0,2)

		colors = ['k' ,'r','b', 'g']
		colors = colors[:self.numPredictors]
		for i in range (0, self.numErrors): # For each type of error we have a subplot
			for j,color in zip(range(0, self.numPredictors), colors): # For each predictor we have a curve
				ax[i].plot(self.predTime, self.errors[j][i,:], label = self.predictorsNames[j], color = color)
				meanError = [self.avgErrors[j][i] for k in self.predTime]
				ax[i].plot(self.predTime, meanError,'--', color=color)
				ax[i].set_ylabel(self.errorsNames[i])
		ax[0].legend(bbox_to_anchor=(0., 1.05, 1., .102), loc=3, ncol=self.numPredictors, mode="expand", borderaxespad=0.)

		self.figures.append(f)
 
 	# Plotting error against sigma
	def plotErrorSigma(self, sigma):
		
		f, ax = plt.subplots(self.numErrors, 1, sharex=True, sharey=True,  figsize=self.figsize)
		meanError = 0
		x = range (0,2)

		colors = ['k' ,'r','b', 'g']
		colors = colors[:self.numPredictors]
		for i in range (0, self.numErrors): # For each type of error we have a subplot
			for j,color in zip(range(0, self.numPredictors), colors): # For each predictor we have a curve
				ax[i].plot(sigma, self.errors[j][i,:], label = self.predictorsNames[j], color = color)
				meanError = [self.avgErrors[j][i] for k in sigma]
				ax[i].plot(sigma, meanError,'--', color=color)
				ax[i].set_ylabel(self.errorsNames[i])
		ax[0].legend(bbox_to_anchor=(0., 1.05, 1., .102), loc=3, ncol=self.numPredictors, mode="expand", borderaxespad=0.)
		
		self.figures.append(f)

	# Showing plots
	def generatePlots(self):
		plt.show()

 	# Saving figures
 	def savePlots(self, filename):
 		i = 0
 		for fig in self.figures:
 			fig.savefig('outputs/plots/'+str(i)+filename+'.png')
 			i += 1

 	# Closing all figures
 	def closeFigures(self):
 		plt.close('all')





