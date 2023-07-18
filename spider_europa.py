import scrapy


class SpiderEuropaSpider(scrapy.Spider):
    name = "spider_europa"

    def start_requests(self):
        url="https://ec.europa.eu/taxation_customs/dds2/rd/rd_download_home.jsp?Lang=en"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        link_href=response.xpath("//div[@id='outer-container']//div[@class='ecl-file__container_custom']//a[1]/@href")[0].get()

        yield scrapy.Request(link_href, callback=self.parse_link)

    def parse_link(self, response):
        
        file_name = response.url.split('/')[-1]

        with open(file_name, 'wb') as file:
            file.write(response.body)