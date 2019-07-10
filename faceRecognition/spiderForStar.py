# -*- coding: utf-8 -*-
# @Time    : 2019/7/2 16:14
# @Author  : LiJinjin
# @Email   : 1484972292@qq.com
# @File    : spiderForStar.py
# @Software: PyCharm

# -*- coding: utf-8 -*-
import requests
import re
import os
from pypinyin import pinyin, lazy_pinyin


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("")


def getPageUrls(text, name):
    re_pageUrl = r'href="(.+)">\s*<img src="(.+)" alt="' + name
    return re.findall(re_pageUrl, text)


def downPictures(text, root, name):
    pageUrls = getPageUrls(text, name)
    titles = re.findall(r'alt="' + name + r'(.+)" ', text)
    for i in range(len(pageUrls)):
        pageUrl = pageUrls[i][0]
        path = root + titles[i] + "//"
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.listdir(path):
            pageText = getHTMLText(pageUrl)
            totalPics = int(re.findall(r'<em>(.+)</em>）', pageText)[0])
            downUrl = re.findall(r'href="(.+?)" class="">下载图片', pageText)[0]
            cnt = 1;
            while (cnt <= totalPics):
                picPath = path + str(cnt) + ".jpg"
                r = requests.get(downUrl)
                with open(picPath, 'wb') as f:
                    f.write(r.content)
                    f.close()
                print('{} - 第{}张下载已完成\n'.format(titles[i], cnt))
                cnt += 1
                nextPageUrl = re.findall(r'href="(.+?)">下一张', pageText)[0]
                pageText = getHTMLText(nextPageUrl)
                downUrl = re.findall(r'href="(.+?)" class="">下载图片', pageText)[0]
    return


def main():
    name = input("请输入想要搜索的明星姓名:")
    nameUrl = "https://image.baidu.com/search/acjson" + ''.join(lazy_pinyin(name)) + ".html"
    try:
        text = getHTMLText(nameUrl)
        if not re.findall(r'暂无(.+)!', text):
            root = r"C:\Users\SAM\Pictures\明星图片" + name + "//"
            if not os.path.exists(root):
                os.mkdir(root)
            downPictures(text, root, name)
            try:
                nextPage = re.findall(r'next" href="(.+)"', text)[0]
                while (nextPage):
                    nextText = getHTMLText(nextPage)
                    downPictures(nextText, root, name)
                    nextPage = re.findall(r'next" href="(.+)"', nextText)[0]
            except IndexError:
                print("已全部下载完毕")
    except TypeError:
        print("不好意思，没有{}的照片".format(name))
    return


if __name__ == '__main__':
    main()