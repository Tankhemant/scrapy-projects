from concurrent import futures
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree

list_for_csv=[]
def next_method(number):
    print(number)
    url = "https://www.vijaysales.com/searchpagenew.aspx/loadProductsUnbxdapi"

    payload = {'pageNo': number,'SearchData': 'iphone','MinPriceData': '*','MaxPriceData': '*','FilterData': '','URLData': '','isDefault': 'true','SortBy': '0'
    }

    headers = {
        'content-type': 'application/json;charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    }

    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()  # Check for any HTTP errors

    soup = BeautifulSoup(r.content, 'html.parser')

    json_data = json.loads(str(soup))
    product_list=json_data['d']['prdlist']
    

    for path_obj in product_list:
        dict_for_csv={}
        path=path_obj['productUrl']
        r1 = requests.post(path)
        r1.raise_for_status()  # Check for any HTTP errors

        soup1 = BeautifulSoup(r1.content, 'html.parser')
        etree_obj = etree.HTML(str(soup1))
        # with open("test.html", "w",encoding='utf-8') as f:
        #     f.write(str(soup1))
        all_div=etree_obj.xpath("//div[@class='clsKeyFeatures']/div[@class='highlights']")
        os = ''.join(all_div[0].xpath(".//span/text()")[0]).replace("\n","")
        internal_memory = ''.join(all_div[2].xpath(".//span/text()")[0]).replace("\n","")
        dict_for_csv['path']=path
        dict_for_csv['os']=os
        dict_for_csv['internal_memory']=internal_memory
        list_for_csv.append(dict_for_csv)
with futures.ThreadPoolExecutor(20) as ex:
    for i in range(1,25):
        ex.submit(next_method,i)
csv_dataframe=pd.DataFrame(list_for_csv)
csv_dataframe.to_csv("final_data1.csv",index=False)

    


        
