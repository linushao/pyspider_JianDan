#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-06-27 09:22:49
# Project: jiandan

from pyspider.libs.base_handler import *

DIR_PATH = '/Users/acewei/pythonDemo/jiandan'


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v0.2',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36 QQBrowser/4.1.4132.400',
            'Cookie': 'bad-click-load=off; nsfw-click-load=on; gif-click-load=off; jdna=01b0531fab6a989460dd1b231010b496#1498527296411',
        }
    }

    def __init__(self):
        self.deal = Deal()
        # 倒序
        self.page_start = 145
        self.page_end = 130
        self.base_url = 'http://jandan.net/ooxx/page-'
        # 从这开始 'http://jandan.net/ooxx/page-145#comments'

    def on_start(self):
        while self.page_start >= self.page_end:
            url = self.base_url + str(self.page_start) + '#comments'
            self.page_start -= 1
            self.crawl(url, callback=self.index_page)

    def index_page(self, response):
        num = 1;
        cuttent_page = response.url.split('page-')[-1]
        print(cuttent_page)
        for img_a in response.doc('ol.commentlist a.view_img_link').items():
            self.crawl(img_a.attr.href, callback=self.save_img_page, save={'num': num, 'cuttent_page': cuttent_page})
            num += 1

    def save_img_page(self, response):
        num = response.save['num']
        cuttent_page = response.save['cuttent_page']
        print(cuttent_page)

        content = response.content
        img_url = response.url
        print(img_url)

        file_name = img_url.split('/')[-1]
        file_name = file_name.split('?')[0]

        dir_path = DIR_PATH + '/' + str(cuttent_page)
        dir_path = self.deal.mkDir(dir_path)
        print(dir_path)

        img_path = dir_path + '/' + str(num) + '.' + self.deal.getExtension(img_url)
        print(img_path)

        self.deal.saveImg(content, img_path)


import urllib, os


class Deal:
    def __init__(self):
        self.path = DIR_PATH
        if not self.path.endswith('/'):
            self.path = self.path + '/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def saveImgByUrl(url, filename):
        urllib.urlretrieve(url, filename)

    def mkDir(self, path):
        path = path.strip()
        # dir_path = self.path + path
        dir_path = path
        exists = os.path.exists(dir_path)
        if not exists:
            os.makedirs(dir_path)
            return dir_path
        else:
            return dir_path

    def saveImg(self, content, path):
        f = open(path, 'wb+')
        f.write(content)
        f.close()

    def saveBrief(self, content, dir_path, name):
        file_name = dir_path + "/" + name + ".txt"
        f = open(file_name, "wb+")
        f.write(content.encode('utf-8'))

    def getExtension(self, url):
        extension = url.split('.')[-1]
        extension = extension.split('?')[0]
        return extension
