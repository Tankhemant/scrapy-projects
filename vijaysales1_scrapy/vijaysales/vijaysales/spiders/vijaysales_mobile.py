import scrapy
import json


class VijaysalesMobileSpider(scrapy.Spider):
    name = "vijaysales_mobile"
    allowed_domains = ["www.vijaysales.com"]

    payload="{\r\n \"pageNo\":1,\r\n \"SearchData\":\"iphone\",\r\n \"MinPriceData\":\"*\",\r\n \"MaxPriceData\":\"*\",\r\n \"FilterData\":\"\",\r\n \"URLData\":\"\",\r\n \"isDefault\":\"true\",\r\n \"SortBy\":\"0\"\r\n}"

    def start_requests(self):
        url="https://www.vijaysales.com/searchpagenew.aspx/loadProductsUnbxdapi"
        yield scrapy.Request(url,
                             method="POST",
                             body=self.payload,
                             meta={"url":url,"payload":json.loads(self.payload)},
                             headers = {'content-type': 'application/json;charset=UTF-8','origin': 'https://www.vijaysales.com'},
                             callback=self.parse,
                             dont_filter=True
                             )
    def parse(self, response):
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
        if response.meta['payload']['pageNo']<15:
            response.meta['payload']["pageNo"] +=1
            url=response.meta["url"]
        #    response.meta['payload']['firstResult']=response.meta['currunt_page']*12
            yield scrapy.Request(url,
                                 method="POST",
                                 body=json.dumps(response.meta["payload"]),
                                 meta={'url':response.meta['url'],'payload':response.meta['payload']},
                                 headers = {'content-type': 'application/json;charset=UTF-8','origin': 'https://www.vijaysales.com'},
                                 callback=self.parse,
                                 dont_filter=True
                                 )