# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst



class Project1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Scrap_item(scrapy.Item):
    company_name = scrapy.Field(output_processor=TakeFirst())
    city = scrapy.Field(output_processor=TakeFirst())
    state = scrapy.Field(output_processor=TakeFirst())
    zip_code = scrapy.Field(output_processor=TakeFirst())
    phone_number = scrapy.Field(output_processor=TakeFirst())
    website = scrapy.Field(output_processor=TakeFirst())