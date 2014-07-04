# Twitter crawler

# Libraries import
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import threading
import time

from abstractCrawler import abstractCrawler

class twitterCrawler (abstractCrawler):

	# tomasyany API keys
	ck = 'gYbjJnVSnEWmR1hIV6EImA'
	cs = 'd1O6FSvpklfBseZQAcRY3Ev0OQnC0NMdaNXio6gppA'
	at = '362186874-SFfDliJejG7DlQGuJ7QVpEhyH3BS242joBYhYKpe'
	ats = '0OPLM2ydTg27l9UVw2YDHDSjLyuG5PXorj25Y0K4l9NUz'

	def __init__(self, lang='en', consumer_key=ck,consumer_secret=cs,access_token=at,access_token_secret=ats, duration=10, stepTime=2):
		
		self.lang = lang
		self.duration = duration
		self.stepTime = stepTime
		self.stopCounter = threading.Event()

		# API keys to do requests on Twitter
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.access_token = access_token
		self.access_token_secret = access_token_secret

		# Variables initialization
		self.wordCounter = 0
		f = open("crawlers/lang/"+self.lang, 'r') # Reading the important words from file
		self.words = f.read().split()
		self.wordsCount = {}
		for i in self.words:
			self.wordsCount[i] = 0

	# Time counter
	def print_time(self, step, stop_event):
		while (not stop_event.isSet()):
			time.sleep(step)
			print "%s: %s" % ("Clock", time.ctime(time.time()))

	# Connecting to stream
	def connect(self):
		# Authentification
		auth = OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token (self.access_token, self.access_token_secret)

		# Connecting to the stream
		self.twitterStream = Stream (auth, twitterListener())

		return True

	# Disconnecting to stream
	def disconnect(self):
		self.twitterStream.disconnect()	
		print ("Disconnected succesfully")

	# Crawling function
	def crawl(self):

		self.connect()

		try:
			# Threads for time and stream listening
			timeThread = threading.Thread(target=self.print_time, args=(self.stepTime, self.stopCounter))		
			streamThread = threading.Thread(target=self.twitterStream.filter, kwargs={'track': self.words})
			timeThread.start()
			streamThread.start()
			pass
		except:
			print("Error in threads start")

		# Execution during duration	
		time.sleep(self.duration)
		self.stopCounter.set()
		self.disconnect()

		

# Listening to stream, overriden some methods from StreamListener
class twitterListener(StreamListener):

	def __init__(self):
		self.counter=0

	def on_connect (self):
		print ("Connection established")

	def on_data (self, data):		
		# tweet = data.split(',"text":"')[1].split('","source')[0]
		self.counter = self.counter + 1
		print self.counter
		return True

	def on_error(self, status):
		print status

if __name__ == "__main__":
	crawler = twitterCrawler()
	crawler.crawl()

	





