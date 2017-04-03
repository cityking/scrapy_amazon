# -*- coding: utf-8 -*-
import scrapy
from scrapy_amazon.items import ProductItem
from scrapy.http import Request


class CategorySpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["amazon.cn"]
    url = 'https://www.amazon.cn/s/ref=sd_allcat_digita_l3_siphone/455-0954308-9828468?ie=UTF8&page=1&rh=n%3A665002051%2Cp_89%3AApple%2Cn%3A664978051'
    start_urls =[url,] 

    def parse(self, response):
        pro_list = response.xpath('//*[@id="s-results-list-atf"]')
        lis = pro_list.xpath('li')
        if lis:
            for li in lis:
                pro_item = ProductItem()
                pro_item['title'] = li.xpath('div/div[2]/div[1]/a/@title')[0].extract()
                pro_item['price'] = li.xpath('div/div[3]/div[1]/a/span[2]/text()').extract()[0]
                link = li.xpath('div/div[2]/div[1]/a/@href')[0].extract()
                yield Request(link, meta={'item': pro_item}, callback=self.detailparse) 

    def detailparse(self, response):
        item = response.meta['item']
        tbody = response.xpath('//*[@id="prodDetails"]/div[2]/div[1]/div/div[2]/div/div/table/tbody')
        if tbody.xpath('tr[4]/td[1]/text()').extract()[0]=='产品颜色':
            item['color'] = tbody.xpath('tr[4]/td[2]/text()')[0].extract()
        else:
            item['color'] = tbody.xpath('tr[5]/td[2]/text()')[0].extract()
        item['img_url'] = [response.xpath('//*[@id="landingImage"]/@src')[0].extract(),]
        return item
