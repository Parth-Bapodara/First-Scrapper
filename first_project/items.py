# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import scrapy.interfaces
import scrapy.item

class FirstProjectItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    tags = scrapy.Field()
    asked_by = scrapy.Field()
    answered_by = scrapy.Field()
    answered_by_other = scrapy.Field()
    accepted_answer = scrapy.Field()
    other_answers = scrapy.Field()

class AnsweredByInfo(scrapy.Item):
    name = scrapy.Field()
    answeredago = scrapy.Field()
    answeredtime = scrapy.Field()
    reputation = scrapy.Field()
    gold = scrapy.Field()
    silver = scrapy.Field()
    bronze = scrapy.Field()
    