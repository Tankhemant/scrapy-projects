from lxml import etree
from datetime import datetime
import json
import os
from bs4 import BeautifulSoup
import pandas
import scrapy
import xml.etree.ElementTree as ET

class HsciqCodeSpider(scrapy.Spider):
    name = 'hsciq_code'
    custom_settings = {'RETRY_TIMES': 30,
                       'RETRY_HTTP_CODES': [403, 404, 501, 502, 503, 302],
                       'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
                       'ROBOTSTXT_OBEY': False,
                       'DOWNLOAD_TIMEOUT': 20}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    start_date = datetime.utcnow().strftime('%Y-%m-%dT%H%M%S')
    start_date_folder = os.path.join("C:\\Users\\heman\\OneDrive\\Desktop\\sajan_task\\scrapy_task\\hsciq\\output", start_date)
    os.makedirs(start_date_folder, exist_ok=True)

    def start_requests(self):
        # contery_code = ['HSCN','HSJP']
        contery_code = ['HSCN']
        for contery_cd in contery_code:
            if 'HSCN' == contery_cd:
                url = f"http://hsciq.com/{contery_cd}/Search?keywords=01&viewtype=1"
                "http://hsciq.com/HSJP/Search?keywords=01"
                yield scrapy.Request(
                    url=url,
                    method='GET',
                    headers = self.headers,
                    meta={"url":url,"current_page":1,"keyword" : 1,"url_keyword" : "01","contery_cd": contery_cd,"check_hs_code":""},
                    dont_filter=True,
                    callback=self.parse,
                )

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        dom = etree.HTML(str(soup))
        check_hs_code = response.xpath("//tr[3]//a/@data-clipboard-text").get()
        for hs_code in dom.xpath("//*[@class='copy']/@data-clipboard-text"):
            url = f"http://hsciq.com/HSCN/Code/{hs_code}"
            

            yield scrapy.Request(
                url=url,
                method='GET',
                headers = self.headers,
                meta={"url":url},
                callback=self.details,
                dont_filter=True,
            )
            # break
            # print((url),"~~~~~~~~~~~~~~~~~~~~~~")

        next_page = response.xpath("//a[@aria-label='Next']/@href").get()
        if response.meta['check_hs_code'] != check_hs_code and next_page:
            url = f'http://hsciq.com{next_page}'
            yield scrapy.Request(
                                    url=url,
                                    method='GET',
                                    headers = self.headers,
                                    meta={"url":url,
                                        "current_page":response.meta["current_page"],
                                        "keyword":response.meta["keyword"],
                                        "url_keyword":response.meta["url_keyword"],
                                        "check_hs_code":check_hs_code,
                                        "contery_cd":response.meta['contery_cd']
                                        },
                                    dont_filter=True,
                                    callback=self.parse
                                )
        else:
            response.meta["keyword"] += 1
            if response.meta["keyword"] < 10:
                url_keyword = f'0{response.meta["keyword"]}' 
            else:
                url_keyword = response.meta["keyword"]
            if response.meta["keyword"] < 99:
                url = f"http://hsciq.com/{response.meta['contery_cd']}/Search?keywords={url_keyword}&viewtype=1"
                print(url,"$$$$$$$$$$$$$$$$$$$$$$$$")
                yield scrapy.Request(
                    url=url,
                    method='GET',
                    headers = self.headers,
                    meta={"url":url,
                        "current_page":1,
                        "keyword":response.meta["keyword"],
                        "url_keyword":url_keyword,
                        "contery_cd":response.meta['contery_cd'],

                        "check_hs_code":""
                        },
                    dont_filter=True,
                    errback=self.eroor_in_working,
                    callback=self.parse
                )
    element_csv=[]
    def details(self,response):
        
        declaration_elements = []
        regulatory_conditions = []
        inspection_and_quarantine = []
        treaty_rate = []
        rcep_tax_rate = []
        chapter = []
        ciq_code = []

        # basic_information
        try:
            commodity_code = response.xpath('//td[contains(text(),"商品编码")]/following::td[1]/text()').get().strip()
        except:
            try:
                commodity_code = response.xpath('//td[contains(text(),"商品编码")]/following::td[1]/font/text()').get().strip()
            except:
                commodity_code = None    
        try:
            product_name = response.xpath('//td[contains(text(),"商品名称")]/following::td[1]/text()').get().strip()
        except:
            try:
                product_name = response.xpath('//td[contains(text(),"商品名称")]/following::td[1]/font/text()').get().strip()
            except:
                product_name = None    
        try:
            product_description = response.xpath('//td[contains(text(),"商品描述")]/following::td[1]/text()').get().strip()
        except:
            try:
                product_description = response.xpath('//td[contains(text(),"商品描述")]/following::td[1]/font/text()').get().strip()
            except:
                product_description  = None
        try:
            first_legal_unit = response.xpath('//td[contains(text(),"第一法定单位")]/following::td[1]/text()').get().strip()
        except:
            try:
                first_legal_unit = response.xpath('//td[contains(text(),"第一法定单位")]/following::td[1]/font/text()').get().strip()
            except:
                first_legal_unit = None  
        try:
            second_legal_unit = response.xpath('//td[contains(text(),"第二法定单位")]/following::td[1]/text()').get().strip()
        except:
            try:
                second_legal_unit = response.xpath('//td[contains(text(),"第二法定单位")]/following::td[1]/font/text()').get().strip()
            except:
                second_legal_unit = None 
        try:
            state = response.xpath('//td[contains(text(),"状态")]/following::td[1]/text()').get().strip()
        except:
            try:
                state = response.xpath('//td[contains(text(),"状态")]/following::td[1]/font/text()').get().strip()
            except:
                state = None 
        try:
            update_time = response.xpath('//td[contains(text(),"更新时间")]/following::td[1]/text()').get().strip()  
        except:
            try:
                update_time = response.xpath('//td[contains(text(),"更新时间")]/following::td[1]/font/text()').get().strip()
            except:
                update_time = None
        # basic_information = '''<basic_information>'''
        root = ET.Element("data")
        root = ET.Element("basic_information")
        elements = {
            "commodity_code": commodity_code,
            "product_name": product_name,
            "product_description" : product_description,
            "first_legal_unit" : first_legal_unit,
            "second_legal_unit" : second_legal_unit,
            "state" : state,
            "update_time" : update_time
        }

        for tag, value in elements.items():
            if value is not None:
                element = ET.SubElement(root, tag)
                element.text = value
                one_tag = f"<{tag}>{element.text}</{tag}>"
                self.element_csv.append([tag,one_tag])
        basic_information = ET.tostring(root, encoding="unicode", method="xml")

        self.element_csv.append([root.tag,basic_information])
        
        # tax_rate_information    
        try:
            export_tax_rate = response.xpath('//td[contains(text(),"出口税率")]/following::td[1]/text()').get().strip()
        except:
            try:
                export_tax_rate = response.xpath('//td[contains(text(),"出口税率")]/following::td[1]/font/text()').get().strip()
            except:
                export_tax_rate = None    
        try:
            export_tax_rebate_rate = response.xpath('//td[contains(text(),"出口退税税率")]/following::td[1]/text()').get().strip()
        except:
            try:
                export_tax_rebate_rate = response.xpath('//td[contains(text(),"出口退税税率")]/following::td[1]/font/text()').get().strip()
            except:
                export_tax_rebate_rate = None    
        try:
            export_provisional_tax_rate = response.xpath('//td[contains(text(),"出口暂定税率")]/following::td[1]/text()').get().strip()
        except:
            try:
                export_provisional_tax_rate = response.xpath('//td[contains(text(),"出口暂定税率")]/following::td[1]/font/text()').get().strip()
            except:
                export_provisional_tax_rate = None 
        try:
            vat_rate = response.xpath('//td[contains(text(),"增值税率")]/following::td[1]/text()').get().strip()
        except:
            try:
                vat_rate = response.xpath('//td[contains(text(),"增值税率")]/following::td[1]/font/text()').get().strip()
            except:
                vat_rate = None  
        try:
            most_favored_nation_tax_rate = response.xpath('//td[contains(text(),"最惠国税率")]/following::td[1]/text()').get().strip()
        except:
            try:
                most_favored_nation_tax_rate = response.xpath('//td[contains(text(),"最惠国税率")]/following::td[1]/font/text()').get().strip()
            except:
                most_favored_nation_tax_rate = None 
        try:
            import_provisional_tax_rate = response.xpath('//td[contains(text(),"进口暂定税率")]/following::td[1]/text()').get().strip()
        except:
            try:
                import_provisional_tax_rate = response.xpath('//td[contains(text(),"进口暂定税率")]/following::td[1]/font/text()').get().strip()
            except:
                import_provisional_tax_rate = None
        try:
            ordinary_tax_rate = response.xpath('//td[contains(text(),"普通税率")]/following::td[1]/text()').get().strip()
        except:
            try:
                ordinary_tax_rate = response.xpath('//td[contains(text(),"普通税率")]/following::td[1]/font/text()').get().strip()
            except:
                ordinary_tax_rate = None    
        try:
            consumption_tax_rate = response.xpath('//td[contains(text(),"消费税率")]/following::td[1]/text()').get().strip()
        except:
            try:
                consumption_tax_rate = response.xpath('//td[contains(text(),"消费税率")]/following::td[1]/font/text()').get().strip()
            except:
                consumption_tax_rate = None    
    
