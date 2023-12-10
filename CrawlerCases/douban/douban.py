# -*- coding: utf-8 -*-
# @Author  : hakusai
# @Time    : 2023/12/10 18:09


from bs4 import BeautifulSoup
import urllib.request, urllib.error
import xlwt  # 进行excel操作
import re
import time

# 获取电影名的规则
findtitle = re.compile(r'<span class="title">(.*?)</span>')
# 创建变量 记录电影链接规则
findlink = re.compile(r'<a href="(.*?)">')
# 获取演员规则
findactors = re.compile(r'<p class="">(.*?)</p>', re.S)  # re.S 让.匹配换行符包括在内
# 获取评分
findscore = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
# 获取评价人数
findsum = re.compile(r'<span>(.*?)人评价</span>')
# 获取图片
findpic = re.compile(r'<img.*src="(.*?)"', re.S)

# 获取简介
findinq = re.compile(r'<span class="inq">(.*?)</span>', re.S)

def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1、爬取网页
    datalist = getdata(baseurl)
    save_path = "./豆瓣电影.xls"

    # 3、保存数据
    saveData(save_path, datalist)

# 爬取网页
def getdata(baseurl):
    datalist = []
    # 使用循环获取所有页面的信息
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        #     # 保存网页源码
        html = askurl(url)
        #     # print(html)
        #
        # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")

        for item in soup.find_all('div', class_="item"):  # 因为class 是一个类别 ，所以要加_
            # print(item)
            data = []  # 保存一部电影的所有信息
            item = str(item)  # 把item换成字符串类型

            # 获取电影名
            title = re.findall(findtitle, item)[0]
            # print(title)
            # title = '片名是：'+ title
            data.append(title)

            # 获取电影链接
            link = re.findall(findlink, item)[0]
            # print(link)
            # link = "电影链接为：" + link
            data.append(link)

            # 获取图片
            pic = re.findall(findpic, item)[0]
            # pic = "图片链接是："+ pic
            data.append(pic)
            # print(pic)

            # 获取评价人数
            sum = re.findall(findsum, item)[0]
            # sum = "评价总人数为：" + sum
            data.append(sum)

            # 获取得分
            score = re.findall(findscore, item)[0]
            # score = '得分' + score
            data.append(score)

            # 获取简介
            jianjie = re.findall(findinq, item)
            # jianjie = '影片名言:'+jianjie[0]
            data.append(jianjie)

            # 获取演员
            actors = re.findall(findactors, item)[0]
            actors = re.sub(r'[a-zA-Z]*', '', actors)
            actors = re.sub(r'\xa0*', '', actors)
            actors = re.sub(r'[/]|</>\n ', '', actors)
            actors = re.sub(r' *', '', actors)
            data.append(actors.strip())  # 去掉空格
            # print(actors)
            datalist.append(data)
            time.sleep(0.1)  # 等待0.1s
            # print(data)
    print("爬取成功")
    return datalist

def saveData(save_path, datalist):
    # 创建一个exel对象
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建一个工作表
    worksheet = workbook.add_sheet('豆瓣电影top_250', cell_overwrite_ok=True)
    # 设计表头
    col = ('电影名', '电影链接', '图片链接', '评价总人数', '豆瓣得分', '电影de相关描述', '电影概况')
    for j in range(len(col)):
        worksheet.write(0, j, col[j])
    # 循环遍历字典写入exel表格
    for i in range(len(datalist)):
        print("第 %d 部电影" % i)
        data = datalist[i]
        for j in range(len(data)):
            worksheet.write(i + 1, j, data[j])
    # 保存Exel表格
    workbook.save(save_path)

# 得到指定网页的url网页内容
def askurl(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }
    req = urllib.request.Request(url=url, headers=header)
    html = ''
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode("utf-8")
        # print(html)
    except:
        print("获取失败")
    return html

if __name__ == "__main__":
    main()
