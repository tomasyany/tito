# This file generates fake data set for later testing

# import numpy as np
# import math
import random as random

wordMatrix = open ('../../data/fakeWordDate.txt','w')
dateRange = 5000


line = ''
maxAmount = 30
amount = 0

# # Uniform
# for i in range(0, dateRange):
# 	amount = random.randint(int(-maxAmount/2),int(maxAmount/2))
# 	if amount < 0:
# 		amount = 0
# 	# else:
# 	# 	amount = 1
# 	if i == dateRange-1:
# 		line = line + str(amount)
# 	else:
# 		line = line + str(amount)+ ','

# wordMatrix.write(line)
# wordMatrix.write('\n')
# line = ''

# 1 equiDistribute over time
for i in range(0, dateRange):
	amount = 0
	if i%20==0:
		amount = 1
	if i == dateRange-1:
		line = line + str(amount)
	else:
		line = line + str(amount)+ ','

wordMatrix.write(line)
wordMatrix.write('\n')
line = ''

# 1 equiDistribute over time
for i in range(0, dateRange):
	amount = 0
	if i%20==0:
		amount = 1
	if i == dateRange-1:
		line = line + str(amount)
	else:
		line = line + str(amount)+ ','

wordMatrix.write(line)
wordMatrix.write('\n')
line = ''

# # Gaussian distribution
# for i in range(0, dateRange):
# 	amount = int(random.gauss(0,maxAmount/4))
# 	if amount < 0:
# 		amount = 0
# 	if i == dateRange-1:
# 		line = line + str(amount)
# 	else:
# 		line = line + str(amount)+ ','

# wordMatrix.write(line)
# wordMatrix.write('\n')
# line = ''

# # Only zeros
# for i in range(0, dateRange):
# 	amount = 0
# 	if i == dateRange-1:
# 		line = line + str(amount)
# 	else:
# 		line = line + str(amount)+ ','

# wordMatrix.write(line)
# wordMatrix.write('\n')
# line = ''

# # Only ones
# for i in range(0, dateRange):
# 	amount = 1
# 	if i == dateRange-1:
# 		line = line + str(amount)
# 	else:
# 		line = line + str(amount)+ ','

# wordMatrix.write(line)
# wordMatrix.write('\n')
# line = ''

wordMatrix.close()
