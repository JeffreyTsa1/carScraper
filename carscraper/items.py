# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    vin = scrapy.Field()
    image = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    dealer = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    drive = scrapy.Field()
    engine = scrapy.Field()
    transmission = scrapy.Field()
    color = scrapy.Field()
    mileage = scrapy.Field()
    body = scrapy.Field()
    url = scrapy.Field()
    fuelType = scrapy.Field()
    fuelEfficiency = scrapy.Field()
    description = scrapy.Field()
