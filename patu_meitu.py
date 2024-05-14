import requests
import os
import time
from lxml import etree
from bs4 import BeautifulSoup
import random
# 自定义模块，发送邮件
from send_email import email_func


#从ip代理网站获取ip列表
def get_ip_list(headers):
    i = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    s = random.choice(i)
    # ip代理网站
    proxy_url = 'https://www.89ip.cn/index_' + str(s) + '.html'
    try:
        web_data = requests.get(url=proxy_url, headers=headers)
        soup = BeautifulSoup(web_data.text,'lxml')
        ips = soup.find_all('tr')
        ip_list = []
        for i in range(1,len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            # 拼接成【ip:端口】的格式
            ip_list.append(tds[0].text.replace('\n', '').replace('\t', '') + ':' + tds[1].text.replace('\n', '').replace('\t', ''))
        print(ip_list)
        return ip_list
    except:
        email_func("网络请求出错了，请重新运行程序！", "python爬虫")
        return None

#在ip列表中随机取出一个ip
def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)   #拼接成网址
    proxy_ip = random.choice(proxy_list)    #随机选择一个网址
    proxies = {'http':proxy_ip}  #proxies的格式是一个字典：{‘http’: ‘http://123.123.321.123:808‘}
    return proxies


# 发起请求，找出总页数
def getAllPage(picPageUrl, headers):
    response = requests.get(url=picPageUrl, headers=headers)
    # 处理中文乱码
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    allPage = html.xpath('//div[@class="uk-page uk-text-center"]/span/text()')[0]
    allPage = int(allPage.split('/')[-1])
    print(allPage)
    pageUrl = picPageUrl.split('_')[0]
    # 调用函数get_ip_list 传入参数url和headers，返回一个IP列表
    ip_list = get_ip_list(headers)
    
    i = 2
    while i <= allPage:
        # 调用函数get_random_ip 传入参数是第一个函数得到的列表，返回一个随机的proxies
        proxies = get_random_ip(ip_list)
        pUrl = pageUrl + '_' + str(i) + '.html'
        print(pUrl)
        # 调用函数
        getPicSrc(pUrl, headers, proxies)
        pUrl = ''
        i += 1
        time.sleep(10)


# 发起请求，从页面找出需要的元素内容
def getPicSrc(pUrl, headers, proxies):
    try:
        response = requests.get(url=pUrl, headers=headers, proxies=proxies)
        # 处理中文乱码
        response.encoding = 'utf-8'
        if response.status_code == 200:
            html = etree.HTML(response.text)
            #获取图集名称
            title = html.xpath('//div[@class="uk-article-bd uk-margin-remove"]/p/a/img/@alt')[0]
            print(title)
            #获取图片地址
            picUrl = html.xpath('//div[@class="uk-article-bd uk-margin-remove"]/p/a/img/@src')[0]
            print(picUrl)
            # 调用函数
            getPic(title, picUrl, headers, proxies)
        else:
            return None
    except:
        email_func("网络请求出错了，请重新运行程序！", "python爬虫")
        return None


# 下载图片并保存
def getPic(title, picUrl, headers,proxies):
    path = "images/" + title
    timestamp = str(time.time())
    try:
        response = requests.get(url=picUrl, headers=headers, proxies=proxies)
        if response.status_code == 200:
            if not os.path.exists(path):
                os.makedirs(path)
                with open(path + '/' + timestamp + '.png', 'wb') as file:
                    file.write(response.content)
                    print('下载完成')
            else:
                with open(path + '/' + timestamp + '.png', 'wb') as file:
                    file.write(response.content)
                    print('下载完成')
        else:
            return None
    except:
        email_func("网络请求出错了，请重新运行程序！", "python爬虫")
        return None


def main(pageNum):
    picPageUrl = 'https://m.meitu131.com/meinv/' + pageNum + '/index_2.html'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    getAllPage(picPageUrl, headers)


if __name__ == "__main__":
    # https://www.meitu131.com/nvshen/  首页页面
    # https://www.meitu131.com/meinv/7214/  图集页面
    
    n = 6406
    while n <= 6500:
        pageNum = str(n)
        with open("pageNum.txt","w") as f:
            f.write(pageNum)
        
        # 调用函数
        main(pageNum)
        n += 1
        time.sleep(60)
