# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DjinniScrapyItem(scrapy.Item):
    tags = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    views = scrapy.Field()
    applications = scrapy.Field()
    experience = scrapy.Field()

