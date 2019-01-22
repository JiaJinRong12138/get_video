from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute('scrapy crawl youku'.split())
    # cmdline.execute('scrapy crawl tencent'.split())
    # cmdline.execute('scrapy crawl iqy'.split())