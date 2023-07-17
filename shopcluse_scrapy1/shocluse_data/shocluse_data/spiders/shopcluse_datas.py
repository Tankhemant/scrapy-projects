import scrapy
from ..items import ShocluseDataItem
items=ShocluseDataItem()

class ShopcluseDatasSpider(scrapy.Spider):
    name = "shopcluse_datas"
    page_number=6
    allowed_domains = ["www.shopclues.com"]
    start_urls = ["https://www.shopclues.com/search?q=mobiles&sc_z=&z=0&count=9&user_id=&user_segment=default"]
    
    def parse(self, response):
        all=response.xpath("//div[@class='column col3 search_blocks']")
        for  divs in all:
            imgpath=divs.xpath(".//a/div[@class='img_section']/img/@data-img").get()
            price=divs.xpath(".//div[@class='prd_p_section new_prd_section']//span[@class='p_price']/text()").get().strip()
            name=divs.xpath(".//h2/text()").get()
            # yield {"name":name,"imgpath":imgpath,"price":price}
            items["name"]=name
            items["imgpath"]=imgpath
            items["price"]=price
            yield items
        next_page=f"https://www.shopclues.com/ajaxCall/searchProducts?q=mobiles&z=0&page={ShopcluseDatasSpider.page_number}&filters=&fl_cal=1&sc_z=&user_id=&user_segment=default"
        
        if ShopcluseDatasSpider.page_number<=1950:
            ShopcluseDatasSpider.page_number+=1
            print(next_page)
            yield response.follow(next_page,callback=self.parse)