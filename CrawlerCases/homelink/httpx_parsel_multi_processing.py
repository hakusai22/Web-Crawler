from bisect import bisect_left, bisect_right, insort_left, insort_right, insort, bisect
from math import ceil, floor, pow, gcd, sqrt, log10, fabs, fmod, factorial, inf, pi, e
from heapq import heapify, heapreplace, heappush, heappop, heappushpop, nlargest, nsmallest
from collections import defaultdict, Counter, deque
from itertools import permutations, combinations, combinations_with_replacement, accumulate, count, groupby
from queue import PriorityQueue, Queue, LifoQueue
from functools import lru_cache
from typing import List
import sys

sys.setrecursionlimit(10001000)

MOD = int(1e9 + 7)
INF = int(1e20)
INFMIN = float('-inf')
INFMAX = float('inf')
PI = 3.141592653589793
direc = [(1, 0), (0, 1), (-1, 0), (0, -1)]
direc8 = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
ALPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alps = 'abcdefghijklmnopqrstuvwxyz'

def alp(i):
    return chr(ord('a') + i % 26)  # i=0->'a', i=25->'z'

def input():
    return sys.stdin.readline().rstrip()

def end(r=-1):
    print(r)
    exit()

# -*- coding: utf-8 -*-
# @Author  : hakusai
# @Time    : 2023/12/08 17:39

from fake_useragent import UserAgent
import csv
import re
import time
from parsel import Selector
import httpx
from multiprocessing import Pool, cpu_count, Queue, Manager


class HomeLinkSpider(object):
    def __init__(self):
        # 因为多进程之间不能共享内存，需使用队列Queue共享数据进行通信
        # 每个进程爬取的数据都存入这个队列，不能使用self.data列表
        # 子进程获取不到self.headers这个变量，需要直接使用UserAgent().random
        # self.ua = UserAgent()
        # self.headers = {"User-Agent": self.ua.random}
        self.q = Manager().Queue()
        self.path = "浦东_三房_500_800万.csv"
        self.url = "https://sh.lianjia.com/ershoufang/pudong/a3p5/"

    def get_max_page(self):
        response = httpx.get(self.url, headers={"User-Agent": UserAgent().random})
        if response.status_code == 200:
            # 创建Selector类实例
            selector = Selector(response.text)
            # 采用css选择器获取最大页码div Boxl
            a = selector.css('div[class="page-box house-lst-page-box"]')
            # 使用eval将page-data的json字符串转化为字典格式
            max_page = eval(a[0].xpath('//@page-data').get())["totalPage"]
            print("最大页码数:{}".format(max_page))
            return max_page
        else:
            print("请求失败 status:{}".format(response.status_code))
            return None

    # 解析单页面，需传入单页面url地址
    def parse_single_page(self, url):
        print("子进程开始爬取:{}".format(url))
        response = httpx.get(url, headers={"User-Agent": UserAgent().random})
        selector = Selector(response.text)
        ul = selector.css('ul.sellListContent')[0]
        li_list = ul.css('li')
        for li in li_list:
            detail = dict()
            detail['title'] = li.css('div.title a::text').get()

            #  2室1厅 | 74.14平米 | 南 | 精装 | 高楼层(共6层) | 1999年建 | 板楼
            house_info = li.css('div.houseInfo::text').get()
            house_info_list = house_info.split(" | ")

            detail['bedroom'] = house_info_list[0]
            detail['area'] = house_info_list[1]
            detail['direction'] = house_info_list[2]


            floor_pattern = re.compile(r'\d{1,2}')
            match1 = re.search(floor_pattern, house_info_list[4])  # 从字符串任意位置匹配
            if match1:
                detail['floor'] = match1.group()
            else:
                detail['floor'] = "未知"

            # 匹配年份
            year_pattern = re.compile(r'\d{4}')
            match2 = re.search(year_pattern, house_info_list[5])
            if match2:
                detail['year'] = match2.group()
            else:
                detail['year'] = "未知"

            # 文兰小区 - 塘桥    提取小区名和哈快
            position_info = li.css('div.positionInfo a::text').getall()
            detail['house'] = position_info[0]
            detail['location'] = position_info[1]

            # 650万，匹配650
            price_pattern = re.compile(r'\d+')
            total_price = li.css('div.totalPrice span::text').get()
            detail['total_price'] = re.search(price_pattern, total_price).group()

            # 单价64182元/平米， 匹配64182
            unit_price = li.css('div.unitPrice span::text').get()
            detail['unit_price'] = re.search(price_pattern, unit_price).group()

            self.q.put(detail)

    def parse_page(self):
        max_page = self.get_max_page()
        print("CPU内核数:{}".format(cpu_count()))

        # 使用进程池管理多进程任务
        with Pool(processes=4) as pool:
            urls = ['https://sh.lianjia.com/ershoufang/pudong/pg{}a3p5/'.format(i) for i in range(1, max_page + 1)]
            # 也可以使用pool.apply_async(self.parse_single_page, args=(url,))
            pool.map(self.parse_single_page, urls)


    def write_csv_file(self):
        head = ["标题", "小区", "房厅", "面积", "朝向", "楼层",
                "年份", "位置", "总价(万)", "单价(元/平方米)"]
        keys = ["title", "house", "bedroom", "area", "direction",
                "floor", "year", "location",
                "total_price", "unit_price"]
        try:
            with open(self.path, 'w', newline='', encoding='utf_8_sig') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                if head is not None:
                    writer.writerow(head)

                # 如果队列不为空，写入每行数据
                while not self.q.empty():
                    item = self.q.get()
                    if item:
                        row_data = []
                        for k in keys:
                            row_data.append(item[k])
                        writer.writerow(row_data)

                print("Write a CSV file to path %s Successful." % self.path)
        except Exception as e:
            print("Fail to write CSV to path: %s, Case: %s" % (self.path, e))

if __name__ == '__main__':
    start = time.time()
    home_link_spider = HomeLinkSpider()
    home_link_spider.parse_page()
    home_link_spider.write_csv_file()
    end = time.time()
    print("耗时：{}秒".format(end-start))