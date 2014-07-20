# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Source(Item):
    name = Field()
    category = Field()
    website = Field()
    description = Field()
    recommendation_group = Field()

class RecommendationGroup(Item):
    name = Field()
    website = Field()
    date = Field()
    description = Field()
    recommendations = Field()

class Restaurant(Item):
    name = Field()
    website = Field()
    address = Field()
