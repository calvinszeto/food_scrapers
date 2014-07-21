from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import log

from category.items import Category
from unidecode import unidecode
import json
import string
import urllib

class CategorySpider(Spider):
    RESTAURANT_INPUT = "/home/puppyplus/Projects/food_scrapers/yelp/category/restaurants.json"
    name = "category"
    allowed_domains = ["yelp.com"]

    def start_requests(self):
        # Retrieve a json list of restaurant IDs, restaurant names, and restaurant cities from an output file generated from the Hibbert console. 
        restaurants = []
        with open(self.RESTAURANT_INPUT, 'r') as f:
            restaurants = json.load(f)            
        requests = []
        for restaurant in restaurants:
            log.msg("Crafting request for: " + restaurant['name'])
            name = urllib.quote_plus(unidecode(restaurant['name']))
            # For each restaurant, run a search on Yelp
            request = Request(
                    "http://www.yelp.com/search?find_desc={name}&find_loc={city}".format(
                        name=name, city=restaurant['city']),
                    callback=self.parse_search)
            request.meta['restaurant'] = restaurant
            requests.append(request)
        log.msg(str(len(requests)) + " total requests queued")
        return requests
    
    def parse_search(self, response):
        sel = Selector(response)
        # Check if there are city options
        cities = sel.xpath("//ul[@class='suggestions-list js-search-exception-links']/li/a/@href").extract()
        if len(cities):
            # Follow the first city suggestion
            yield Request("http://www.yelp.com" + cities[0], callback=self.parse_search)
        else:
            # Grab the first result
            name = sel.xpath('//div[@data-key="1"]//a[@class="biz-name"]/text()|//div[@data-key="1"]//a[@class="biz-name"]/span/text()').extract()
            # Check if the names match by splitting both names into words and comparing the words
            first = unidecode(string.join(name)).split()
            second = unidecode(response.meta['restaurant']['name']).split()
            match = first == second
            if not match:
            # If there is not an EXACT match, print a log message 
            # so I can double check it manually later
                log.msg("First result was {first} when searching for {second} in {city}".format(
                    first=string.join(first, " "), second=string.join(second, " "),
                    city=response.meta['restaurant']['city']), level=log.WARNING)
            # Grab the categories
            categories = sel.xpath('//div[@data-key="1"]//span[@class="category-str-list"]/a/text()').extract()
            if not len(categories):
                log.msg("No categories found for {name} in {city}".format(name=string.join(second, " "), city=response.meta['restaurant']['city']), level=log.WARNING)
            for category in categories:
                yield Category({"name": category, "restaurantId": response.meta['restaurant']['id']})
