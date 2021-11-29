# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    car = scrapy.Field()
    mileage = scrapy.Field()
    price = scrapy.Field()
    color = scrapy.Field()
    transmission = scrapy.Field()
    engine = scrapy.Field()
    doors = scrapy.Field()
    body = scrapy.Field()
    mpg = scrapy.Field()
    kbb_expert_review = scrapy.Field()
    consumer_review = scrapy.Field()
    location = scrapy.Field()
    website = scrapy.Field()
