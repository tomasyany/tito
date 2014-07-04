# This file contains the confusion matrix anlysis

import matplotlib.pyplot as plt

class confusion():

	def __init__(self):

		self.confusionMatrix = {'truePositive':0,'falsePositive':0,'falseNegative':0,'trueNegative':0}
		self.partPourcentage = {'truePositive':0,'falsePositive':0,'falseNegative':0,'trueNegative':0}
		self.totalValues = 0

	# Function for setting values of the matrix to 0
	def goZero(self):
		self.confusionMatrix = {'truePositive':0,'falsePositive':0,'falseNegative':0,'trueNegative':0}
		self.partPourcentage = {'truePositive':0,'falsePositive':0,'falseNegative':0,'trueNegative':0}
		self.totalValues = 0

	# Function for normalizing the vector
	def normalize (self, vector, theta=1):
		newVector = []
		for i in vector:
			if i >= theta:
				newVector.append(1)
			else:
				newVector.append(0)
		return newVector

	# Updating the matrix
	def updateConfMatrix(self, predictedVector, realVector):

		normPredVector = self.normalize(predictedVector)
		normRealVector = self.normalize(realVector)

		for i in range(0,len(normPredVector)):
			if normPredVector[i] == 1 and normRealVector[i] == 1:
				self.confusionMatrix['truePositive'] += 1
			elif normPredVector[i] == 1 and normRealVector[i] == 0:
				self.confusionMatrix['falsePositive'] += 1
			elif normPredVector[i] == 0 and normRealVector[i] == 1:
				self.confusionMatrix['falseNegative'] += 1
			elif normPredVector[i] == 0 and normRealVector[i] == 0:
				self.confusionMatrix['trueNegative'] += 1

			self.totalValues += 1.0

		self.updatePourcentage()

	# Updating the pourcetange
	def updatePourcentage(self):
		self.partPourcentage['truePositive'] = round(self.confusionMatrix['truePositive']/self.totalValues*100,3)
		self.partPourcentage['falsePositive'] = round(self.confusionMatrix['falsePositive']/self.totalValues*100,3)
		self.partPourcentage['falseNegative'] = round(self.confusionMatrix['falseNegative']/self.totalValues*100,3)
		self.partPourcentage['trueNegative'] = round(self.confusionMatrix['trueNegative']/self.totalValues*100,3)

	def dumpInfo (self):
		print ('Values for the confusion matrix:')
		for i in self.partPourcentage.iterkeys():
			print '%s : %s %%' %(i,self.partPourcentage[i])
