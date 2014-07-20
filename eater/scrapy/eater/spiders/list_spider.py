from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from urlparse import urlparse
import re
import string
from dateutil import parser
import strip_tags

from eater.items import Restaurant, Source, RecommendationGroup

class ListSpider(Spider):
    name = "list"
    allowed_domains = ["*.eater.com", "localhost"]
    start_urls = [
        "http://www.eater.com"
    ]

    def parse(self, response):
        """Starting from Eater homepage, construct Splash URLs for each link in the 'Where to Eat' section"""
        sel = Selector(response)
        links = sel.xpath('//div[@class="module where-to-eat"]/ul/li/a/@href').extract()
        for link in links:
            request = Request("http://localhost:8050/render.html?url={link}&timeout=30&wait=2".format(link = link), callback=self.parse_list)
            request.meta['full_url'] = link
            url = urlparse(link) 
            request.meta['base_url'] = "http://" + url.netloc
            yield request

    def parse_list(self, response):
        """Construct Items for an Eater list"""
        sel = Selector(response)

        # Source
        # Name comes from the "City" field
        # Category is Blog
        # Website is the root URL
        # Description is the same - the paragraph from http://curbednetwork.com/titles/eater
        source = Source()
        source['name'] = "Eater " + sel.xpath('//div[@id="locale-nav"]/ul/li[@class="selected visible-top"]/a/text()').extract()[0]
        source['category'] = "Blog"
        source['website'] = response.meta['base_url']
        source['description'] = "Eater is the source for people who care about dining and drinking in the nation's most important food cities. A favorite of industry pros and amateurs alike, Eater has an uncanny knack for finding out what's opening where, who's serving what, and how it's all going down. Since its launch in New York in 2005, Eater has opened its doors in 16 more cities around the country. And Eater National brings Eater's signature coverage to parts far and wide, with beefed-up reporting on celebrity chefs, reality TV, and national dining trends."

        # RecommendationGroup
        # Name is the header of the page
        # Website is the current URL (without any params)
        # Date is right under the title
        # Description is the first two paragraphs
        group = RecommendationGroup()
        group['name'] = sel.xpath('//h1[@class="post-title"]/a/text()').extract()[0]
        group['website'] = response.meta['full_url']
        date_str = re.compile(r"\s+(.+),\sby.*$").match(sel.xpath('//div[@class="post-byline"]/text()').extract()[0]).group(1)
        group['date'] = parser.parse(date_str)
        group['description'] = string.join(sel.xpath('//div[@class="post-body"]/p/text()|//div[@class="post-body"]//strong/text()').extract())
        group['recommendations'] = []

        # Restaurant
        # Name is the title of each row
        # Website is in a link in the row, if applicable
        # Address is in the right side of the row
        restaurants = sel.xpath('//div[@class="point-mode point-mode-list"]/div/div')
        for restaurant in restaurants:
            item = Restaurant()
            name = restaurant.xpath('div[@class="name fn org overflow-controlled"]/@title').extract()
            address = restaurant.xpath('div[@class="metadata"]/div[@class="address adr overflow-controlled"]/text()').extract()
            website = restaurant.xpath('div[@class="metadata"]/div[@class="url overflow-controlled"]/a/@href').extract()
            item['name'] = name[0] if name else ""
            item['address'] = address[0] if address else ""
            item['website'] = website[0] if website else ""
            group['recommendations'].append(item)

        source['recommendation_group'] = group
        yield source
