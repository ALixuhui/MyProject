# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import os
from scrapy.utils.project import get_project_settings
import requests
import random
import string
# 导入这个包为了移动文件
import shutil


# class Jj20Pipeline(object):

# 使用renquest下载模块(速度较慢)
# def process_item(self, item, spider):
#     img_store = get_project_settings().get('IMAGES_STORE')
#
#     # 模拟浏览器
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
#                "Referer": "http://www.jj20.com/"
#                }
#
#     # 定义保存的路径
#     img_path = "%s%s" % (img_store, item['title'])
#     # print(img_path)
#     # print('-------------不同的路径-------------')
#     # 如果路径不存在
#     if os.path.exists(img_path) == False:
#         os.mkdir(img_path)
#     r = requests.get(url=item['image_urls'][0], headers=headers)
#     # print(item['image_urls'][0], item['title'])
#     # print('-------------每次地址与名字展示-------------')
#     # 下载图片，存储在本地文件目录下
#     # 随机生成名字
#     salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
#     # print(salt)
#     # print('-------------随机出来的名字-------------')
#     with open(img_path + '/' + salt + '.jpg', 'wb') as f:
#         f.write(r.content)

# 通过ImagesPipeline下载图片(速度贼快)
class Jj20Pipeline(ImagesPipeline):
    # 从项目设置文件中导入图片下载路径
    img_store = get_project_settings().get('IMAGES_STORE')

    # print(img_store)
    # print('-------------保存根路径-------------')

    # 重写ImagesPipeline类的此方法
    # 发送图片下载请求
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    # 将不同板块的图片保存到不同的文件夹下
    def item_completed(self, results, item, info):
        image_path = [x["path"] for ok, x in results if ok]  # ok判断是否下载成功

        # print(image_path[0])
        # print('-------------上为下载的返回-------------')

        # 定义保存的路径
        img_path = "%s%s" % (self.img_store, item['title'])
        # print(img_path)
        # print('-------------不同的路径-------------')
        # 如果路径不存在
        if os.path.exists(img_path) == False:
            os.mkdir(img_path)

        # # 将文件从默认的下载路径移动到指定路径下
        # 分割字符串 示例: image_path[0]==/full/6b39bf83fd9dda629aa0854c88e2910f08540d79.jpg
        _, img_name = image_path[0].split("/")
        # print(img_name)
        # print('-------------展示下载后的文件名字-------------')
        # 原文件地址                       移动到哪里
        shutil.move(self.img_store + image_path[0], img_path + "/" + img_name)

        # item["title"] = img_path + "/" + image_path[0] + '.jpg'

        # yield item
