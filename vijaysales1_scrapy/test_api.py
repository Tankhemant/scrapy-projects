import requests

url = "https://www.vijaysales.com/searchpagenew.aspx/loadProductsUnbxdapi"

payload = "{'pageNo': 10,'SearchData': 'iphone','MinPriceData': '*','MaxPriceData': '*','FilterData': '','URLData': '','isDefault': 'true','SortBy': '0'\r\n}"
headers = {
  'content-type': 'application/json;charset=UTF-8',
  'origin': 'https://www.vijaysales.com',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
