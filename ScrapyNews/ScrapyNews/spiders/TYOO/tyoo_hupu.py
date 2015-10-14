#encoding: utf-8
import scrapy
import re
from scrapy.selector import Selector

from ScrapyNews.items import ScrapyNewsItem
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule
import random
import cStringIO,urllib2,datetime
from PIL import Image
class ExampleSpider(CrawlSpider):
    name = "tyoo_hupu"
    allowed_domains = ["wap.hupu.com"]
    start_urls = ['http://wap.hupu.com/',]
    rules=(
        Rule(LinkExtractor(allow=r"/*/news/\d{7}.html"),
        callback="parse_news",follow=True),
    )
    for i in range(1,30):
        start_urls.append('http://wap.hupu.com/nba/news-'+str(i))
    for i in range(1,30):
        start_urls.append('http://wap.hupu.com/soccer/news-'+str(i))

    def parse_news(self,response):
        item = ScrapyNewsItem()
        self.get_news_id(response,item)
        self.get_news_title(response,item)
        self.get_news_info(response,item)
        self.get_news_content(response,item)
        self.get_news_img(response,item)
        self.get_news_url(response,item)
        self.get_news_date(response,item)
        self.get_news_source(response,item)
        self.get_news_status(response,item)
        self.get_type_id(response,item)
        print(item['news_title'])
        return item

    def get_news_id(self,response,item):
        news_id=response.url
        if news_id:
            item['news_id']='HP'+news_id[-11:-5]

    def get_news_title(self,response,item):
        news_title=response.xpath("/html/body/div[2]/text()").extract()
        if news_title:
            item['news_title']=news_title[0]

    def get_news_info(self,response,item):
        news_info=response.xpath("/html/body/div/text()").extract()
        if news_info:
            item['news_info']=news_info

    def get_news_content(self,response,item):
            item['news_content']='http://m'+response.url[10:]

    def get_news_img(self,response,item):
        news_img=response.xpath("/html/body/div[4]/center/img/@src").extract()
        if news_img:
            file=urllib2.urlopen(news_img[0][56:].replace("%3A",":").replace("%2F","/"))
            tmpIm=cStringIO.StringIO(file.read())
            im=Image.open(tmpIm)
            if im.size[0]>=400 and im.size[1]>=400:
                item['news_img']='{'+news_img[0][56:].replace("%3A",":").replace("%2F","/")+'}'

    def get_news_date(self,response,item):
        news_date=response.xpath("/html/body/div[3]/text()").extract()
        if news_date:
            newsdate=datetime.datetime.strptime(str(news_date[0]),"%Y-%m-%d %H:%M:%S")
            today=datetime.datetime.today()
            daterange=today-datetime.timedelta(days=1)

            if newsdate>daterange:
                rd= random.uniform(0.0001,1)
                item['news_date']=news_date[0][0:19]+str(rd)[1:6]

    def get_news_source(self,response,item):
        news_source=response.xpath("//*[@id='endText']/div[2]/span/text()").extract()
        item['news_source']='虎扑'
    def get_news_status(self,response,item):
        news_status=response.url
        item['news_status']=0
    def get_type_id(self,response,item):
        item['type_id']='TYOO'

    def get_news_url(self,response,item):

        item['news_url']=response.url