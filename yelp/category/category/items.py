from scrapy.item import Item, Field

class Category(Item):
    name = Field()
    restaurantId = Field()
