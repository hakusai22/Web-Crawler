
# -*- coding: utf-8 -*-
# @Author  : hakusai
# @Time    : 2023/12/10 21:36

import scrapy
import json

import random
class UserAgentDownloadMiddleware(object):
    # user-agent随机请求头中间件
    USER_AGENTS = [
        "Mozilla/5.0 (compatible; Baiduspider-render/2.0;"
    ]
    def process_request(self, request, spider):
        user_agent = random.choice(self.USER_AGENT)
        request.headers['User-Agent'] = user_agent

class CsdnDownFileItem(scrapy.Item):
    # define the fields for your item here like:
    file_id = scrapy.Field()
    title = scrapy.Field()
    source_url =scrapy.Field()
    pass


class CsdnDownSpider(scrapy.Spider):
    name = 'csdn_down'
    allowed_domains = ['download.csdn.net']
    start_urls = ['https://download.csdn.net/home/get_more_latest_source?page=1']

    def parse(self, response):
        rs =  json.loads(response.text)
        print(response.meta.get('page'))
        page = 2
        if response.meta.get('page') is not None:
            page = int(response.meta.get('page'))
            page += 1
        if rs.get('message') == 'ok':
            # 取出数据
            data = rs.get('data').get('list')
            # 存取数据
            for content in data:
                file_id = content.get('id')
                title = content.get('title')
                source_url = content.get('download_source_url')
                item = CsdnDownFileItem(
                    file_id=file_id,
                    title=title,
                    source_url=source_url
                )
                yield item

        next_url = f"https://download.csdn.net/home/get_more_latest_source?page={page}"
        yield scrapy.Request(url=next_url, callback = self.parse, meta = {'page': page})

