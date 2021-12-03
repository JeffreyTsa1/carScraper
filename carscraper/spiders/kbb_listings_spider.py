# from typing_extensions import ParamSpecArgs
import scrapy
from carscraper.items import CarscraperItem 
import re
import json
import datetime

class KBBSpider(scrapy.Spider):
    name = "kbb_spider"
    
    # allowed_urls: the main domain of the website you want to scrape
    allowed_domains = ['www.kbb.com']
    
    # start_urls: an attribute listing the URLs the spider will start from
    start_urls = ['https://www.kbb.com/cars-for-sale/used']
    
    ## Vanilla Link
    # https://www.kbb.com/cars-for-sale/used
    
    ## Link format for results under price: x$ 
    ## price can be any integer.
    # https://www.kbb.com/cars-for-sale/used/cars-under-20000
    # https://www.kbb.com/cars-for-sale/used/cars-under-15000
    
    
    ## Link format for results between prices x-and-y: between-x-and-y 
    # https://www.kbb.com/cars-for-sale/used/cars-between-5000-and-10000
    euroAuto = ['Volkswagen','Mercedes-Benz', 'BMW','Volvo','Aston Martin', 'McLaren','Alfa Romeo','FIAT', 'Audi','MINI','Land Rover','Ferrari','Porsche', 'Bentley', 'Jaguar', 'smart', 'Lamborghini',  'Maserati', 'Rolls-Royce']
    domesticAuto = ['Tesla','Jeep','Dodge','Chevrolet','Saturn','Cadillac','GMC','Buick', 'RAM', 'Pontiac', 'Chrysler', 'Dodge', 'Ford', 'Lincoln']
    japanAuto = ['INFINITI','Mitsubishi','Acura','Toyota','MAZDA','Suzuki', 'Lexus','Nissan', 'Subaru','Scion', 'Honda']
    koreaAuto = ['Genesis', 'Hyundai','Kia']
    id = 0
    
    
    
    #parse(): a method of the spider responsible for processing a Response object downloaded from the URL and returning scraped data (as well as more URLs to follow, if necessary)
    
    def parse(self, response):
        #### Useful code snippets
        
        ## Save page results to a file and open it
        # page = response.url.split('/')[-1]
        # filename = 'cars-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        
        # listings = response.css('div.inventory-listing-body').extract()
        # title = listing.css("h2::text").extract()        
        # listings = response.xpath('//script[@data-cmp="lstgSchema"]').getall()
     
        ## Returns listing schema into listings, a list of car listings formatted in json. 
        # "/text()" removes <script> tags 
        # listings = response.xpath('//script[@data-cmp="lstgSchema"]/text()').getall()
        
        ## num records gives us the number of listings displayed per page, and firstRecord = x, where x is the number of listings that have already been seen. firstRecord = 0: page 1,firstRecord = 0: page 2
        # https://www.kbb.com/cars-for-sale/used/cars-between-25000-and-30000?dma=&searchRadius=0&priceRange=&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100&firstRecord=200

        # yield Request(url=url, callback=self.parse_product_page)
        
        ## Note: From my research, these are the ranges that allow for an even distrubtion. (Cars within 50 miles of Chicago || Cars nationwide)
        ## 0k-15k: 6,741 || 184,485
        ## 15-20k: 6,274 || 171,120
        ## 20k-25k: 6,488 || 178,865 
        ## 25k-30k: 6,504 || 187,883 (Inference: Chicago has a lot less cars in this price bracket vs nationally) This might be another metric in my mathematical equation.
        ## 30k-35k: 5,165 || 152,237
        ## 35k-40k: 4,642 || 146,859 
        ## 40k-50k: 6,012 || 179,370
        ## 50k-9mill: 6,486 || 161,832
    
    
        #### Code start   

        rangeNumbers = ["0", "15000", "20000", "25000", "30000", "35000", "40000", "50000", "9000000"]
        rangeLen = len(rangeNumbers)
        
        ## It's important to note that KBB has quite a few bugs on their end. KBB displays the number of listings found, but you can only ever paginate up to 1000 listings.
        ## If you try to access the next page, KBB will display those listings, but will also remove all buttons for pagination. You are also unable to go back a page. 
        
        ## numPages: Number of pages, numRecords in the link controls the number of listings displayed per page
        ## numPages was 25, and numRecords was 100, but it only ever returned ~700 results * 8 = ~5600 results. This could be something within KBB's backend architecture 
        ## numpages = 40, and numRecords = 25 yields ~9000 results 
        numPages = 40
        
        ## Loops through each price bracket (0-15000, 15000-20000, 20000-25000,..., 50000-9000000)
        for i in range(rangeLen-1):
            ## lBound: Lower Bound
            ## uBound: Upper Bound
            lBound = str(rangeNumbers[i])
            uBound = str(rangeNumbers[i+1])
            
            for pageNum in range(numPages):
                postsSeen = str(pageNum * 25)
                
                requestUrl = self.start_urls[0] + "/cars-between-" + lBound + "-and-" + uBound + "?dma=&searchRadius=0&priceRange=&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25&firstRecord=" + postsSeen 
                        # https://www.kbb.com/cars-for-sale/used/cars-between-25000-and-30000?dma=&searchRadius=0&priceRange=&marketExtension=include&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100&firstRecord=" + postsSeen"
                print(requestUrl)
                yield scrapy.Request(url=requestUrl, callback=self.parse_listings)
            
        

    def parse_listings(self, response):
        listings = response.xpath('//script[@data-cmp="lstgSchema"]/text()').getall()
        listingLen = len(listings)
        # print(listingLen)
        # print(listings)
        for listing in listings:
            lDict = json.loads(listing)
            # print(lDict)]
            self.id += 1
            
            ## These functions attempt to calculate usability, cost, and reliability for each car listing. These will be made crucial features for our vectorizer. 
            ## They aren't implemented currently because I'm still refining my main algorithm to be more efficient. 
            # uScore, uDescription = self.calculateU(lDict)
            # cScore, cDescription = self.calculateC(lDict)
            # rScore, rDescription = self.calculateR(lDict)
            avgScore = 0
            
            vin= lDict["vehicleIdentificationNumber"]
            image= lDict["image"]
            name= lDict["name"]
            price= lDict["offers"]["price"]
            dealer= lDict["offers"]["seller"]["name"]
            make= lDict["brand"]["name"]
            model= lDict["model"]
            year= lDict["productionDate"]
            drive= lDict["driveWheelConfiguration"]
            engine= lDict["vehicleEngine"]
            transmission= lDict["vehicleTransmission"]
            color= lDict["color"]
            mileage= lDict["mileageFromOdometer"]["value"]
            body= lDict["bodyType"]
            url= lDict["url"]
            fuelType= lDict["fuelType"]
            fuelEfficiency= lDict["fuelEfficiency"]
            description= lDict["description"]
            
                
            yield {
                "id": self.id,
                "vin": vin,
                "image": image,
                "name": name,
                "price": price,
                "dealer": dealer,
                "make": make,
                "model": model,
                "year": year,
                "drive": drive,
                "engine": engine,
                "transmission": transmission,
                "color": color,
                "mileage": mileage,
                "body": body,
                "url": url,
                "fuelType": fuelType,
                "fuelEfficiency": fuelEfficiency,
                "description": description
                # "uScore": uScore,
                # "cScore": cScore,
                # "rScore": rScore,
                # "uDescription": uDescription,
                # "cDescription": cDescription,
                # "rDescription": rDescription,
                # "avgScore": avgScore
            }
            
    ## This section is not particularly DRY yet.
    
    ## Calculates Usability Score
    def calculateU(self, lDict):
        uDescriptions = []
        uScore = 0
        engine = lDict["vehicleEngine"]
        
        transmission = lDict["vehicleTransmission"]
        ## Engine has over 8-cylinders
        if engine:
            cylinderCount = engine[0:]
            if cylinderCount > 8:
                uScore += 1

        if engine:
            cylinderCount = engine[0:]
            if cylinderCount > 8:
                uScore += 1
        
        
        return uScore, uDescriptions
        
    ## Calculates Cost Score
    def calculateC(self, lDict):
        cDescriptions = []
        cScore = 0
        make = lDict["make"]
        
        
        # American cars are cheaper to repair, maintain.
        if make in self.domesticAuto:
            cDescriptions.append("American cars are often cheaper") 
            cScore += 1
        mpg = lDict["mileageFromOdometer"]["value"]  
        
        if mpg:
            cityMPG = mpg[:]
            hwyMPG = mpg[:]
            combinedMPG = (cityMPG*0.55) + (hwyMPG*0.45)
        
            if combinedMPG < 20:
                cDescriptions.append("This car is very bad on gas!") 
                cScore -= 2
            elif combinedMPG < 28:
                cScore -= 1
                cDescriptions.append("This car is not great on gas") 
            elif combinedMPG >= 28:
                cScore += 1       
                cDescriptions.append("This car gets great gas mileage") 
        return cScore, cDescriptions

    ## Calculate Reliability Score
    def calculateR(self, lDict):
        rDescriptions = []
        rScore = 0
        
        make = lDict["brand"]["name"]
        currentYear = datetime.now().year
        year = lDict["productionDate"]
        # drive = lDict["driveWheelConfiguration"]
        mileage = lDict["mileageFromOdometer"]["value"]

        
        # European cars have a tendency to be less reliable 
        if make in self.euroAuto:
            rScore -= 1
            
        # Japanese cars have a tendency to be more reliable, except for Nissans lol.
        if make in self.japanAuto:
            rScore += 1
        
        # Korean cars have a tendency to be unreliable.
        if make in self.koreaAuto:
            rScore -= 1
        
    
        carAge = currentYear - year
        
        if (carAge) >= 8:
            # This car is older, and some components might need replacing from old age.
            rScore -= 2   
        elif (carAge) >= 4:
            # This car is starting to get old. It could have some reliability issues.
            rScore -= 1
        elif (carAge) < 2:
            ## This is bad logic, it doesn't cover all ranges of carAge, and flipping the conditional comparator to < is terrible.
            ## But it makes more sense this way. 
            rScore += 1
        return rScore, rDescriptions
    
    