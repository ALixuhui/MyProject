# -*- coding: utf-8 -*-
import scrapy

import re
# 可以拼接地址
from urllib.parse import urljoin
# 爬虫
from scrapy.spiders import Spider
# 请求
from scrapy.http import Request
# 导入字段
from jj20.items import Jj20Item


class GetmeiziSpider(scrapy.Spider):
    name = 'getmeizi'
    # allowed_domains = ['http://www.jj20.com/bz/']

    # 开始路径
    start_urls = ['http://www.jj20.com/bz/nxxz/list_7_1.html']

    # 伪装浏览器

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
    }

    # 一级页面处理函数
    def parse(self, response):

        # 提取所有可以进入url,提取界面所有的符合入口条件的url
        all_urls = response.xpath('//div[@class="main"]/ul/li/a[1]/@href').extract()
        # 每个版块的名字
        file_name = response.xpath('//div[@class="main"]/ul/li/a[2]/text()').extract()
        # print('-------------展示all_urls和file_name-------------')
        # print(all_urls)
        # print(file_name)
        # print('-------------展示抓取的效果-------------')
        # 判断是否获取成功
        if len(all_urls):
            # 将本页面所有的url,循环拼接起来
            for i in range(len(all_urls)):
                # 使用urljoin生成完整的url地址   https://blog.csdn.net/mycms5/article/details/76902041  介绍
                url = urljoin(response.url, all_urls[i])
                # print('-------------展示拼接后的URL-------------')
                # print(all_urls)
                # print(url)
                # print('-------------每次展示一个-------------')
                # 将请求送的二级页面处理方法中去
                yield Request(url, callback=self.parse_img, meta={'file_name': file_name[i]}, headers=self.headers)
            # 动态获取下一页
            # 跳转路径:href="list_7_2.html"--re.search 扫描整个字符串并返回第一个成功的匹配,所以每个页面取得都是下一页
            next_url = re.search(r'list_\d+_(\d+)', response.url)
            # print('-------------next_url-------------')
            # print(next_url)
            next_page = str(int(next_url.group(1)) + 1) + '.html'
            # print('-------------next_page-------------')
            # print(next_page)
            # 下一页面的url
            next_url = re.sub(r'(\d+).html', next_page, response.url)
            print('-------------next_url-------------')
            print(next_url)

            # print('-------------静态获取下一页(测试处理)-------------')
            #
            # next_url = 'http://www.jj20.com/bz/nxxz/list_7_2.html'

            # 再把请求发送回这个方法
            yield Request(next_url, callback=self.parse)

    # 二级页面的处理函数，二级页面里面有一张图片,然后从三级里面再抓取其他的图片
    def parse_img(self, response):
        # 对象标签
        item = Jj20Item()
        # print(response.url)
        # print('-------------xxx-------------')
        # 获取图片地址
        item['image_urls'] = response.xpath('//img[@id="bigImg"]/@src').extract()
        # print(item['image_urls'])
        # print('-------------二级页面的url-------------')
        # 来自于哪个板块的图片
        item['title'] = response.meta['file_name']

        yield item

        # 获取第二个页面中其他图片的url
        # 点击图片就可以跳转到下一页,所以直接在a连接上获取下一页的地址
        all_urls = response.xpath('//ul[@id="showImg"]/li/a/@href').extract()
        # print('-------------二级页面下的url-------------')
        # print(all_urls)
        # 遍历url传到三级处理
        for url in all_urls:
            url = urljoin(response.url, url)
            # print('-------------展示拼接后的URL-------------')
            # print(url)
            # print('-------------每次展示一个-------------')

            # 将请求发送到下一个函数中
            yield Request(url, callback=self.parse_img_img, meta={'file_name': response.meta['file_name']})

    # 三级页面的处理函数
    def parse_img_img(self, response):
        # 继续提取页面中的url
        item = Jj20Item()
        # 由于页面与二级页面一样所以接下来的解析都是一样的
        # 获取图片地址
        # 获取图片地址
        item['image_urls'] = response.xpath('//img[@id="bigImg"]/@src').extract()
        # print(item['image_urls'])
        # print('-------------三级页面的url-------------')
        # 来自于哪个板块的图片
        item['title'] = response.meta['file_name']

        yield item
