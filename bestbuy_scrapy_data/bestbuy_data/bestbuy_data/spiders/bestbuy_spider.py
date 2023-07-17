import scrapy
class BestbuySpiderSpider(scrapy.Spider):
    name = "bestbuy_spider"
    # start_urls = ["https://www.bestbuy.ca/api/v2/json/search?categoryid=&currentRegion=&include=facets%2C%20redirects&lang=en-CA&page=1&pageSize=24&path=&query=mobile&exp=labels&sortBy=relevance&sortDir=desc"]
    pagenumber=1
    search="iphone"
    url=f"https://www.bestbuy.ca/api/v2/json/search?categoryid=&currentRegion=&include=facets%2C%20redirects&lang=en-CA&page=1&pageSize=24&path=&query={search}&exp=labels&sortBy=relevance&sortDir=desc"
    def start_requests(self):
        yield scrapy.Request(self.url,
                                method="GET",
                                headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'},
                                callback=self.parse,
                                dont_filter=True    
                                  )
    def parse(self, response):
        data =response.json()
        all_product=data["products"]
        totalPages=data["totalPages"]   
        
        for one_product in all_product:
            
            Image_path=one_product["productUrl"]
            product_url=f"https://www.bestbuy.ca{Image_path}"
            id=one_product['sku']
            product_name=one_product['name']
            product_salePrice=one_product['salePrice']
            highResImage=one_product['highResImage']
            
            url=f"https://www.bestbuy.ca/api/reviews/v2/products/{id}/reviews?source=all&lang=en-CA&pageSize=25&page=1&sortBy=relevancy"
            yield scrapy.Request(url,
                             method="GET",
                             meta={"Image_path": product_url,"product_name":product_name,"product_salePrice":product_salePrice,"highResImage":highResImage},
                             headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'},
                             callback=self.parse_rating_pagination,
                             dont_filter=True
                             )
        
        self.pagenumber+=1
        if self.pagenumber<=2:
            self.url=f"https://www.bestbuy.ca/api/v2/json/search?categoryid=&currentRegion=&include=facets%2C%20redirects&lang=en-CA&page={self.pagenumber}&pageSize=24&path=&query={self.search}&exp=labels&sortBy=relevance&sortDir=desc"
            yield scrapy.Request(self.url,
                                method="GET",
                                headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'},
                                callback=self.parse,
                                dont_filter=True
                                )
    def parse_rating_pagination(self, response):
        img_url=response.meta['Image_path']
        highResImage=response.meta['highResImage']
        product_name=response.meta['product_name']
        product_salePrice=response.meta['product_salePrice']

        data =response.json()
        page_number=data['totalPages']
        prd_id=data['productId']
        if page_number>0:
            
            for page in range(1,page_number+1):
                url=f"https://www.bestbuy.ca/api/reviews/v2/products/{prd_id}/reviews?source=all&lang=en-CA&pageSize=25&page={page}&sortBy=relevancy"
                yield scrapy.Request(url,
                             method="GET",
                             meta={"Img_path": img_url,"product_name":product_name,"product_salePrice":product_salePrice,"highResImage":highResImage},
                              headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'},
                             callback=self.parse_rating,
                             dont_filter=True
                             )
        else:
            try:
                imgurl =img_url
            except:
                imgurl=None
            try:
                highResImage =highResImage
            except:
                highResImage=None
            try:
                product_name =product_name
            except:
                product_name=None
            try:
                product_salePrice =product_salePrice
            except:
                product_salePrice=None
            yield{"product_name":product_name,
                    "product__salePrice":product_salePrice,
                    "highResImage":highResImage,
                    "imgurl":imgurl,
                    "comment":None,
                    "rating":None,
                    "reviewerName":None,
                    "comment_photo":None}            
    def parse_rating(self, response):
        image_url=response.meta['Img_path']
        highResImage=response.meta['highResImage']
        product_name=response.meta['product_name']
        product_salePrice=response.meta['product_salePrice']
        data_rewiew=response.json() 
        reviews=data_rewiew["reviews"]
        if reviews:
            for dareview in reviews:
                photo=dareview['photos']   
                photos=[]
                for i in photo:
                    img_comment_url=i['thumbnailUrl']
                    print(img_comment_url)
                    photos.append(img_comment_url)
                    print(photos)
                try:
                    comment_photo=photos
                except:
                    comment_photo=None
                try:
                    reviewerName=dareview['reviewerName']
                except:
                    reviewerName=None
                try:
                    rating =dareview['rating']
                except:
                    rating=None
                try:
                    comment =dareview['comment']
                except:
                    comment=None
                try:
                    imgurl =image_url
                except:
                    imgurl=None
                try:
                    product__name =product_name
                except:
                    product__name=None
                try:
                    product__salePrice =product_salePrice
                except:
                    product__salePrice=None
                try:
                    highResImage =highResImage
                except:
                    highResImage=None
                yield{"product_name":product__name,
                      "product__salePrice":product__salePrice,
                      "highResImage":highResImage,
                      "imgurl":imgurl,
                      "comment":comment,
                      "rating":rating,
                      "reviewerName":reviewerName,
                      "comment_photo":comment_photo}
        else:
                try:
                    imgurl =image_url
                except:
                    imgurl=None
                try:
                    product__name =product_name
                except:
                    product__name=None
                try:
                    product__salePrice =product_salePrice
                except:
                    product__salePrice=None
                try:
                    highResImage =highResImage
                except:
                    highResImage=None
                yield{"product_name":product__name,
                      "product__salePrice":product__salePrice,
                      "highResImage":highResImage,
                      "imgurl":imgurl,
                      "comment":None,
                      "rating":None,
                      "reviewerName":None,
                      "comment_photo":None}

