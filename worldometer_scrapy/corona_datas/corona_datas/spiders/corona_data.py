import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CoronaDataSpider(scrapy.Spider):
    name = "corona_data"
    start_urls = ["https://www.worldometers.info/coronavirus/"]

    def __init__(self):
        options = Options()
        options.add_argument("--headless")  # Run Chrome in headless mode
        service = Service(ChromeDriverManager().install())  # Path to your ChromeDriver executable
        self.driver = webdriver.Chrome(service=service, options=options)

    def parse(self, response):
        self.driver.get(response.url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "main_table_countries_today")))

        # Extract the HTML content after JavaScript rendering
        html = self.driver.page_source
        selector = Selector(text=html)

        all_links = selector.xpath("//div[@class='main_table_countries_div']//table[@id='main_table_countries_today']//tbody//tr[@role='row']//td//a[starts-with(@href,'country/')]")

        for link in all_links:
            country_link = link.xpath("@href").get()
            next_page=f"https://www.worldometers.info/coronavirus/{country_link}"
            yield scrapy.Request(url=next_page, method="POST",callback=self.parse_for_csv)

    def parse_for_csv(self,response):
        country=response.xpath("//div[@class='content-inner']//div[@style]/h1[1]/text()[2]").get()
        Coronavirus_Cases=response.xpath("//div[@id='maincounter-wrap']/div[1]/span/text()").get().strip()
        death=response.xpath("//div[@class='content-inner']//div[5]/div/span/text()").get()
        revovery=response.xpath("//div[@class='content-inner']//div[6]/div/span/text()").get()
       
        countri1=country.replace("\xa0","").strip()
        yield{"country":countri1,
              "cases":Coronavirus_Cases,
              "death":death,
              "revovery":revovery,

              }
    def closed(self, reason):
        self.driver.quit()
