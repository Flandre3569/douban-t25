# -*- codeing = utf-8 -*-
# @Time: 2022/1/28 20:40
# @Author: Coisini
# @File: spider.py
# @Software: PyCharm
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import re
import xlwt


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 爬取网页获取的内容
    dataList = getData(baseurl)

    # 保存数据
    savePath = "豆瓣电影Top25.xls"
    saveData(dataList, savePath)


# 影片链接获取规则
findLink = re.compile(r'<a href="(.*?)">')  # 生成正则表达式对象
# 影片封面获取规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
# 影片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findScore = re.compile(r'<span.*property="v:average">(.*)</span>')
# 评价人数
findNum = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取网页 获取数据
def getData(baseurl):
    dataList = []
    for i in range(0, 1):
        url = baseurl + str(i * 25)
        html = askUrl(url)  # 获取到的单个网页源码
    # 解析数据
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div', class_="item"):    # 查找符合要求的字符串，形成列表
        data = []  # 保存一部电影的全部信息
        item = str(item)

        # 获取影片链接
        link = re.findall(findLink, item)[0]   # 使用正则表达式查找指定的字符串
        data.append(link)

        imgSrc = re.findall(findImgSrc, item)[0]
        data.append(imgSrc)

        titles = re.findall(findTitle, item)
        if(len(titles) == 2):
            ctitle = titles[0]
            data.append(ctitle)
            otitle = titles[1].replace("/", "")
            otitle = re.sub("\xa0", "", otitle)
            data.append(otitle)
        else:
            data.append(titles[0])
            data.append(' ')

        score = re.findall(findScore, item)[0]
        data.append(score)

        num = re.findall(findNum, item)[0]
        data.append(num)

        inq = re.findall(findInq, item)
        if len(inq) != 0:
            inq = inq[0].replace("。", "")
            data.append(inq)
        else:
            data.append(" ")

        bd = re.findall(findBd, item)[0]
        bd = re.sub('<br(\s+)?/>(\s+)?', ' ', bd)
        bd = re.sub('/', " ", bd)
        bd = re.sub('\xa0', " ", bd)
        data.append(bd.strip())  # 去掉前后空格

        dataList.append(data)  # 把处理好的一部电影信息放入dataList
    return dataList


# 得到指定一个url的网页内容
def askUrl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接受什么水平的分件）
    request = urllib.request.Request(url, headers=head)
    html = ""

    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def saveData(dataList, savePath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet("豆瓣电影top25", cell_overwrite_ok=True)
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评分人数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, 25):
        print("第%d条" % (i+1))
        data = dataList[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])   # 数据填写

    book.save(savePath)  # 保存


if __name__ == '__main__':
    main()
    print("爬取完成")
