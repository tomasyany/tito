import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append ('/Users/tomasyany/Projects/tito')

from analyzers.plotter import plotter


modelsNames = ['ESN', 'Autoregression', 'Random', 'Constant']
errorsNames = ['MSE','RMSE','Blabla']
time = [0,20,50]
realValues = np.random.randn(5,len(time))
predictedValues = []
for i in range (0,4):
	predictedValues.append(np.random.randn(5,len(time)))

errors = []
for i in range(0,4):
	errors.append(np.random.randn(3,len(time)))


	
myPlotter = plotter(time, realValues, predictedValues ,modelsNames, errors, errorsNames)

myPlotter.plotRealPred()
myPlotter.plotRealPredTime(2)

myPlotter.plotErrorTime()

myPlotter.generatePlot()