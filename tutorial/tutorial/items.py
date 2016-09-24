# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class TencentItem(Item):
    name = Field()
    catalog = Field()
    location = Field()
    number = Field()
    detailLink = Field()
    publishTime = Field()
    responsibilities = Field()
    requirements = Field()


class Weather(Item):
    city = Field()
    date = Field()
    temperature1 = Field()
    temperature2 = Field()
    summary = Field()
    wind = Field()
    day = Field()
    night = Field()
    ziwai = Field()
    ziwaiD = Field()
    chuanyi = Field()
    chuanyiD = Field()
    lvyou = Field()
    lvyouD = Field()
    shushi = Field()
    shushiD = Field()
    chenlian = Field()
    chenlianD = Field()
    xiche = Field()
    xicheD = Field()
    liangshai = Field()
    liangshaiD = Field()
    guomin = Field()
    guominD = Field()
