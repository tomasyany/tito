# Abstract Crawler

class abstractCrawler:

	# Not implemented methods
	def connect(self):
		raise NotImplementedError ('Method must be implemented in ' +self.__class__.__name__ + ' class')

	def disconnect(self):
		raise NotImplementedError ('Method must be implemented in ' +self.__class__.__name__ + ' class')
	        
	def crawl(self):
		raise NotImplementedError ('Method must be implemented in ' +self.__class__.__name__ + ' class')
