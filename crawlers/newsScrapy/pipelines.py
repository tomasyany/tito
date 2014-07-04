# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.

import operator

class NewsPipeline(object):

    # When spider starts
    def open_spider(self,spider):
        self.bigPipe = FileWriter()

    # Method for each item received from the loader
    def process_item(self, item, spider):

        errorCodes = [403,404,500]

        if (not 'body' in item):
            errorF = open('../logs/errorsSelecting.txt','a')
            errorF.write('The '+item['date'][0]+' web didn\'t return anything')
            errorF.write('\n')
            errorF.close()
        else:    
            date = item['date'][0]
            status = item['status'][0]

            if status in errorCodes:
                self.bigPipe.updateErrorDates(date)
            else:
                for word in item['body']:
                    self.bigPipe.updateMatrix(word,date)

        return item

    # When spider closes
    def close_spider(self,spider):
        self.bigPipe.dumpMatrix('../../data/wordDate.txt', '../../data/wordIndex.txt', '../../data/dateIndex.txt', '../../data/errorDates.txt')

class FileWriter(object):

    # Constructor with variables initialization
    def __init__(self):
        self.wordMatrix = {}
        self.wordAmount = {}
        self.currentDate = ''
        self.dates = []
        self.errorDates = []
        

    # Updating the cumulated word/date dictionnary
    def updateMatrix(self, word, date):
        # Updating the matrix for each new (word,date) tuple
        if((word,date) in self.wordMatrix):
            self.wordMatrix[word,date] += 1
        else:
            self.wordMatrix[word,date] = 1

        # Updating the total final times a word appears
        if word in self.wordAmount:
            self.wordAmount[word] += 1
        else:
            self.wordAmount[word] = 1

        # Updating the dates list
        self.updateDate(date)

    # Sorting the wordAmount list by amount
    def sortWordAmount(self, rv=True):
        self.wordAmount = sorted(self.wordAmount.iteritems(), key=operator.itemgetter(1), reverse=rv)

    # Writing the matrix into a file
    def dumpMatrix (self,fileName, indexWord, indexDate, error):
        wordDate = open(fileName, 'w')
        dateIndex = open(indexDate, 'w')
        wordIndex = open(indexWord, 'w')
        errorUrlsFile = open(error,'w')

        self.sortDates()
        self.sortWordAmount()
        i=0
        j=0
        dateBool = True
        firstColumn = True
        for t in self.wordAmount:
            word = t[0]

            wordIndex.write(str(j)+','+word)
            wordIndex.write('\n')
            j+=1

            line = ''

            for date in self.dates:
                date = '/'.join(date)

                if not (word,date) in self.wordMatrix:
                    self.wordMatrix[word,date] = 0

                if firstColumn:
                    line = line + str(self.wordMatrix[word,date])
                    firstColumn = False
                else:
                    line = line + ',' + str(self.wordMatrix[word,date])

                if dateBool:
                    dateIndex.write(str(i)+','+date)
                    dateIndex.write('\n')
                    i+=1

            dateBool = False
            firstColumn = True
            wordDate.write(line)
            wordDate.write('\n')

        # Writing down the dates which gave errors
        for errorD in self.errorDates:
            errorD = '/'.join(errorD)
            errorUrlsFile.write(errorD)
            errorUrlsFile.write('\n')

        # Closing all the files
        wordDate.close()
        dateIndex.close()
        wordIndex.close()
        errorUrlsFile.close()

    # Updating the dates set
    def updateDate (self, date):
        if not self.currentDate == date:
            self.dates.append(date.split('/'))
            self.currentDate = date

    # Sorting the dates set chronologically
    def sortDates (self):
        self.dates = sorted(self.dates, key=operator.itemgetter(2,1,0))
        self.errorDates = sorted(self.errorDates, key=operator.itemgetter(2,1,0))

    # Updating the list of urls having errors
    def updateErrorDates (self, date):
        self.errorDates.append(date.split('/'))
