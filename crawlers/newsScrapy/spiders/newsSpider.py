from scrapy.spider import Spider
from scrapy.selector import Selector

from newsScrapy.loader import NewsLoader


class newsSpider(Spider):

    handle_httpstatus_list = [403,404,500]

    name = "newsSpider"
    start_urls = []

    global prefix
    prefix = "http://www.nytimes.com/indexes/"
    sufix = "/todayspaper/index.html"
    for year in range (2001,2015):
        for month in range (1,13):
            if month in [4,6,9,11]:
                totalDays = 30
            elif month == 2:
                totalDays = 28
            else:
                totalDays = 31
            for day in range (1,totalDays+1):
                if(month<10 and day<10):
                    start_urls.append (prefix+str(year)+"/"+"0"+str(month)+"/"+"0"+str(day)+'/')
                elif (month<10 and day>9):
                    start_urls.append (prefix+str(year)+"/"+"0"+str(month)+"/"+str(day)+'/')
                elif (month>9 and day<10):
                    start_urls.append (prefix+str(year)+"/"+str(month)+"/"+"0"+str(day)+'/')
                else:
                    start_urls.append (prefix+str(year)+"/"+str(month)+"/"+str(day)+'/')

    # start_urls = [prefix + '2010/01/01']

    def parse(self, response):

        sel = Selector(response)

        news = NewsLoader (response=response)

        news.add_xpath('body', '//body//text()')
        news.add_value('date', response.url.strip(prefix))
        news.add_value('status', response.status)

        return news.load_item()
