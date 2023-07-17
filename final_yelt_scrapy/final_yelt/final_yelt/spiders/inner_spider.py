import scrapy
import json

class InnerSpiderSpider(scrapy.Spider):
    name = "inner_spider"
    PAGE_NUMBER=0
    count=0
    number=0
    def start_requests(self):
        with open('pizza.json', 'r') as f:
            data = json.load(f)
            for i in data:
                # self.count=0
                self.number+=1
                page=i["page"]
                name=i['name']
                rating=i["rating"]
                product_img=i["product_img"]
                if self.number==1:
                    if page:
                        page="https://www.yelp.com/biz/blondie-s-pizza-san-francisco?osq=pizza"
                        yield scrapy.Request(page,
                                method="GET",
                                headers={ 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'},
                                meta={"page":page,'product_img':product_img,'name':name,'rating':rating},
                                callback=self.parse,
                                dont_filter=True    
                                )  
    def parse(self,response):
        page=response.meta['page']
        product_img=response.meta['product_img']
        name=response.meta['name']
        rating=response.meta['rating']
        request_id=response.xpath("//meta[5]/@content").get()
        # request=f"https://www.yelp.com/biz/{request_id}/props?osq=pizza"
        request=f"https://www.yelp.com/biz/{request_id}/review_feed?rl=en&osq=pizza&start=0"
        if request_id:
                    yield scrapy.Request(request,
                            method="GET",
                            headers={ 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'},
                            meta={'request_id':request_id,"page":page,'product_img':product_img,'name':name,'rating':rating},
                            callback=self.parse_pagination,
                            dont_filter=True)  
    def parse_pagination(self,response):
        page=response.meta['page']
        product_img=response.meta['product_img']
        name=response.meta['name']
        rating=response.meta['rating']
        request_id=response.meta['request_id']
        data =response.json()
        print(page)
        data1=data['pagination']['totalResults']
        
        # with open("jsonformate.json", 'w') as json_file:
        #     json.dump(data, json_file)
        comment=data['reviews']
        for comment1 in comment:
            reviewe_photo=comment1['user']['src']
            reviewer_comment=comment1['comment']['text']
            reviewer_name=comment1['user']['altText']
            reviewer_location=comment1["user"]["displayLocation"]
            localizedDate=comment1['localizedDate']
            try:
                 localizedDate=localizedDate
            except:
                 localizedDate=None
            try:
                 reviewer_location=reviewer_location
            except:
                 reviewer_location=None
            try:
                 reviewe_photo=reviewe_photo
            except:
                 reviewe_photo=None
            try:
                 reviewer_comment=reviewer_comment
            except:
                 reviewer_comment=None
            try:
                 reviewer_name=reviewer_name
            except:
                 reviewer_name=None
            try:
                 page=page
            except:
                 page=None
            try:
                 rating=rating
            except:
                 rating=None
            try:
                 name=name
            except:
                 name=None
            try:
                 product_img=product_img
            except:
                 product_img=None
            yield {'name':name,
                   'product_img':product_img,
                   'rating':rating,
                   "reviewe_photo":reviewe_photo,
                   "reviewer_comment":reviewer_comment,
                   "reviewer_name":reviewer_name,
                   'reviewer_location':reviewer_location,
                   'localizedDate':localizedDate,
                   'page':page,
                   'data1':data1
                   

            }   
        self.count+=10
             
        request=f"https://www.yelp.com/biz/{request_id}/review_feed?start={self.count}"
        if self.count<=data1:
                    yield scrapy.Request(request,
                            method="GET",
                            headers={ 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'},
                            callback=self.parse_pagination,
                            meta={'request_id':request_id,"page":page,'product_img':product_img,'name':name,'rating':rating},
                            dont_filter=True)