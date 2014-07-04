# This file contains the tests for the autoregression model
import time
import sys
sys.path.append ('/Users/tomasyany/Projects/tito')
import numpy as np
from predictors.autoregression import autoregression
from predictors.esn import esn

import matplotlib.pyplot as plt

from scipy.stats.stats import pearsonr   


class Printer():
	def __init__(self, data):
		sys.stdout.write("\r\x1b[K"+data.__str__())
		sys.stdout.flush()



print "Loading file"
data = np.loadtxt('data/firstWords.txt',delimiter=',')
mots = -100
data = data[mots:,:]
t = data.shape[1]



a = autoregression(data, 1)
b = esn(100, data, 1, 1)

p = 0
allP = []
allPB = []
time = []
i = 0
pVectorA = []
pVectorB = []
realVector = []

for tF in range (t-100, t-1, 1):

	# tF = tF/100.0

	timeSteps = tF

	# print "Building regression"

	# print "Training regression"
	a.train(timeSteps)

	# print "Building ESN"

	# print "Training ESN"
	b.train(timeSteps)

	real = data[:,timeSteps+1]

	a.predict()
	b.predict()

	pVectorA.append(a.predictedVector[0][55])
	pearson = pearsonr(real, a.predictedVector[0])
	allP.append (pearson[0])

	pVectorB.append(b.predictedVector[55])
	pearsonB = pearsonr(real, b.predictedVector)
	allPB.append (pearsonB[0])

	realVector.append(real[55])

	p = (tF-t+100) * 100
	output = "%d%% of the test completed" % p
	Printer(output)

	time.append(i)
	i+=1


plt.plot(time,pVectorA, 'g',time,pVectorB, 'r-', time, realVector, 'b')
plt.show()

print 'Autoregressoin' 
print allP
moyA = np.mean(allP)
print moyA

print '\nESN'
print allPB
moyB = np.mean(allPB)
print moyB

print 'Done'