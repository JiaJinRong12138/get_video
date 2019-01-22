import scrapy
import re
from scrapy import cmdline
from fake_useragent import UserAgent
import pymysql
from tutorial.items import TutorialItem


class DomzSpider(scrapy.spiders.Spider):
    name = "tencent"

    def __init__(self, category=None, *args, **kwargs):
        # 域名
        self.offset=0
        self.start_urls = [
            # tencent vip视频url
        ]
        cishu = {
            1:4980,
            2:150,
            3:30
        }
        for a in range(3):
            i = 0
            while(i <= cishu.get(a+1)):
                url = 'https://v.qq.com/x/list/movie?charge='+str(a+1)+'&offset=' + str(i)
                self.start_urls.append(url)
                i += 30
        self.headers = {
            "user-agent":UserAgent().random
        }
        print(self.start_urls)

    def parse(self, response):
        ts = []
        item = TutorialItem()
        titles = response.xpath('/html/body/div[3]/div/div/div[1]/div[2]/div/ul/li/a').extract()
        # print(titles)
        try:
            for title in titles:
                # print(title)
                t = re.search('<a href=\"(.*?)\".*?>.*?<img.*?alt=\"(.*?)\".*?>.*?',title,  re.S)
                ts.append(t.group(2) + ' ' + t.group(1))
                # print(ts)
            self.save_db(ts)
        except:
            print("****************************************ONE ERROR*******************************************")
        item['movie_title'] = '======================================================SUCCESS——Tencent======================================================'
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
            sql = "insert into tencent value ('"+name+"', '"+link+"') on duplicate key update link = '"+link+"', name = '"+name+"';"
            # print(sql)
            mycursor.execute(sql)
        mydb.commit()
        mydb.close()





