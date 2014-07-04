# Item model

from scrapy.item import Item, Field

class NewsItem(Item):

	# Item fields
    body = Field()
    date = Field()
    status = Field()

