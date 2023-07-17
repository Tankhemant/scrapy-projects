import requests

# url = "https://www.yelp.com/biz/mSMZJj2pFvttWLpcDmgrEA/review_feed?rl=en&osq=pizza&start=6450"
# url = "https://www.yelp.com/biz/WHJ2spR-_1P_tbiOqOibjg/review_feed?q=pizza&start=9"
url = "https://www.yelp.com/biz/PTFxtXS47ZVRCdZIrEWvGw/review_feed?rl=en&osq=pizza&start=0"
payload = {}
headers = {







}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
