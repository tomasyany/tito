# Scrapy settings for newsScrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'newsScrapy'

SPIDER_MODULES = ['newsScrapy.spiders']
NEWSPIDER_MODULE = 'newsScrapy.spiders'

ITEM_PIPELINES = {'newsScrapy.pipelines.NewsPipeline' : 1}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'newsScrapy (+http://www.yourdomain.com)'
