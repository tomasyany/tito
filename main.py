#import sys
# # sys.path.append ('/Users/tomasyany/Projects/tito')
# # from tests.predictorsTests.esnTests import esnTest

# # test = esnTest()

# # answer = True
# # while answer == True:
# # 	testNumber = input("Which test do you want to run? ")
# # 	print 'Running test number '+str(testNumber)
# # 	if testNumber == 1:
# # 		test.test1()
# # 	elif testNumber == 2:
# # 		test.test2()
# # 	elif testNumber == 3:
# # 		test.test3()
# # 	else:
# # 		test.test4()

# # 	print '\nDone'
# # 	print '----------------------------------------------'

# # 	boo = input("Do you want to run another test?(1/0) ")
# # 	print('\n')
# # 	if boo == 0:
# # 		answer = False

# import pandas as pd
# import numpy as np
# from datetime import datetime

# namesFile = open('data/nasdaq/wordIndex.txt','r')
# names = []
# for line in namesFile.readlines() :
# 	names.append(line.split(',')[1].strip())
# namesFile.close()

# start_date = '06/12/2004'
# end_date = '06/12/2014'
# date_formatter1 = '%Y-%m-%d'
# # date_formatter2 = '%d/%m/%Y'
# # rng = pd.bdate_range(start_date, end_date)


# rng = [d.date().isoformat() for d in pd.bdate_range(start_date, end_date)]
# datesLength = len(rng)

# # dateIndexFile = open('data/nasdaq/dateIndex.txt', 'w')

# # i = 0 
# # for date in rng:
# # 	d = datetime.strptime(date, date_formatter1)
# # 	d = d.strftime(date_formatter2)

# # 	line = str(i) + ','+d+'\n'

# # 	dateIndexFile.write(line)

# # 	i += 1

# # dateIndexFile.close()

# companies = []
# for companyName in names:
# 	company = pd.read_csv('data/nasdaq/companies/'+companyName+'.csv', index_col=0, parse_dates=True)
# 	company = company[1:]['close']
# 	companies.append(company)

# companiesLength = len(companies)

# wordDateFile = open('data/nasdaq/wordDate.txt', 'w')
# for companyID in range(0,companiesLength):
# 	line = ''
# 	for dateID in range (0, datesLength):
# 		d = datetime.strptime(rng[dateID], date_formatter1)

# 		if d in companies[companyID]:
# 			value = companies[companyID][d]
# 		else:
# 			value = np.mean(companies[companyID][-dateID:])
# 			companies[companyID].loc[d] = value

# 		if dateID == 0:
# 			line = str(value)
# 		else:
# 			line = line + ',' + str(value)

# 	wordDateFile.write(line)
# 	wordDateFile.write('\n')

# wordDateFile.close()

# import matplotlib.pyplot as plt
# import numpy as np


 = np.linspace(-3,3)
x= plt.subplot(1,1,1)
x.set_ylim((-1.5,1.5))
x.plot(x,np.tanh(x))
x.spines['left'].set_position('center')
x.spines['bottom'].set_position('center')
x.spines['right'].set_color('none')
x.spines['top'].set_color('none')
x.annotate('tanh(x)', xy=(2, 0.7), xytext=(2.05, 1.1))      

lt.grid()
lt.show()

