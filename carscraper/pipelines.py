# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#Added 
import psycopg2
import os
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
#Added End


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CarscraperPipeline:
    def process_item(self, item, spider):
        if not all(item.values()):
            raise DropItem("Missing values!")
        else:
            return item

class KbbPipeline(object):
    def open_spider(self, spider):
        hostname = 'ec2-18-213-133-45.compute-1.amazonaws.com'
        username = 'ziqvmhxhcnuase' # your username
        password = '90c460cf3812eef43dfe2b49c221061575bc154f69177f0530fa9ab69a8dc371' # your password
        database = 'd8gf6jesquhuaj'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()
        # self.cur.execute("CREATE TABLE cars(vin VARCHAR, image VARCHAR, name VARCHAR, price INT, dealer VARCHAR
        # , make VARCHAR, model VARCHAR, year INT, drive VARCHAR, engine VARCHAR, transmission VARCHAR, 
        # color VARCHAR, mileage VARCHAR, body VARCHAR, url VARCHAR, fuelType VARCHAR, fuelEfficiency VARCHAR, 
        # description VARCHAR)")
        # self.cur.execute("CREATE TABLE cars(vin, image, name, price, dealer, make, model, year, drive, engine, transmission, color, mileage, body, url, fuelType, fuelEfficiency, description)")

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close() 

    def process_item(self, item, spider):
        vin = item["vin"]
        image = item["image"]
        name = item["name"]
        price = item["price"]
        dealer = item["dealer"]
        make = item["make"]
        model = item["model"]
        year = item["year"]
        drive = item["drive"]
        engine = item["engine"]
        transmission = item["transmission"]
        color = item["color"]
        mileage = item["mileage"]
        body = item["body"][0]
        url = item["url"]
        fuelType = item["fuelType"]
        fuelEfficiency = item["fuelEfficiency"]
        description = item["description"]
        sql = "INSERT INTO cars (vin, image, name, price, dealer, make, model, year, drive, engine, transmission, color, mileage, body, url, fuelType, fuelEfficiency, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (vin, image, name, price, dealer, make, model, year, drive, engine, transmission, color, mileage, body, url, fuelType, fuelEfficiency, description)
        self.cur.execute(sql, val)
        # self.cur.execute("INSERT INTO cars (item['vin'], item['image'], item['name'], item['price'], item['dealer'], item['make'], item['model'], item['year'], item['drive'], item['engine'], item['transmission'], item['color'], item['mileage'], item['body'], item['url'], item['fuelType'], item['fuelEfficiency'], item['description']) VALUES (%s, %s, %s, %d, %s, %s, %s, %d, %s, %s, %s, %s, %s, %s, %s, %s)")
        self.connection.commit()
        return item




    # def __init__(self):
    #     self.filename = 'kbbData.csv'
    # def open_spider(self, spider):
    #     self.csvfile = open(self.filename, 'wb')
    #     self.exporter = CsvItemExporter(self.csvfile)
    #     self.exporter.start_exporting()
    # def close_spider(self, spider):
    #     self.exporter.finish_exporting()
    #     self.csvfile.close()
    # def process_item(self, item, spider):
    #     self.exporter.export_item(item)
    #     return item