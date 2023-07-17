import json
import scrapy


class SiskySpiderSpider(scrapy.Spider):
    name = "sisky_spider"
    allowed_domains = ["susicky.heureka.cz"]
    start_urls = ["https://susicky.heureka.cz"]
    def start_requests(self):
        payload = {
            "query": "query ReviewsMixed($countryCode: CountryCode!, $categorySlug: String, $productSlug: String!, $productId: ID, $limit: Int = 10, $offset: Int = 0) { productDetail(countryCode: $countryCode, categorySlug: $categorySlug, productSlug: $productSlug, productId: $productId) { reviews { mixed(limit: $limit, offset: $offset) { ... on ExpertReview { id title perex url filledAt type youtubeId } ... on RegularReview { id shop { id name url ownerId } author { name avatarUrl } filledAt recommendsType rating pros cons summary verified type response { id type text avatarUrl updatedAt } } } } } }",
            "variables": {
                "categorySlug": "susicky",
                "productSlug": "aeg-absolutecare-t8dee68sc",
                "offset": 0,
                "limit": 201,
                "productId": "399384676",
                "countryCode": "CZECH"
            }
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67"
        }

        url = "https://api.heureka.cz/product-detail-gateway/graphql"  # Replace with the actual GraphQL endpoint URL

        yield scrapy.Request(url=url, method="POST", headers=headers, body=json.dumps(payload), callback=self.parse)

    def parse(self, response):
        data_json=response.json()

        data1=data_json['data']['productDetail']
        reviews=data1['reviews']['mixed']
        for r in reviews:
            try:
                puchased_at=r['shop']['name']
            except:
                puchased_at=None
            try:
                reviewer_title=r['author']['name']
            except:
                reviewer_title=None
            try:
                date=r['filledAt']
            except:
                date=None
            try:
                comment=r['response']['text']
            except:
                comment=None
                
            yield {
                "reviewer_title":reviewer_title,
                "puchased_at":puchased_at,
                "date":date,
                "comment":comment
            }
        
           