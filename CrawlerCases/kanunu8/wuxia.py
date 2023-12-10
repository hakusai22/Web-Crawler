# -*- coding: utf-8 -*-
# @Author  : hakusai
# @Time    : 2023/12/10 17:54

import requests
import re
from bs4 import BeautifulSoup

count_error = []  # 记录无效的网址

def setSrr(url):
    # 判断网址是否有效，如果无效就打印错误并返回。
    if (requests.get(url).status_code == 404):
        print('error')
        global count_error
        count_error.append(url)  # 把错误网址加入到列表
        return []
    print('开始下载……')

    l = []  # 定义列表用来保存小说内容
    r = requests.get(url, timeout=5)  # 获取链接
    r.raise_for_status()  # 检查状态
    r.encoding = r.apparent_encoding  # 改变编码形式
    html = r.text  # 获取文本
    # html = request.urlopen(url).read()    #读取网页中所有的内容
    soup = BeautifulSoup(html, "html.parser")
    item = soup.findAll('h2')  # h2里面是章节标题
    # 这一步的根据是查看网站源码，找到所需要爬去的内容
    print('this......', str(item))  # 打印章节标题处的源码
    title = re.match(r'.*<h2><font color="#dc143c">(.*)</font></h2>.*', str(item), re.M | re.I)  # 用正则表达式提取出章节标题
    print('title:', title.group(1))  # 打印标题，看是否正确
    l.append(title.group(1))  # 标题加入到列表
    # 提取本章节小说内容部分源码，然后剔除源码部分<p>和</p>
    strings = soup.findAll('p')[0].__str__().strip('<p>').strip('</p>')
    # print(strings)

    # 提取出来的字符串按段落切分，然后加到列表中
    l += map(lambda x: x.rstrip(), strings.split('<br/>'))
    # 返回爬去到的内容
    return l

# 内容写到文件上
def setDoc(l, file):
    if len(l) < 2:
        return
    # 追加方式打开文件，并写入文件。
    with open(file, 'a', encoding='utf-8') as f:
        for i in l:
            f.write('\t' + i)
        f.write('\n')

def setNewUrl():
    urls = []  # 所有要爬取的网址
    # 《昆仑》中第一章和最后一章网址数字的差是109，所以有110个网址，生成网址列表返回。
    for s in range(0, 10):
        url = "https://www.kanunu8.com/wuxia/201102/1718/" + str(38407 + s) + ".html"
        urls.append(url)
    return urls

if __name__ == '__main__':
    urls = setNewUrl()
    file = '昆仑.txt'
    # setSrr(urls[0])
    # 爬取每一个网址里面的内容
    for url in urls:
        l = setSrr(url)
        setDoc(l, file)
    # 打印不存在的网址数量和网址
    print(len(count_error))
    print(count_error)
    # 最后发现110个网址，有30个无法访问，《昆仑》正好80章。
