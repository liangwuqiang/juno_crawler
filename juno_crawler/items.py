# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# 定义模型的抓取项目
# See documentation in: 参考文档
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class JunoCrawlerItem(Item):
    artist = Field()  # 艺术家
    title = Field()  # 标题
    label = Field()  # 标签
    tracks = Field()  # 音轨
    catalog_number = Field()  # 目录号
    release_date = Field()  # 发布日期
    genre = Field()  # 流派
