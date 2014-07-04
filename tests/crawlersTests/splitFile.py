import sys
sys.path.append ('/Users/tomasyany/Projects/tito')

fileName = 'data/dateIndex.txt'
# fileName = 'testsResults/testData.txt'
f = open (fileName,'r')

i=0
j=1

a =(open('words'+str(j)+'.txt','w'))
for line in f.readlines():

	a.write(line)

	if(not i ==0 and i%500==0):
		j+=1
		a.close()
		# a = open('testsResultswords'+str(j)+'.txt','w')
	i+=1