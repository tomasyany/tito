# This file contains the constant predictor (prediction = day before value)

# Package import
import numpy as np

class constant (object):

	# Constructor
	def __init__(self, inputSet):
		self.predictedVector = None
		self.realVector = None
		self.inputSet = inputSet

	# No training needed
	def train (self, timeSteps, outputSet = None):
		self.realVector = self.inputSet[:,timeSteps-1]

	# Predicting the same as the day before
	def predict (self, predTimeSteps):
		self.train(predTimeSteps)
		self.predictedVector = np.array([self.realVector])

