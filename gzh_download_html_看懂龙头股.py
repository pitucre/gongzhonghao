import datetime
import random
from pathlib import Path

from pathlib import Path
import requests
import json
import time
import re
from bs4 import BeautifulSoup
import os
from PIL import Image, ImageDraw, ImageFont
import shutil


# import pdfkit
# import wechatsogou


# 保存下载的 html 页面和图片
def save(search_response, html_dir, file_name):
    # 保存 html 的位置
    htmlDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), html_dir)
    # 保存图片的位置
    targetDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), html_dir + '/images')
    # 不存在创建文件夹
    if not os.path.isdir(targetDir):
        os.makedirs(targetDir)
    domain = 'https://mp.weixin.qq.com/s'
    # 调用保存 html 方法
    save_html(search_response, htmlDir, file_name)
    # 调用保存图片方法
    save_file_to_local(htmlDir, targetDir, search_response, domain, file_name)


# 保存图片到本地
def save_file_to_local(htmlDir, targetDir, search_response, domain, file_name):
    # 使用lxml解析请求返回的页面
    obj = BeautifulSoup(save_html(search_response, htmlDir, file_name).content, 'lxml')
    # 找到有 img 标签的内容
    imgs = obj.find_all('img')
    # 将页面上图片的链接加入list
    urls = []
    for img in imgs:
        if 'data-src' in str(img):
            urls.append(img['data-src'])
        elif 'src=""' in str(img):
            pass
        elif "src" not in str(img):
            pass
        else:
            urls.append(img['src'])

    # 遍历所有图片链接，将图片保存到本地指定文件夹，图片名字用0，1，2...
    i = 0
    for each_url in urls:
        # 跟据文章的图片格式进行处理
        if each_url.startswith('//'):
            new_url = 'https:' + each_url
            r_pic = requests.get(new_url)
        elif each_url.startswith('/') and each_url.endswith('gif'):
            new_url = domain + each_url
            r_pic = requests.get(new_url)
        elif each_url.endswith('png') or each_url.endswith('jpg') or each_url.endswith('gif') or each_url.endswith(
                'jpeg'):
            r_pic = requests.get(each_url)
        time.sleep(random.randint(1, 2))
        # 创建指定目录
        t = os.path.join(targetDir, str(i) + '.jpeg')
        # t1要把图片存成相对路径，否则移动位置无法打开
        t1 = os.path.join('images', str(i) + '.jpeg')
        print('该文章共需处理--' + str(len(urls)) + '张图片，正在处理第' + str(i + 1) + '张……')
        # 指定绝对路径
        fw = open(t, 'wb')
        # 保存图片到本地指定目录
        fw.write(r_pic.content)

        i += 1
        # 将旧的链接或相对链接修改为直接访问本地图片
        update_file(each_url, t1, htmlDir, file_name)
        fw.close()
        # 给图片加水印
        fp = open(t, 'rb')
        im = Image.open(fp).convert('RGBA')  # 这里改为文件句柄
        barcode = random.choice([r'F:\File\个人\微信二维码.png', r'F:\File\个人\微信二维码.png'])
        logo = Image.open(barcode)
        txt = Image.new('RGBA', im.size, (0, 0, 0, 0))
        txt.paste(logo, (im.size[0] - logo.size[0], im.size[1] - logo.size[1]))
        fnt = ImageFont.truetype("c:/Windows/fonts/simkai.ttf", 20)
        d = ImageDraw.Draw(txt)
        d.text((im.size[0] - 250, im.size[1] - 80), u"WX:guduxin2020 整理", font=fnt, fill=(255, 255, 255, 255))
        Image.alpha_composite(im, txt).save(str(t).replace('jpeg', 'png'), 'png')

        fp.close()

        shutil.copyfile(str(t).replace('jpeg', 'png'), t)
        os.remove(str(t).replace('jpeg', 'png'))


# 保存 HTML 到本地
def save_html(url_content, htmlDir, file_name):
    f = open(htmlDir + "/" + file_name + '.html', 'wb')
    # 写入文件
    f.write(url_content.content)
    f.close()
    return url_content


# 修改 HTML 文件,将图片的路径改为本地的路径
def update_file(old, new, htmlDir, file_name):
    # 打开两个文件，原始文件用来读，另一个文件将修改的内容写入
    with open(htmlDir + "/" + file_name + '.html', encoding='utf-8') as f, open(htmlDir + "/" + file_name + '_bak.html',
                                                                                'w', encoding='utf-8') as fw:
        # 遍历每行，用replace()方法替换路径
        for line in f:
            new_line = line.replace(old, new)
            new_line = new_line.replace("data-src", "src")
            # 写入新文件
            fw.write(new_line)
    # 执行完，删除原始文件
    os.remove(htmlDir + "/" + file_name + '.html')
    time.sleep(0.5)
    # 修改新文件名为 html
    os.rename(htmlDir + "/" + file_name + '_bak.html', htmlDir + "/" + file_name + '.html')


