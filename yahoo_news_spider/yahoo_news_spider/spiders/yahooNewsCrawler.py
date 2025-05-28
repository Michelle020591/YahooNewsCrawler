import scrapy
import re
import time
from datetime                           import datetime, timedelta
from yahoo_news_spider.items            import YahooBreakNewsItem
import json
from urllib.parse                       import quote


class YahooBreakNewsSpider(scrapy.Spider):
    name = "yahoo_break_news"
    allowed_domains = ["tw.news.yahoo.com"]
    base_url = "https://tw.news.yahoo.com/_td-news/api/resource/ListService"
    
    def start_requests(self):
        start = 0
        yield self.make_request(start)
    

    def make_request(self, start):
        ncpParams = {
            "query": {
                "count": 50,
                "imageSizes": "220x128",
                "documentType": "article",
                "start": start,
                "tag": None
            }
        }
        

        ncpParams_encoded = quote(json.dumps(ncpParams))
        
        params = {
            "api": "archive",
            "ncpParams": ncpParams_encoded,
            "bkt": "c1-pc-twnews-article-r2",
            "device": "desktop",
            "ecma": "modern",
            "feature": "oathPlayer,enableEvPlayer,enableGAMAds,enableGAMEdgeToEdge,videoDocking",
            "intl": "tw",
            "lang": "zh-Hant-TW",
            "partner": "none",
            "prid": "05obhrpk3ddat",
            "region": "TW",
            "site": "news",
            "tz": "Asia/Taipei",
            "ver": "2.3.3021",
            "returnMeta": "true"
        }
        
        url = f"{self.base_url};api={params["api"]};ncpParams={params["ncpParams"]}&bkt={params["bkt"]}&device={params["device"]}&ecma={params["ecma"]}&feature={params["feature"]}&intl={params["intl"]}&lang={params["lang"]}&partner={params["partner"]}&prid={params["prid"]}&region={params["region"]}&site={params["site"]}&tz={params["tz"]}&ver={params["ver"]}&returnMeta={params["returnMeta"]}"
        
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://tw.news.yahoo.com/",
        }
        
        return scrapy.Request(url, headers=headers, callback=self.parse, meta={"start": start})
    

    def parse(self, response):
        items = json.loads(response.text)
        print(items)
        
        if not items:
            self.logger.info("No more items, stop crawling.")
            return
        
        for item in items:
            newsItem = YahooBreakNewsItem()
            newsItem["title"] = item["title"]
            newsItem["author"] = item["provider_name"]
            newsItem["time"] = datetime.fromtimestamp(item["published_at"])
            newsItem["link"] = self.base_url + item["url"]
            yield newsItem
        
        next_start = response.meta["start"] + 50
        
        if next_start < 500:  
            yield self.make_request(next_start)



