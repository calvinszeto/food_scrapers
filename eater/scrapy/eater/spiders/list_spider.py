from scrapy.spider import Spider
from scrapy.selector import Selector

from eater.items import RestaurantItem

class ListSpider(Spider):
    name = "list"
    allowed_domains = ["eater.com"]
    start_urls = [
        # Houston
        "http://localhost:8050/render.html?url=http://houston.eater.com/archives/2014/01/07/the-essential-38-houston-restaurants-january-2014-1.php&timeout=5&wait=1",
        "http://localhost:8050/render.html?url=http://houston.eater.com/archives/2014/04/08/the-essential-38-houston-restaurants-april-2014.php&timeout=5&wait=1",
        # New York
        "http://localhost:8050/render.html?url=http://ny.eater.com/archives/2014/01/the_38_essential_new_york_restaurants_january_14.php&timeout=5&wait=1",
        "http://localhost:8050/render.html?url=http://ny.eater.com/archives/2014/04/the_38_essential_new_york_restaurants_april_14.php&timeout=5&wait=1",
        # Austin
        "http://localhost:8050/render.html?url=http://austin.eater.com/archives/2014/01/07/the-38-essential-austin-restaurants-january-14.php&timeout=5&wait=1",
        "http://localhost:8050/render.html?url=http://austin.eater.com/archives/2014/04/08/the-38-essential-austin-restaurants-april-14.php&timeout=5&wait=1",
    ]

    def parse(self, response):
        sel = Selector(response)
        restaurants = sel.xpath('//div[@class="point-mode point-mode-list"]/div/div')
        for restaurant in restaurants:
            item = RestaurantItem()
            name = restaurant.xpath('div[@class="name fn org overflow-controlled"]/@title').extract()
            address = restaurant.xpath('div[@class="metadata"]/div[@class="address adr overflow-controlled"]/text()').extract()
            website = restaurant.xpath('div[@class="metadata"]/div[@class="url overflow-controlled"]/a/@href').extract()
            item['name'] = name[0] if name else ""
            item['address'] = address[0] if address else ""
            item['website'] = website[0] if website else ""
            yield item
