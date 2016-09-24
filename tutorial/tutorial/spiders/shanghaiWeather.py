# coding=utf8

import scrapy
from scrapy.selector import Selector

from tutorial.items import *


class ShanghaiTianqi(scrapy.Spider):
    name = 'shanghai'
    start_urls = ['http://shanghai.tianqi.com/20160918.html']

    def parse(self, response):
        sel = Selector(response)

        weather = Weather()
        weather['city'] = '上海'
        wdiv = response.css('#tool_site')
        weather['date'] = wdiv.css('#today ul .time::text').extract_first()
        weather['temperature1'] = wdiv.css('#t_temp font:nth-child(1)::text').extract_first()
        weather['temperature2'] = wdiv.css('#t_temp font:nth-child(2)::text').extract_first()
        weather['summary'] = wdiv.css('#today ul li:nth-child(4)::text').extract_first()
        weather['wind'] = wdiv.css('#today ul li:nth-child(5)::text').extract_first()

        weather['day'] = wdiv.css('.tqshow_ls:nth-child(1) li:nth-child(2)::text').extract_first()
        weather['night'] = wdiv.css('.tqshow_ls:nth-child(2) li:nth-child(2)::text').extract_first()

        div = response.css('#main')
        weather['ziwai'] = div.css('.history_sh>div:nth-child(1) dt span::text').extract_first()
        weather['ziwaiD'] = div.css('.history_sh>div:nth-child(1) dd::text').extract_first()
        weather['chuanyi'] = div.css('.history_sh>div:nth-child(2) dt span::text').extract_first()
        weather['chuanyiD'] = div.css('.history_sh>div:nth-child(2) dd::text').extract_first()
        weather['lvyou'] = div.css('.history_sh>div:nth-child(3) dt span::text').extract_first()
        weather['lvyouD'] = div.css('.history_sh>div:nth-child(3) dd::text').extract_first()
        weather['shushi'] = div.css('.history_sh>div:nth-child(4) dt span::text').extract_first()
        weather['shushiD'] = div.css('.history_sh>div:nth-child(4) dd::text').extract_first()
        weather['chenlian'] = div.css('.history_sh>div:nth-child(5) dt span::text').extract_first()
        weather['chenlianD'] = div.css('.history_sh>div:nth-child(5) dd::text').extract_first()
        weather['xiche'] = div.css('.history_sh>div:nth-child(6) dt span::text').extract_first()
        weather['xicheD'] = div.css('.history_sh>div:nth-child(6) dd::text').extract_first()
        weather['liangshai'] = div.css('.history_sh>div:nth-child(7) dt span::text').extract_first()
        weather['liangshaiD'] = div.css('.history_sh>div:nth-child(7) dd::text').extract_first()
        weather['guomin'] = div.css('.history_sh>div:nth-child(8) dt span::text').extract_first()
        weather['guominD'] = div.css('.history_sh>div:nth-child(8) dd::text').extract_first()
        yield weather

        prev_page = wdiv.css('.tqxiangqing a:nth-child(1)::attr(href)').extract_first()
        text = wdiv.css('.tqxiangqing a:nth-child(1)::text').extract_first()
        if prev_page and text == u'上一天':
            yield scrapy.Request(prev_page, callback=self.parse)
