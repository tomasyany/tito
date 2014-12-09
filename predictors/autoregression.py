# This file contains the vector autoregression model with lag p (VAR(p))

# Package import
import numpy as np

class autoregression (object):

	# Constructor
	def __init__ (self, inputSet, lag, gamma):

		# Next step prediction
		self.predictedVector = None

		# Setting the input set
		self.inputSet = inputSet

		# Declaring the matrices
		self.inputY = None
		self.inputZ = None
		self.beta = None # Solution matrix

		# Setting the lag
		self.lag = lag

		# Setting the regularization factor
		self.gamma = gamma

	# Training with the dataset
	def train (self, timeSteps, outputSet = None):

		self.trainTimeSteps = timeSteps

		self.inputY = self.inputSet[:,self.lag:self.trainTimeSteps]

		# Building Z
		self.inputZ = np.ones((1,self.trainTimeSteps - self.lag))
		for i in range(1, self.lag+1, 1):
			self.inputZ = np.concatenate((self.inputZ,self.inputSet[:,self.lag-i:self.trainTimeSteps-i]),axis=0) 

		A = self.inputZ.dot(self.inputZ.transpose())
		b = self.inputZ.dot(self.inputY.transpose())

		self.beta = np.linalg.solve(A+self.gamma*np.eye(A.shape[0]), b)
		self.beta = self.beta.transpose()


	# Predict future values
	def predict (self, predTimeSteps):
		
		lastZ = np.ones((1,1))
		for i in range(1, self.lag+1, 1):
			lastZ = np.concatenate((lastZ, np.array([self.inputSet[:, predTimeSteps+1-i]])), axis=1)

		self.predictedVector = lastZ.dot(self.beta.transpose())

	# Function to ask for autoregression parameters
	@staticmethod
	def askAR():
		print '\n-- Parameters for the autoregression --'
		lag = input("Lag = ")
		gammaAR = input("GammaAR = ")

		return lag, gammaAR
