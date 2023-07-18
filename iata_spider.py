import pandas
import scrapy


class IataSpiderSpider(scrapy.Spider):
    name = "iata_spider"
    allowed_domains = ["www.iata.org"]
    start_urls = ["https://www.iata.org"]

    all_prod_details = []

    def start_requests(self):
        for letter_f in range(ord('a'), ord('z') + 1):
            for letter_s in range(ord('a'), ord('z') + 1):
                search = f"{chr(letter_f)}{chr(letter_s)}"
                url = f"https://www.iata.org/en/publications/directories/code-search?airline.search={search}"
                yield scrapy.Request(
                    url,
                    method="GET",
                    headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
                    },
                    callback=self.parse,
                    dont_filter=True
                )
        for letter_f in range(0,10):
            for letter_s in range(0,10):
                format0to9=f"{letter_f}{letter_s}"
                url = f"https://www.iata.org/en/publications/directories/code-search?airline.search={format0to9}"
                yield scrapy.Request(
                    url,
                    method="GET",
                    headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
                    },
                    callback=self.parse,
                    dont_filter=True
                )
        for letter_f in range(0,10):
            for letter_s in range(ord('a'), ord('z') + 1):
                format0to9andatoz=f"{letter_f}{chr(letter_s)}"
                
                url = f"https://www.iata.org/en/publications/directories/code-search?airline.search={format0to9andatoz}"
                yield scrapy.Request(
                    url,
                    method="GET",
                    headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
                    },
                    callback=self.parse,
                    dont_filter=True
                )

        df = pandas.DataFrame(self.all_prod_details)
        df.columns = ["company_name", "country_name", "letter_code"]
        df.to_csv("all_data2.csv", index=False, header=True)

    def parse(self, response):
        all_row = response.xpath("//tbody/tr")
        for i in all_row:
            company_name = i.xpath(".//td[1]/text()").get()
            country_name = i.xpath(".//td[2]/text()").get()
            letter_code = i.xpath(".//td[3]/text()").get()
            if [company_name, country_name, letter_code] in self.all_prod_details:
                pass
            else:
                self.all_prod_details.append([company_name, country_name, letter_code])

        # df = pandas.DataFrame(self.all_prod_details)
        # df.columns = ["company_name", "country_name", "letter_code"]
        # df.to_csv("all_data.csv", index=False, header=True)
