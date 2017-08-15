# -*- coding: utf-8 -*-

import scrapy
from scrapy import Spider
from scrapy.http import Request
from juno_crawler.items import JunoCrawlerItem


class JunoSpider(Spider):
    name = "juno"
    # allowed_domains = ["junodownload.com"]
    start_urls = [
        # 'http://www.junodownload.com/all/back-cat/releases/?music_product_type=single'
        'file:///home/lwq/Desktop/juno_crawler/html/Dance music downloads catalogue.html'
    ]

    def parse(self, response):
        next_page_url = response.xpath('//a[span[contains(@class, "glyphicon-arrow-right")]]/@href').extract_first()

        item = JunoCrawlerItem()
        releases = response.xpath('.//div[@class="productlist_widget_container"]')
        for release in releases:
            """艺术家"""
            artist_text = release.xpath(
                './/div[@class="productlist_widget_product_artists"]/span[@class="jq_highlight pwrtext"]'
                '/descendant-or-self::*/text()')
            artist_list = []
            for artist in artist_text:
                artist_list.append(artist.extract())
            artist = ''.join(artist_list)
            item['artist'] = artist
            # print(artist)
            """标题"""
            title = release.xpath(
                './/div[@class="productlist_widget_product_title"]/span[@class="jq_highlight pwrtext"]/a/text()')\
                .extract_first()
            item['title'] = title
            """标签"""
            label = release.xpath(
                './/div[@class="productlist_widget_product_label"]/span[@class="jq_highlight pwrtext"]/a/text()')\
                .extract_first()
            item['label'] = label
            """音轨(单曲)"""
            track_div = release.xpath('.//div[@class="productlist_widget_tracklist_left"]')
            for tracks in track_div:
                track_urls = tracks.xpath(
                    './/div[@class="productlist_widget_tracklist_row"]/a[@ua_action="play"]/@href').extract()
                track_name_list = tracks.xpath(
                    './/div[@class="productlist_widget_tracklist_row_text"]/span[@class="jq_highlight"]/text()')\
                    .extract()
                track_names = []
                for tracks1 in track_name_list:
                    track = tracks1.replace('\t', '')
                    if len(track) > 0:
                        track_names.append(track)
                tracks = list(zip(track_names, track_urls))
                item['tracks'] = tracks
            """目录号"""
            catalog_number = release.xpath(
                './/div[@class="productlist_widget_product_preview_buy"]/text()').extract_first()
            catalog_number = catalog_number.strip()
            item['catalog_number'] = catalog_number
            """发布日期"""
            release_date = release.xpath(
                './/div[@class="productlist_widget_product_preview_buy"]/span/text()').extract_first()
            item['release_date'] = release_date
            """流派"""
            genre = release.xpath(
                './/div[@class="productlist_widget_product_preview_buy"]/span/following-sibling::span/text()')\
                .extract_first()
            genre = genre.strip()
            item['genre'] = genre

            yield item
            print(item)
            break
        yield Request(next_page_url)

        # Python yield 使用浅析
        # https://www.ibm.com/developerworks/cn/opensource/os-cn-python-yield/

# 运行结果:
# {'artist': u'CLEAR VIEW feat JESSICA',
#  'catalog_number': u'SB 215-0',
#  'genre': u'Progressive House',
#  'label': u'Songbird Holland',
#  'release_date': u'10 Sep 08',
#  'title': u'Tell Me',
#  'tracks': [(u'Tell Me - (6:43)',
#              u'http://www.junodownload.com/MP3/SF1354749-02-01-01.mp3'),
#             (u'Tell Me (Max Graham remix) - (8:49)',
#              u'http://www.junodownload.com/MP3/SF1354749-02-01-02.mp3')]}
