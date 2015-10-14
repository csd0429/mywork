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
    name = "kjoo_techcrunch"
    allowed_domains = ["techcrunch.cn"]
    start_urls = ['http://techcrunch.cn/',]
    rules=(
        Rule(LinkExtractor(allow=r"/\d{4}/\d{2}/\d{2}/*"),
        callback="parse_news",follow=True),
    )
    for i in range(1,10):
        start_urls.append('http://www.techcrunch.cn/page/'+str(i)+'/')


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
        return item

    def get_news_id(self,response,item):

        item['news_id']='TC'+response.url[-7:-1]

    def get_news_title(self,response,item):
        news_title=response.xpath("/html/body/div[2]/article/div/div[1]/div/header/h1/text()").extract()
        if news_title:
            item['news_title']=news_title[0]

    def get_news_info(self,response,item):
        news_info=response.xpath("/html/body/div[2]/article/div/div[1]/div/div/div[1]/div/div[1]/descendant::text()").extract()
        if news_info:
            item['news_info']=news_info
            print news_info

    def get_news_content(self,response,item):
            item['news_content']=response.url

    def get_news_img(self,response,item):
        news_img=response.xpath("/html/body/div[2]/article/div/div[1]/div/div/div[1]/div/div[1]/img/@src").extract()

        if news_img:
            user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
            headers={'User-Agent':user_agent,}

            result='{'
            count=0
            for img in news_img:
                request=urllib2.Request(img,None,headers)
                file=urllib2.urlopen(request)
                tmpIm=cStringIO.StringIO(file.read())
                im=Image.open(tmpIm)
                if im.size[0]>=400 and im.size[1]>=400:
                    result+=img+','
                    count+=1
                if count==3:
                    result=result[:-1]+'}'
                    item['news_img']=result
                    break
                if img==news_img[len(news_img)-1] and count!=0:
                    result=result[:-1]+'}'
                    item['news_img']=result
                    break

    def get_news_date(self,response,item):
        news_date=response.xpath("/html/body/div[2]/article/div/div[1]/div/header/div[2]/div[1]/time/@datetime").extract()

        if news_date:
            date=news_date[0]+' '+str(random.randint(0,23))+':'+str(random.randint(0,59))+':'+str(random.randint(0,59))
            newsdate=datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
            today=datetime.datetime.today()
            daterange=today-datetime.timedelta(days=30)


            if newsdate>daterange:
                rd= random.uniform(0.0001,1)
                item['news_date']=str(newsdate)+str(rd)[1:6]

    def get_news_source(self,response,item):
        item['news_source']='TechCrunch日报'

    def get_news_status(self,response,item):
        news_status=response.url
        item['news_status']=0

    def get_type_id(self,response,item):
        item['type_id']='KJOO'

    def get_news_url(self,response,item):

        item['news_url']=response.url
