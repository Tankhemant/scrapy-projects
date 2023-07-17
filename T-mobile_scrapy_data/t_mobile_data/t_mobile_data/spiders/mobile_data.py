import json
import scrapy
import random
import time

from ..items import TMobileDataItem
items=TMobileDataItem()
class MobileDataSpider(scrapy.Spider):
#self.payload = "{\r\n    \"visitorId\": \"bac0dde8-7ff4-47b0-9da0-a55a2c4c6d40\",\r\n    \"firstResult\": 12,\r\n    \"q\": \""+self.keyword+"\",\r\n    \"disableCaching\": true\r\n}"

    name = "mobile_data"
    count_number=0
    number=1

    def start_requests(self):
        url = 'https://www.t-mobile.com/self-service-flex/v1/search/all/relevant'

        payload="{\r\n \"firstResult\":0,\r\n \"q\":\"iphone\",\r\n \"visitorId\":\"4233696f-e26d-43a4-9b88-7b6ef9f76139\",\r\n \"disableCaching\":\"True\"}"
        yield scrapy.Request(url,
                             method='POST',
                             body=payload,
                             meta={"url": url, "payload": json.loads(self.payload)},
                             callback=self.parse
                             )
    def parse(self, response):
        try:
            data_json = response.json()
            get_data_json = data_json['results']
        except:
            print("json~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        for singel_listing in get_data_json:
            try:
                items['title'] = singel_listing['title']
            except:
                items['title']=None
            try:
                items['imgpath'] = singel_listing['thumbnail']
            except:
                items['imgpath']=None
            try:
                items['salesprice'] = singel_listing['saleprice']
            except:
                items['salesprice']=None

            print(self.number)
            self.number += 1
            

            yield items
            
       
        if response.meta['payload']["firstResult"]<=1600:
            response.meta['payload']["firstResult"]+=12
            url = response.meta["url"]
            yield scrapy.Request(url,
                             method='POST',
                             body=json.dumps(response.meta["payload"]),
                             meta={"url": self.url, "payload": json.loads(self.payload), "current_page": 1},
                             callback=self.parse)


        
        