with open("F:\source\PYTHON\python-100-day-master\python-100-day-master\公众号文章保存\cookie.txt", "r") as file:
    cookie = file.read()
cookies = json.loads(cookie)
url = "https://mp.weixin.qq.com"
response = requests.get(url, cookies=cookies)
# token = re.findall(r'token=(\d+)', str(response.url))[0]
token = re.findall(r'token=(\d+)', str(response.url))[0]
headers = {
    "Host": "mp.weixin.qq.com",
    "Referer": "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=1595906960&lang=zh_CN",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

# 循环遍历前10页的文章
for j in range(1, 5, 1):
    begin = (j - 1) * 5
    # 请求当前页获取文章列表
    requestUrl = "https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=" + str(
        begin) + "&count=5&fakeid=MzAxMDYxNDQ4NA==&type=9&query=&token=" + token + "&lang=zh_CN&f=json&ajax=1"
    search_response = requests.get(requestUrl, cookies=cookies, headers=headers)
    # MzU2NzEwMDc1MA== 爱在冰川
    # MzAxMDYxNDQ4NA== 看懂龙头股
    # MzIyMjAyMzkyNw==下注的快感
    # Mzg5MzEyNzEwNQ==财联社
    # MzI5ODc4Njc2Ng==盘口逻辑拆解

    # 获取到返回列表 Json 信息
    re_text = search_response.json()
    list = re_text.get("app_msg_list")

    if list is not None:
        # file_normal = open('公众号文章链接_平常1.txt', mode='a', encoding='utf-8')
        # file_saturday = open('公众号文章链接_周六1.txt', mode='a', encoding='utf-8')
        # 遍历当前页的文章列表
        for i in list:
            # 将文章链接转换 pdf 下载到当前目录
            tupTime = time.localtime(i["create_time"])  # 秒时间戳
            standardTime = time.strftime("%Y%m%d", tupTime)  # 转换Wie正常的时间
            title = i["title"]
            # print(i["link"] + "  " + i["title"] + " " + standardTime)
            # 目录名为标题名，目录下存放 html 和图片
            pat = r"(\xe2\x98\x85|\xe2\x97\x86)|(\[\d+-\d+-\d+\])"
            repat = re.compile(pat)
            # 特殊字符替换
            dir_name = repat.sub('_', i["title"])
            print(os.path.dirname(__file__))
            # if (os.path.exists(dir_name)):
            #     print('已经存在' + dir_name)
            #     continue
            dir_name = dir_name.replace(' ', '')
            dir_name = dir_name.replace('，', '')
            dir_name = dir_name.replace('：', '')
            dir_name = dir_name.replace('?', '')
            dir_name = dir_name.replace('？', '')
            dir_name = dir_name.replace('/', '_')
            dir_name = dir_name.replace('|', '_')
            dir_name = dir_name.replace('*', '_')
            # dir_name = i["title"].replace(' ', '').replace(':',)
            myfolder = Path(standardTime + '_' + dir_name)
            if myfolder.is_dir():
                print('已经存在' + dir_name)
                continue
            print("正在下载文章：" + dir_name)
            # 请求文章的url，获取文章内容
            response = requests.get(i["link"], cookies=cookies, headers=headers)

            # 保存文章到本地
            try:
                if str(i["title"]).__contains__('周六'):
                    save(response, standardTime + '_' + dir_name,standardTime + '_' + dir_name)
                else:
                    save(response, standardTime + '_' + dir_name, standardTime + '_' + dir_name)
            except Exception:
                # print('第d%页第d%篇文章错误' % (j - 1) % begin)
                print(('第{page}页第{count}篇文章{dir_name}错误' + str(Exception.args)).format(page=(j - 1), count=(begin),
                                                                                       dir_name=dir_name))
                continue
            # 将html文件转换为pdf文件
            # pdfkit.from_file(dir_name + "/" + i["aid"] + '.html', i["title"] + standardTime + '.pdf')
            # 重命名pdf文件名字

            # os.rename(dir_name + "/" + standardTime + '.html', dir_name + "/" + dir_name+standardTime + '.html')
            print('第{page}页第{count}篇文章{dir_name} 下载完成！'.format(page=str(j - 1), count=str(begin), dir_name=dir_name))
            # if str(i["title"]).__contains__('周六'):
            #     file_saturday.writelines(i["title"] + " " + standardTime + "\r\n' " + i["link"] + '\r\n')
            # else:
            #     file_normal.writelines(i["title"] + " " + standardTime + "\r\n' " + i["link"] + '\r\n')

            # 过快请求可能会被微信问候，这里进行10秒等待
            # time.sleep(1)

            # file_normal.close()
            # file_saturday.close()
