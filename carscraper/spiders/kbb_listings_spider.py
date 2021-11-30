# from typing_extensions import ParamSpecArgs
import scrapy
from carscraper.items import CarscraperItem 
import re
import json


class KBBSpider(scrapy.Spider):
    name = "kbb_spider"
    
    # allowed_urls: the main domain of the website you want to scrape
    allowed_domains = ['www.kbb.com']
    
    # start_urls: an attribute listing the URLs the spider will start from
    start_urls = ['https://www.kbb.com/cars-for-sale/used']
    # listings = response.css('div.inventory-listing-body').extract()
    
    # Vanilla Link
    # https://www.kbb.com/cars-for-sale/used
    
    # Link format for results under price: x$ 
    # price can be any integer.
    # https://www.kbb.com/cars-for-sale/used/cars-under-20000
    
    # Link format for results between prices x-and-y: between-x-and-y 
    # https://www.kbb.com/cars-for-sale/used/cars-between-5000-and-10000
        
        
    #parse(): a method of the spider responsible for processing a Response object downloaded from the URL and returning scraped data (as well as more URLs to follow, if necessary)
    
    def parse(self, response):
        # Save page results to a file and open it
        # page = response.url.split('/')[-1]
        # filename = 'cars-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        
        # listings = response.css('div.inventory-listing-body').extract()
        # title = listing.css("h2::text").extract()        
        # listings = response.xpath('//script[@data-cmp="lstgSchema"]').getall()
     
        # Returns listing schema into listings, a list of car listings formatted in json. 
        # "/text()" removes <script> tags 
        # listings = response.xpath('//script[@data-cmp="lstgSchema"]/text()').getall()
        
        #num records gives us the number of listings displayed per page, and firstRecord = x, where x is the number of listings that have already been seen. firstRecord = 0: page 1,firstRecord = 0: page 2
        # https://www.kbb.com/cars-for-sale/used/cars-between-25000-and-30000?dma=&searchRadius=0&priceRange=&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100&firstRecord=200

        
        # yield Request(url=url, callback=self.parse_product_page)
        
        rangeNumbers = ["0", "15000", "20000", "25000", "30000", "35000", "40000", "50000", "9000000"]
        # rangeNumbers = ["0", "50000", "9000000"]
        rangeLen = len(rangeNumbers)
        number_of_pages = 40
        
        # Loops through each price bracket (0-15000, 15000-20000, 20000-25000,..., 50000-9000000)
        for i in range(rangeLen-1):
            # lBound: Lower Bound
            # uBound: Upper Bound
            lBound = str(rangeNumbers[i])
            uBound = str(rangeNumbers[i+1])
            
            for pageNum in range(number_of_pages):
                postsSeen = str(pageNum * 25)
                
                requestUrl = self.start_urls[0] + "/cars-between-" + lBound + "-and-" + uBound + "?dma=&searchRadius=0&priceRange=&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25&firstRecord=" + postsSeen 
                        # https://www.kbb.com/cars-for-sale/used/cars-between-25000-and-30000?dma=&searchRadius=0&priceRange=&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100&firstRecord=200
                print(requestUrl)
                yield scrapy.Request(url=requestUrl, callback=self.parse_listings)
            
        
        
        # for listing in listings:
            # title = listing.css("h2")
            
        # New Method
        

    def parse_listings(self, response):
        listings = response.xpath('//script[@data-cmp="lstgSchema"]/text()').getall()
        listingLen = len(listings)
        # print(listingLen)
        # print(listings)
        
        for listing in listings:
            lDict = json.loads(listing)
            # print(lDict)
            yield {
                "vin": lDict["vehicleIdentificationNumber"],
                "image": lDict["image"],
                "name": lDict["name"],
                "price": lDict["offers"]["price"],
                "dealer": lDict["offers"]["seller"]["name"],
                "make": lDict["brand"]["name"],
                "model": lDict["model"],
                "year": lDict["productionDate"],
                "drive": lDict["driveWheelConfiguration"],
                "engine": lDict["vehicleEngine"],
                "transmission": lDict["vehicleTransmission"],
                "color": lDict["color"],
                "mileage": lDict["mileageFromOdometer"]["value"],
                "body": lDict["bodyType"],
                "url": lDict["url"],
                "fuelType": lDict["fuelType"],
                "fuelEfficiency": lDict["fuelEfficiency"],
                "description": lDict["description"]
            }