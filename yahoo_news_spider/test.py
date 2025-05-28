import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

url = "https://tw.news.yahoo.com/archive/"
base_url = url

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/113.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

# 找新聞文章區塊，根據 Yahoo 新聞頁面結構調整 selector
articles = soup.select("li.StreamMegaItem")

for article in articles:
    # 標題
    title_tag = article.select_one("h3.Mb\\(5px\\) a")
    if not title_tag:
        title_tag = article.select_one("h3 a")
    title = title_tag.get_text(strip=True) if title_tag else "無標題"
    
    # 連結
    link = title_tag["href"] if title_tag and title_tag.has_attr("href") else None
    if link and not link.startswith("http"):
        link = base_url + link
    
    # 作者、時間（合併文字節點）
    now = datetime.now()
    author_time_tag = article.find("div", class_=re.compile(r"C\(#959595\)"))
    if author_time_tag:
        author_and_time = author_time_tag.get_text(strip=True)
    else:
        author_and_time = "未知"
    
    if '•' in author_and_time:
        author, time_str = [x.strip() for x in author_and_time.split('•')]
    else:
        author, time_str = author_and_time, author_and_time
    # 例：40分鐘前
    if match := re.match(r"(\d+)\s*分鐘前", time_str): 
        time = now - timedelta(minutes=int(match.group(1)))
    
    # 例：1小時前
    elif match := re.match(r"(\d+)\s*小時前", time_str): 
        time = now - timedelta(hours=int(match.group(1)))
    
    # 例：2天前
    elif match := re.match(r"(\d+)\s*天前", time_str): 
        time = now - timedelta(days=int(match.group(1)))
    
    # 轉換失敗
    else:
        time = None  
    
    print("標題:", title)
    print("連結:", link)
    print("作者:", author)
    print("時間:", time)
    print("-" * 40)


{"id":"9956214d-8ef6-3844-a043-3cf822920270",
 "content_type":"STORY",
 "title":"世壯運棒球  Energy隊奪勝賽後合影 (圖)",
 "url":"/%E4%B8%96%E5%A3%AF%E9%81%8B%E6%A3%92%E7%90%83-energy%E9%9A%8A%E5%A5%AA%E5%8B%9D%E8%B3%BD%E5%BE%8C%E5%90%88%E5%BD%B1-%E5%9C%96-081324038.html",
 "summary":"世壯運棒球競賽男子35+組Energy隊28日與55+組美國Boston Wolfpack隊打友誼賽，最終Energy隊以8比2奪勝，賽後兩隊在場中自拍合影。",
 "thumbnail":{
     "url":"https://s.yimg.com/uu/api/res/1.2/teRV8zGqn8tjsc3S31Shiw--~B/Zmk9ZmlsbDtoPTEyODtweW9mZj0wO3c9MjIwO2FwcGlkPXl0YWNoeW9u/https://media.zenfs.com/en/cna.com.tw/4a2d19407a7681eef3f4cefa582a9376",
     "width":220,
     "height":128},
 "published_at":1748420004,
 "provider_name":"中央社",
 "type":"story"},

'''
class YahooBreakNewsSpider(scrapy.Spider):
    name = "yahoo_break_news"
    allowed_domains = ["tw.news.yahoo.com"]
    start_urls = ["https://tw.news.yahoo.com/archive/"]
    time_range = datetime.now() - timedelta(hours=1) # 可調整時間範圍

    def start_requests(self):
        url = self.start_urls[0]
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        time.sleep(5)
        print("Start scrolling...")

        wait = WebDriverWait(driver, 10)
        max_scroll = 50
        pause_time = 5
        for _ in range(max_scroll):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)
            page = driver.page_source

        '''
'''
         try:
        wait.until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "li.StreamMegaItem")) > previous_count
        )
        previous_count = len(driver.find_elements(By.CSS_SELECTOR, "li.StreamMegaItem"))
        print(f"文章數量：{previous_count}")
    except:
        print("文章數量未增加，可能已到底或無更多文章")
        break
       
        for _ in range(max_scroll):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)

            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="C(#959595)"]')))
            except:
                print("Element dosen't exist. Please check!")

            page = driver.page_source
            sel = Selector(text=page)
            info = sel.css("div.C\\(#959595\\)::text").getall()
            print(f"!!!!!:{info[0:5]}")

            absolute_times = []
            for item in info:
                if "•" in item:
                    try: 
                        _, relative_time = [x.strip() for x in item.split("•")]
                        print(relative_time)
                        absolute_time = self.parse_relative_time_to_absolute_time(relative_time)
                        print(absolute_time)
                        if absolute_time:
                            absolute_times.append(absolute_time)

                    except Exception as e:
                        print(f"Error Occur: {e}")
                        continue

            
            earliest_article_time = min(absolute_times)
            in_time_range = earliest_article_time < self.time_range
            if absolute_times and in_time_range:
                break
        '''
'''            
        yield scrapy.Request(
            url = url,
            callback = self.parse,
            meta = {"html":page},
            dont_filter=True 
        )
        driver.quit()
        print("End scrolling")
        



    def parse(self, response):
        print("Start parsing...")
        if "html" not in response.meta:
            self.logger.warning(f"Skipping response for URL: {response.url} - 'html' key not found in meta. This response might be from Scrapy's default start_urls handling.")
            return

        # 取得所有文章
        page = response.meta["html"]
        sel = Selector(text=page)
        articles = sel.css("li.StreamMegaItem")
        print(articles)

        # 取得文章資訊：標題、作者、時間、連結
        for article in articles:
            # 標題
            title = article.css("h3.Mb\\(5px\\) a::text").get()
            print(title)
            
            # 連結
            link = article.css("a::attr(href)").get()
            parent_url = self.start_urls[0]
            url = parent_url + link

            print(link)
            
            # 作者、時間
            author_and_time = article.css('div[class*="C(#959595)"]::text').get(default="未知")
            print(author_and_time)
            ## 拆分
            if not author_and_time:
                continue
        
            if '•' in author_and_time:
                author, time_str = [x.strip() for x in author_and_time.split('•')]
            else:
                author, time_str = author_and_time, author_and_time
                
            
            ## 解析時間，匯集資料
            absolute_time = self.parse_relative_time_to_absolute_time(time_str)
            print(absolute_time)
            in_time_range = absolute_time >= self.time_range
            if absolute_time and in_time_range:            
                item = YahooBreakNewsItem()
                item["title"] = title
                item["author"] = author
                item["time"] = absolute_time
                item["link"] = url
                yield item
        
        print("End parsing")

            
    
    def parse_relative_time_to_absolute_time(self, time_str):
        print("Start parsing to absolute time...")
        now = datetime.now()

        # 例：40分鐘前
        if match := re.match(r"(\d+)\s*分鐘前", time_str): 
            return now - timedelta(minutes=int(match.group(1)))
        
        # 例：1小時前
        elif match := re.match(r"(\d+)\s*小時前", time_str): 
            return now - timedelta(hours=int(match.group(1)))
        
        # 例：2天前
        elif match := re.match(r"(\d+)\s*天前", time_str): 
            return now - timedelta(days=int(match.group(1)))
        
        # 轉換失敗
        else:
            return None  
        
'''    
    

            

