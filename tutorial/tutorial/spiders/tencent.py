# coding=utf-8
import scrapy
from scrapy.selector import Selector

try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle

from tutorial.items import *


class TencentSpider(CrawlSpider):
    name = "tencent"
    allowed_domains = ["tencent.com"]
    start_urls = [
        "http://hr.tencent.com/position.php"
    ]
    rules = [  # 定义爬取URL的规则
        Rule(sle(allow=("/position.php\?&start=\d{,4}#a")), follow=True, callback='parse_item')
    ]

    def parse(self, response):  # 提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据
        sel = Selector(response)
        base_url = get_base_url(response)
        sites_even = sel.css('table.tablelist tr.even')
        for site in sites_even:
            yield self.parsePages(site, base_url)
        sites_odd = sel.css('table.tablelist tr.odd')
        for site in sites_odd:
            yield self.parsePages(site, base_url)

        next_page = sel.css('table.tablelist tr.f #next ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parsePages(self, site, base_url):
        item = TencentItem()
        item['name'] = site.css('.l.square a ::text').extract_first()
        relative_url = site.css('.l.square a').xpath('@href').extract()[0]
        item['detailLink'] = urljoin_rfc(base_url, relative_url)
        item['catalog'] = site.css('tr > td:nth-child(2)::text').extract()
        item['location'] = site.css('tr > td:nth-child(4)::text').extract()
        item['number'] = site.css('tr > td:nth-child(3)::text').extract()
        item['publishTime'] = site.css('tr > td:nth-child(5)::text').extract()

        return scrapy.Request(item['detailLink'], meta={'item': item}, callback=self.parseDetail)

    def parseDetail(self, response):
        sel = Selector(response)
        item = response.meta['item']

        responsibilities = []
        lis = sel.css('table.tablelist tr:nth-child(3) ul li')
        for li in lis:
            responsibilities.append(li.css('::text').extract_first())
        item['responsibilities'] = responsibilities

        requirements = []
        lis = sel.css('table.tablelist tr:nth-child(3) ul li')
        for li in lis:
            requirements.append(li.css('::text').extract_first())
        item['requirements'] = requirements
        return item
