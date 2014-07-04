# Item loader

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose
from w3lib.html import replace_escape_chars, remove_tags
from nltk.corpus import stopwords
import string
import re

from items import NewsItem

class NewsLoader (ItemLoader):

	def filterStopWords(x):
		return None if x in stopwords.words('english') or x=='' else x

	def filterSymbols(x):
		if (re.sub(r'[\W_]+', u'',x)==x):
			return x
		else:
			return None

	def arrangeDateOrder (self,x):
		dateList = x[0].split('/')
		date = dateList[2]+'/'+dateList[1]+'/'+dateList[0]
		return date
	    
	default_item_class = NewsItem

	body_in = MapCompose(lambda v: v.lower().strip(string.punctuation).strip().split(), filterStopWords, filterSymbols, replace_escape_chars, remove_tags)

	date_in = arrangeDateOrder