#  tax_rate_information
        root = ET.Element("tax_rate_information")
        elements = {
            "export_tax_rate" :export_tax_rate,
            "export_tax_rebate_rate" :export_tax_rebate_rate,
            "export_provisional_tax_rate" :export_provisional_tax_rate,
            "vat_rate" :vat_rate,
            "most_favored_nation_tax_rate" :most_favored_nation_tax_rate,
            "import_provisional_tax_rate" :import_provisional_tax_rate,
            "ordinary_tax_rate" :ordinary_tax_rate,
            "consumption_tax_rate" :consumption_tax_rate
        }

        for tag, value in elements.items():
            if value is not None:
                element = ET.SubElement(root, tag)
                element.text = value
                one_tag = f"<{tag}>{element.text}</{tag}>"
                self.element_csv.append([tag,one_tag])

        tax_rate_information = ET.tostring(root, encoding="unicode", method="xml")
        
        self.element_csv.append([root.tag,tax_rate_information])

        df = pandas.DataFrame(self.element_csv)

        df.columns = ["element","tags"]
        df.to_csv("all_data2.csv",index=False,header=True)
        
        # Process regulatory conditions
        for i in response.xpath('//p[contains(text(),"监管条件[")]/following::table[1]/tbody/tr'):
            key = i.xpath('./td[1]/text()').get().replace("[","").strip()
            try:
                try:
                    value = i.xpath('./td[2]/text()').get().replace("[","").strip()
                except:
                    value = i.xpath('./td[2]/font/text()').get().replace("[","").strip()
            except:
                value = "无"
            try:
                condition = {"key": key, "value": value}
            except:
                condition = {"key": key}
            regulatory_conditions.append(condition)

        # Process declaration elements
        for i in response.xpath('//p[contains(text(),"申报要素")]/following::table[1]/tbody/tr'):
            key = i.xpath('./td[1]/text()').get().replace("[","").strip()
            try:
                try:
                    value = i.xpath('./td[2]/text()').get().replace("[","").strip()
                except:
                    value = i.xpath('./td[2]/font/text()').get().replace("[","").strip()
            except:
                value = "无"
            try:
                condition = {"key": key, "value": value}
            except:
                condition = {"key": key}
            declaration_elements.append(condition)

        # Process inspection and quarantine
        for i in response.xpath('//p[contains(text(),"检验检疫类别[")]/following::table[1]/tbody/tr'):
            key = i.xpath('./td[1]/text()').get().replace("[","").strip()
            try:
                try:
                    value = i.xpath('./td[2]/text()').get().replace("[","").strip()
                except:
                    value = i.xpath('./td[2]/font/text()').get().replace("[","").strip()
            except:
                value = "无"
            try:
                condition = {"key": key, "value": value}
            except:
                condition = {"key": key}
            inspection_and_quarantine.append(condition)

        # Process treaty rate
        for i,j in zip(response.xpath('//p[contains(text(),"协定税率")]/following::table[1]/tbody/tr[1]/td'),response.xpath('//p[contains(text(),"协定税率")]/following::table[1]/tbody/tr[2]/td')):
            key = i.xpath('./text()').get().replace("[","").strip()
            try:
                try:
                    value = j.xpath('./text()').get().replace("[","").strip()
                except:
                    value =j.xpath('./font/text()').get().replace("[","").strip()
            except:
                value = "无"
            try:
                condition = {"key": key, "value": value}
            except:
                condition = {"key": key}
            treaty_rate.append(condition)

        # Process RCEP tax rate
        for i,j in zip(response.xpath('//p[contains(text(),"RCEP税率")]/following::table[1]/tbody/tr[1]/td'),response.xpath('//p[contains(text(),"RCEP税率")]/following::table[1]/tbody/tr[2]/td')):
            key = i.xpath('./text()').get().replace("[","").strip()
            try:
                try:
                    value = j.xpath('./text()').get().replace("[","").strip()
                except:
                    value =j.xpath('./font/text()').get().replace("[","").strip()
            except:
                value = "无"
            try:
                condition = {"key": key, "value": value}
            except:
                condition = {"key": key}
            rcep_tax_rate.append(condition)

        # Process chapter
        for i in response.xpath('//p[contains(text(),"所属章节")]/following::table[1]/tbody/tr'):
            key = i.xpath('./td[1]/text()').get().replace("[","").strip()
            try:
                try:
                    value = i.xpath('./td[2]/text()').get().replace("[","").strip()
                except:
                    value = i.xpath('./td[2]/font/text()').get().replace("[","").strip()
            except:
                value = "无"
            try:
                condition = {"key": key, "value": value}
            except:
                condition = {"key": key}
            chapter.append(condition)

        # Process CIQ code
        for i in response.xpath('//p[contains(text(),"CIQ代码表(13位海关编码)")]/following::table[1]/tbody/tr'):
            key = i.xpath('./td[1]/text()').get().replace("[","").strip()
            try:
                try:
                    value = i.xpath('./td[2]/text()').get().replace("[","").strip()
                except:
                    value = i.xpath('./td[2]/font/text()').get().replace("[","").strip()
            except:
                value = "无"
            try:
                condition = {"key": key, "value": value}
            except:
                condition = {"key": key}
            ciq_code.append(condition)

        # Create the root element
        root = ET.Element("code_list")
        
        # Generate XML for declaration elements
        declaration_elements_xml = ET.SubElement(root, "declaration_elements")
        for idx, condition in enumerate(declaration_elements, start=1):
            entry = ET.SubElement(declaration_elements_xml, "entry")
            sequence = ET.SubElement(entry, "sequence")
            sequence.text = str(idx)
            code = ET.SubElement(entry, "code")
            code.text = condition["key"]
            if "value" in condition:
                value = ET.SubElement(entry, "value")
                value.text = condition["value"]

        # Generate XML for regulatory conditions
        regulatory_conditions_xml = ET.SubElement(root, "regulatory_conditions")
        for idx, condition in enumerate(regulatory_conditions, start=1):
            entry = ET.SubElement(regulatory_conditions_xml, "entry")
            sequence = ET.SubElement(entry, "sequence")
            sequence.text = str(idx)
            code = ET.SubElement(entry, "code")
            code.text = condition["key"]
            if "value" in condition:
                value = ET.SubElement(entry, "value")
                value.text = condition["value"]

        # Generate XML for inspection and quarantine
        inspection_and_quarantine_xml = ET.SubElement(root, "inspection_and_quarantine")
        for idx, condition in enumerate(inspection_and_quarantine, start=1):
            entry = ET.SubElement(inspection_and_quarantine_xml, "entry")
            sequence = ET.SubElement(entry, "sequence")
            sequence.text = str(idx)
            code = ET.SubElement(entry, "code")
            code.text = condition["key"]
            if "value" in condition:
                value = ET.SubElement(entry, "value")
                value.text = condition["value"]

        # Generate XML for treaty rate
        treaty_rate_xml = ET.SubElement(root, "treaty_rate")
        for idx, condition in enumerate(treaty_rate, start=1):
            entry = ET.SubElement(treaty_rate_xml, "entry")
            sequence = ET.SubElement(entry, "sequence")
            sequence.text = str(idx)
            code = ET.SubElement(entry, "code")
            code.text = condition["key"]
            if "value" in condition:
                value = ET.SubElement(entry, "value")
                value.text = condition["value"]

        # Generate XML for RCEP tax rate
        rcep_tax_rate_xml = ET.SubElement(root, "rcep_tax_rate")
        for idx, condition in enumerate(rcep_tax_rate, start=1):
            entry = ET.SubElement(rcep_tax_rate_xml, "entry")
            sequence = ET.SubElement(entry, "sequence")
            sequence.text = str(idx)
            code = ET.SubElement(entry, "code")
            code.text = condition["key"]
            if "value" in condition:
                value = ET.SubElement(entry, "value")
                value.text = condition["value"]

        # Generate XML for chapter
        chapter_xml = ET.SubElement(root, "chapter")
        for idx, condition in enumerate(chapter, start=1):
            entry = ET.SubElement(chapter_xml, "entry")
            sequence = ET.SubElement(entry, "sequence")
            sequence.text = str(idx)
            code = ET.SubElement(entry, "code")
            code.text = condition["key"]
            if "value" in condition:
                value = ET.SubElement(entry, "value")
                value.text = condition["value"]

        # Generate XML for CIQ code
        ciq_code_xml = ET.SubElement(root, "ciq_code")
        for idx, condition in enumerate(ciq_code, start=1):
            entry = ET.SubElement(ciq_code_xml, "entry")
            sequence = ET.SubElement(entry, "sequence")
            sequence.text = str(idx)
            code = ET.SubElement(entry, "code")
            code.text = condition["key"]
            if "value" in condition:
                value = ET.SubElement(entry, "value")
                value.text = condition["value"]

        # Serialize the XML tree to a string
        xml_string = ET.tostring(root, encoding="unicode")

        root = ET.Element("data")
        root1 = ET.fromstring(basic_information)

        # Load the second XML data
        root2 = ET.fromstring(tax_rate_information)

        # Load the third XML data
        root3 = ET.fromstring(xml_string)

        # Append the root elements of the XML data to the main root element
        root.append(root1)
        root.append(root2)
        root.append(root3)

