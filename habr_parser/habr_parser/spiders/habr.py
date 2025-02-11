import scrapy

class HabrSpider(scrapy.Spider):
    name = 'habr'
    allowed_domains = ['habr.com']
    start_urls = ['https://habr.com/ru/companies/edison/articles/']

    def parse(self, response):
        articles = response.xpath('//article')

        for idx, article in enumerate(articles, start=1):
            Amount_of_views = article.xpath('.//span[@class="tm-icon-counter__value"]/@title').get()
            reading_time = article.xpath('.//span[@class="tm-article-reading-time__label"]/text()').get()

            yield {
                '№ п/п': idx,
                'url': 'https://habr.com' + article.xpath('.//h2/a/@href').get(default=''),
                'название статьи': article.xpath('.//h2/a/span/text()').get(default='').strip(),
                'количество просмотров': self.extract_int(Amount_of_views),
                'время чтения': self.extract_reading_time(reading_time),
                'количество комментариев': self.extract_int(article.xpath('.//span[contains(@class, "comments-count")]/text()').get(default='0')),
            }
        #переход на след. страницу
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def extract_int(self, value):
        return int(value.split()[0]) if value and value.split()[0].isdigit() else 0

    def extract_reading_time(self, value):
        return int(value.split()[0]) if value else 0
