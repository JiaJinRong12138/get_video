import scrapy
from fake_useragent import UserAgent
import pymysql
from tutorial.items import TutorialItem


class DomzSpider(scrapy.spiders.Spider):
    name = "youku"

    def __init__(self, category=None, *args, **kwargs):
        # 域名
        self.offset=0
        self.start_urls = [
            # tencent vip视频url
        ]
        cishu = {
            2:30,
            3:24
        }
        for a in range(2):
            i = 0
            while(i <= cishu.get(a+2)):
                url = 'http://list.youku.com/category/show/c_96_pt_'+str(a+2)+'_s_6_d_1_p_' + str(i) + '.html?spm=a2h1n.8251845.0.0'
                self.start_urls.append(url)
                # print(url)
                i += 1
        self.headers = {
            "user-agent":UserAgent().random
        }
        print(self.start_urls)

    def parse(self, response):
        ts = []
        item = TutorialItem()
        titles = response.xpath('/html/body/div[3]/div/div[2]/div[2]/ul/li/div/ul[2]/li[1]/a').extract()
        print(titles)
        try:
            for title in titles:
                print(title)
                t = re.search('<a href=\"(.*?)\".*?>.*?<img.*?alt=\"(.*?)\".*?>.*?',title,  re.S)
                # ts.append(t.group(2) + ' ' + t.group(1))
                # print(ts)
            # self.save_db(ts)
        except:
            print("****************************************ONE ERROR*******************************************")
        item['movie_title'] = '======================================================SUCCESS——YouKu======================================================'
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





