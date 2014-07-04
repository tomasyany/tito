# This file contains the different errors analyzers

# Package import
import numpy as np
from math import sqrt

class errors(object):

	# Constructor
	def __init__(self):

		# Declaring the errors
		self.MSE = [] # Mean Squared Error 
		self.RMSE = [] # Root Mean Squared Error

		# Declaring error means
		self.meanMSE = 0
		self.meanRMSE = 0

	# Updating all kind of errors
	def updateErrors (self, predVector, realVector):

		# Getting the errors
		mse, rmse = errors.getMseRmse (predVector, realVector)

		# Updating the MSE
		self.MSE.append (mse)

		# Updating the RMSE
		self.RMSE.append (rmse)

		# Updating the means
		self.meanMSE = (self.meanMSE * (len(self.MSE)-1) + mse) / len(self.MSE)
		self.meanRMSE = (self.meanRMSE * (len(self.RMSE)-1) + rmse) / len(self.RMSE)


	# Computes MSE and RMSE errors
	@staticmethod
	def getMseRmse (predVector, realVector):

		error = predVector - realVector
		mse = sum(i*i for i in error[0])/float(len(error[0]))
		rmse = sqrt(mse)
		return mse, rmse

	def getAllErrors (self):
		allErrors = np.array([self.MSE, self.RMSE])
		return allErrors

	def getAvgErrors (self):
		return self.meanMSE, self.meanRMSE


		
