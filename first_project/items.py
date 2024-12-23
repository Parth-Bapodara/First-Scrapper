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
    views = scrapy.Field()
    votes = scrapy.Field()
    total_answers = scrapy.Field()
    asked_by = scrapy.Field()
    details = scrapy.Field()
    # answered_by = scrapy.Field()
    # answered_by_other = scrapy.Field()
    # accepted_answer = scrapy.Field()
    # other_answers = scrapy.Field()
    is_accepted = scrapy.Field()
    answer = scrapy.Field()
    