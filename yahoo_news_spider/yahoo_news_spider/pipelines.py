# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import pandas as pd
import os
from datetime                   import datetime, timedelta
from yahoo_news_spider.items    import YahooBreakNewsItem


class CsvExportPipeline:
    def __init__(self):
        self.tmp_storage = []

    def process_item(self, item, spider):
        self.tmp_storage.append(dict(item))
        return item
    
    def close_spider(self, spider):
        spider.logger.info("Closing spider, exporting data to CSV...")
        self.export_csv(spider)
    
    def export_csv(self, spider):
        if not self.tmp_storage:
            spider.logger.warning("No items collected, skipping CSV export.")
            return
        
        # 爬取的即時新聞資料
        collect_news = pd.DataFrame(self.tmp_storage)
        # 資料的時間範圍
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1)
        # 命名檔案、設定檔案路徑
        filename = f"yahoo_breaking_news_{start_time}_{end_time}.csv"
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        # 寫入csv
        collect_news.to_csv(filepath, index=False, encoding='utf-8-sig')
        # 紀錄log
        spider.logger.info(f"Successfully exported {len(collect_news)} items to {filepath}")


# class YahooBreakNewsPipeline:


