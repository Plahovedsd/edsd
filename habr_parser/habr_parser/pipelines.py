# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl

class ExcelExportPipeline:

    def open_spider(self, spider):
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active
        self.sheet.append(['№ п/п', 'url', 'название статьи', 'количество просмотров', 'время чтения', 'количество комментариев'])

    def close_spider(self, spider):
        self.wb.save('articles.xlsx')

    def process_item(self, item, spider):
        self.sheet.append([item['№ п/п'], item['url'], item['название статьи'], item['количество просмотров'], item['время чтения'], item['количество комментариев']])
        return item

class HabrParserPipeline:
    def process_item(self, item, spider):
        return item
