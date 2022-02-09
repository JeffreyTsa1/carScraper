# carScraper
Welcome to my kbb scraper, built with Python3, Scrapy, and a few other imports here and there.

File Structure:
'kbb_listings_spider.py' contains all of the main code for scraping
'pipelines.py' contains functionality for what happens to the scraped values. The block of code commented out above connects to a postgresql database, and the block of code below exports the data to a .csv file in the parent directory

Make sure you install all the required dependencies before you run. You can also deploy this project directly to Heroku as a background dyno.

To run, navigate to this "parent" repository in your terminal and then run the commands in the quotation marks below:
"scrapy crawl run kbb_spider"

To run this on Heroku:
"heroku run scrapy crawl kbb_spider"