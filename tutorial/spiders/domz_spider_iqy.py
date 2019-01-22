import scrapy
import re
from scrapy import cmdline
from fake_useragent import UserAgent
import pymysql
from tutorial.items import TutorialItem


class DomzSpider(scrapy.spiders.Spider):
    name = "iqy"

    def __init__(self, category=None, *args, **kwargs):
        # 域名
        self.start_urls = [
            # 爱奇艺vip视频url
        ]
        for i in range(30):
            print(i+1)
            url = 'https://list.iqiyi.com/www/1/----------2---11-'+str(i)+'-1-iqiyi--.html'
            self.start_urls.append(url)
        self.headers = {
            "user-agent":UserAgent().random
        }
        print(self.start_urls)

    def parse(self, response):
        ts = []
        item = TutorialItem()
        titles = response.xpath('/html/body/div[3]/div/div/div[3]/div/ul/li/div[2]/div[1]/p/a').extract()
        try:
            for title in titles:
                t = re.search('<a.*?title=\"(.*?)\".*?href=\"(.*?)\".*?</a>',title,  re.S)
                ts.append(t.group(1) + ' ' + t.group(2))
                print(ts)
            self.save_db(ts)
        except:
            print("****************************************ONE ERROR*******************************************")
        item['movie_title'] = '======================================================SUCCESS——IQY======================================================'
        yield item

    def save_db(self, list):
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            passwd="1006",
            database="movie"
        )
        print('==========================================================================')

        for l in list:
            name = l.split(' ')[0]
            link = l.split(' ')[1]
            # print(link)
            mycursor = mydb.cursor()
            sql = "insert into iqy value ('"+name+"', '"+link+"') on duplicate key update link = '"+link+"', name = '"+name+"';"
            # print(sql)
            mycursor.execute(sql)
        mydb.commit()
        mydb.close()





