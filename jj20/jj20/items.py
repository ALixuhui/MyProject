# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Jj20Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 图片路径
    image_urls = scrapy.Field()
    # 描述
    title = scrapy.Field()
