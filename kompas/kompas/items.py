# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KompasItem(scrapy.Item):
    # define the fields for your item here like:
    tag = scrapy.Field()
    content = scrapy.Field() 
    date = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    source = scrapy.Field()
    img_link = scrapy.Field()