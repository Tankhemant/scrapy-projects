from ..items import VijayprojectItem

import scrapy
import json
items=VijayprojectItem()
class VijayspiderSpider(scrapy.Spider):
    name = "vijayspider"
    allowed_domains = ["www.vijaysales.com"]
    start_urls = ["https://www.vijaysales.com"]
    
    url="https://www.vijaysales.com/searchpagenew.aspx/loadProductsUnbxdapi"
    payload="{\r\n \"pageNo\":1,\r\n \"SearchData\":\"iphone\",\r\n \"MinPriceData\":\"*\",\r\n \"MaxPriceData\":\"*\",\r\n \"FilterData\":\"\",\r\n \"URLData\":\"\",\r\n \"isDefault\":\"true\",\r\n \"SortBy\":\"0\"}"
    
    def start_requests(self):
        yield scrapy.Request(self.url,
                             method="POST",
                             body=self.payload,
                             meta={"url": self.url, "payload": json.loads(self.payload), "current_page": 1},
                             headers={'content-type': 'application/json;charset=UTF-8', 'origin': 'https://www.vijaysales.com'},
                             callback=self.parse,
                             dont_filter=True
                             )
    
    def parse(self, response):
        # data = json.loads(response.text)
        # Process the data as needed
        # ...

        # Write data to JSON file
            # with open("output.json", "w") as file:
            #     json.dump(data, file)
            #     file.write("\n")
        try:
            data_json=response.json()
            get_data_json=data_json['d']['prdlist']
            for prdlists in get_data_json:
                try:
                    title= prdlists['title']
                except:
                    title=None
                try:
                    imgpath = prdlists['imageUrl']
                except:
                    imgpath=None
                try:
                    salesprice = prdlists['sellingPrice']
                except:
                    salesprice=None
                yield {
                "title": title,
                "imgpath":imgpath,
                "salesprice":salesprice

        }  
        except:
            print("json errorr")
        if response.meta['payload']["pageNo"]<=14:
            response.meta['payload']["pageNo"] += 1
            url = response.meta["url"]
            # response.meta['payload']['firstResult'] = response.meta['currunt_page'] * 12
            yield scrapy.Request(url,
                                method="POST",
                                body=json.dumps(response.meta["payload"]),
                                meta={'url': response.meta['url'], 'payload': response.meta['payload']},
                                headers={'content-type': 'application/json;charset=UTF-8', 'origin': 'https://www.vijaysales.com'},
                                callback=self.parse,
                                dont_filter=True
                                )



# import scrapy
# import json

# class VijayspiderSpider(scrapy.Spider):
#     name = "vijayspider"
#     allowed_domains = ["www.vijaysales.com"]
#     start_urls = ["https://www.vijaysales.com"]
    
#     url="https://www.vijaysales.com/searchpagenew.aspx/loadProductsUnbxdapi"
#     payload="{\r\n \"pageNo\":1,\r\n \"SearchData\":\"iphone\",\r\n \"MinPriceData\":\"*\",\r\n \"MaxPriceData\":\"*\",\r\n \"FilterData\":\"\",\r\n \"URLData\":\"\",\r\n \"isDefault\":\"true\",\r\n \"SortBy\":\"0\"}"
#     def start_request(self):
#         print(self.payload)
#         yield scrapy.Request(self.url,
#                              method="POST",
#                              body=self.payload,
#                              meta={"url":self.url,"payload":json.loads(self.payload)},
#                              headers = {'content-type': 'application/json;charset=UTF-8','origin': 'https://www.vijaysales.com'},
#                              callback=self.parse,
#                              dont_filter=True
#                              )
#     def parse(self, response):
#         print(self.payload)
#         print(response.text)
        
#         response.meta['payload']["pageNo"] +=1
#         print(response.meta['payload']["pageNo"])
#         url=response.meta["url"]
#     #    response.meta['payload']['firstResult']=response.meta['currunt_page']*12
#         yield scrapy.Request(url,
#                                 method="POST",
#                                 body=json.dump(response.meta["payload"]),
#                                 meta={'url':response.meta['url'],'payload':response.meta['payload']},
#                                 headers = {'content-type': 'application/json;charset=UTF-8','origin': 'https://www.vijaysales.com'},
#                                 callback=self.parse,
#                                 dont_filter=True
#                                 )


        #     data = json.loads(response.text)
        # # Process the data as needed
        # # ...

        # # Write data to JSON file
        #     with open("output.json", "a") as file:
        #         json.dump(data, file)
        #         file.write("\n")