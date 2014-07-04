# This file contains the ESN model

# Package import
import numpy as np
import random as random
import math

class esn (object):

	# Constructor
	def __init__ (self, reservoirSize, inputSet, sigma, kappa, gamma, muM=0, muW=0):

		# Next step prediction
		self.predictedVector = None

		# Setting the reservoir size (number of neurons)
		self.n = reservoirSize	

		# Setting gamma
		self.gamma = gamma	

		# Generating U matrix from the inputSet
		self.U = inputSet
		self.m = self.U.shape[0]
		self.T = self.U.shape[1]

		# Generating M matrix
		self.sigma = sigma
		self.muM = muM
		self.M = self.sigma/math.sqrt(self.m)*np.random.randn(self.n, self.m) + self.muM # M is an n x m matrix

		# Generating W matrix
		self.kappa = kappa
		self.muW = muW
		self.W = self.kappa/math.sqrt(self.n)*np.random.randn(self.n, self.n) + self.muW # N is an n x n matrix

		# Initialize X matrix
		self.X = np.zeros((self.n,self.T)) # Initializing the matrix X to 0. X is an n x T matrix
		xPast = self.X[:,0]
		uPast = self.U[:,0]
		

		# Declaring omega solution
		self.omega = None

		# Generating X matrix
		for t in range(1, self.T):

			result = self.W.dot(xPast) + self.M.dot(uPast)
			xFuture = np.array([math.tanh(x) for x in result])
			self.X[:,t] = xFuture

			xPast = xFuture
			uPast = self.U[:,t]


	# Training with the dataset	
	def train (self, timeSteps, outputSet = None):

		self.trainTimeSteps = timeSteps

		# We take as a teacher a part of the inputSet
		if not outputSet == None:
			newU = np.array([self.U[i,:] for i in outputSet])
		else:
			newU = self.U.copy()

		newX = self.X[:,:self.trainTimeSteps]
		newU = newU[:,:self.trainTimeSteps]

		A = newX.dot(newX.transpose()) + self.gamma*np.eye(self.n)
		self.Z = newU[:,1:].copy()
		self.Z = np.concatenate((self.Z, np.zeros((self.m,1))), 1)
		b = newX.dot(self.Z.transpose())

		self.omega = np.linalg.solve(A, b)

	# Predict future values
	def predict (self, predTimeSteps):

		lastX = self.X[:,predTimeSteps].copy()
		self.predictedVector = np.array([self.omega.transpose().dot(lastX).copy()])

	# Prints the info
	def dumpInfo (self):
		print ('U shape : '+str(self.U.shape))
		print ('Z shape : '+str(self.Z.shape))
		print ('X shape : '+str(self.X.shape))
		print ('omega shape : '+str(self.omega.shape))
		print ('n value : '+ str(self.n))
		print ('m value : '+ str(self.m))
		print ('T value : '+ str(self.T))
		print ('\n')

	# Function to ask for ESN parameters
	@staticmethod
	def askESN():
		print '-- Parameters for the ESN --'
		neurons = input("Neurons = ")
		sigma = input("Sigma = ")
		kappa = input("Kappa = ")
		gamma = input("Gamma = ")

		return neurons, sigma, kappa, gamma
