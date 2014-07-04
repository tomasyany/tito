# This file constains a random prediction model (Gaussian law)

# Package import 
import numpy as np

class randomPred (object):

	# Constructor
	def __init__ (self, inputSet, multi = False):

		# Setting the input set
		self.inputSet = inputSet

		# Declaring the mean and covariance matrix of the Gaussian multivariate distribution
		self.mu = None
		self.sigma = None

		# Declaring the predicted vector
		self.predictedVector = None

		# Setting multivariate boolean
		self.multi = multi

	# Training with the inputSet
	def train (self, timeSteps, outputSet = None):
		self.mu = np.mean(self.inputSet[:,:timeSteps], axis = 1)

		if (self.multi):
			self.cov = np.cov(self.inputSet[:,:timeSteps])
		else:
			self.sigma = np.std(self.inputSet[:,:timeSteps], axis = 1)

	# Predict future values
	def predict (self, predTimeSteps):
		if (self.multi):
			self.predictedVector = np.array([np.random.multivariate_normal(self.mu, self.cov)])
		else:
			self.predictedVector = np.array([self.sigma[i]*np.random.randn()+self.mu[i] for i in range(0, self.inputSet.shape[0])])
			self.predictedVector = np.array([self.predictedVector])