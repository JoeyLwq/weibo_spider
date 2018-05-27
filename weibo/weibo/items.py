# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    sex = scrapy.Field()
    location = scrapy.Field()
    id = scrapy.Field()
    certification = scrapy.Field()
    follows = scrapy.Field()
    articles = scrapy.Field()
    fans = scrapy.Field()
    brief = scrapy.Field()

