import scrapy


class FinalSpiderSpider(scrapy.Spider):
    name = "final_spider"
    pagenumber=1
    number=1
    pizza="pizza"
    apple="apple"
    coffee="coffee"
    url = f"https://www.yelp.com/search?find_desc={apple}&find_loc=San+Francisco%2C+CA"

    def start_requests(self):
        yield scrapy.Request(self.url,
                                method="GET",
                                headers={ 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'},
                                callback=self.parse,
                                dont_filter=True    
                                  )
        
    def parse(self, response):
        # html=response.text
        # with open("apple_test.html", 'w',encoding="utf-8") as f:
        #     f.write(html)
        all_heading=response.xpath("//div[@class='  padding-t3__09f24__TMrIW padding-r3__09f24__eaF7p padding-b3__09f24__S8R2d padding-l3__09f24__IOjKY border-color--default__09f24__NPAKY']")

        for heading in all_heading:
            name=heading.xpath(".//h3/span/a/text()").get()
            rating=heading.xpath(".//div[@class=' display--inline-block__09f24__fEDiJ margin-r1__09f24__rN_ga  border-color--default__09f24__NPAKY']//div/@aria-label").get()
            product_img=heading.xpath(".//div[@class=' css-w8rns  border-color--default__09f24__NPAKY']/a//img/@src").get()
            page=heading.xpath(".//div[@class=' css-w8rns  border-color--default__09f24__NPAKY']/a/@href").get()
            if page:
                page=f"https://www.yelp.com{page}"
            else:
                page=None
            if name:
                name=name
            else:
                name=None
            if rating:
                rating=rating
            else:
                rating=None
            if page:
                product_img=product_img
            else:
                product_img=None
                

            yield{
                "name":name,
                "rating":rating,
                "product_img":product_img,
                "page":page
            }
        next_page=response.xpath("//div[@class=' navigation-button-container__09f24__SvcBh  border-color--default__09f24__NPAKY']/span/a[@class='next-link navigation-button__09f24__m9qRz css-ahgoya']/@href").get()
        if next_page:
            self.number+=1
            yield scrapy.Request(next_page,
                                    method="GET",
                                    headers={ 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'},
                                    callback=self.parse,
                                    dont_filter=True    
                                    )