# Create a new XML tree using the main root element
        new_tree = ET.ElementTree(root)

        product_code = str(response.url.split("Code/")[1].split(".html")[0])
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H%M%S')

        hscode_parts = [product_code[:i] for i in range(2, len(product_code) + 2, 2)]
        hscode_folders = [os.path.join(self.start_date_folder, "\\".join(hscode_parts[:i])) for i in range(1, len(hscode_parts) + 1)]
        for folder in hscode_folders:
            os.makedirs(folder, exist_ok=True)

        url = f"http://hsciq.com/HSCN/Code/{product_code}"

        
        file_name = f"{product_code}_{timestamp}.html"
        file_path = os.path.join(hscode_folders[-1], file_name)
        with open(file_path, 'w',encoding ="utf-8") as file:
            file.write(response.text)

        file_name = f"{product_code}_{timestamp}.xml"
        file_path = os.path.join(hscode_folders[-1], file_name)
        new_tree.write(file_path, encoding="utf-8")
        metadata = {
            "url": url,
            "point_in_time": timestamp,
            "status": "success"
        }
        json_res = json.dumps(metadata, indent=4)
        metadata_file = os.path.join(hscode_folders[-1], "download_success.json")
        with open(metadata_file, 'w') as file:
            file.write(json_res)
        yield { "product_code":product_code}

    def eroor_in_working(self, failure):
        request = failure.request
        meta = request.meta
        current_url_keyword = meta["url_keyword"]
        new_url_keyword = str(int(current_url_keyword) + 1).zfill(2)

        # Create the new URL with the updated url_keyword
        url = f"http://hsciq.com/{meta['contery_cd']}/Search?keywords={new_url_keyword}&viewtype=1"
        # Retry the request with the updated URL and meta
        yield scrapy.Request(
            url=url,
            method='GET',
            headers=self.headers,
            meta={
                "url": url,
                "current_page": 1,
                "keyword": meta["keyword"],
                "url_keyword": new_url_keyword,
                "contery_cd": meta['contery_cd'],
                "check_hs_code": ""
            },
            dont_filter=True,
            callback=self.parse
        )
