import time
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import os
import datetime

# 获取微信公众号新闻
from upload_datas import upload

date = datetime.datetime.now()
year = str(date.year)
month = str(date.month)
today = str(date.day)
if date.month < 10:
    month = "0" + month
if date.day < 10:
    today = "0" + today
today = month + today


def get_access():
    return webdriver.Firefox()


def load_page(driver, url):
    driver.get(url)
    page = driver.page_source
    return page


# 获取新闻列表页面
def next_page(page):
    soup = BeautifulSoup(page, "html.parser")
    link = soup.find('div', attrs={"class": "img-box"})
    link_to = link.find('a')
    return link_to.attrs['href']


def get_news_urls(page):
    base_url = 'https://mp.weixin.qq.com'
    # 存储新闻页面的列表
    # news_urls = {}
    news_urls = []
    soup = BeautifulSoup(page, "html.parser")
    # 新闻列表
    news_list = soup.find_all('h4', attrs={'class': 'weui_media_title'})
    # 全部新闻标题
    for i in news_list:
        news_url = base_url + i.attrs['hrefs']
        news_urls.append(news_url)
    return news_urls


def download_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    data = response.read()
    return data


def get_imgs_url(url):
    images = []
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    imgs = soup.find_all('img')
    for img in imgs:
        try:
            images.append(img.attrs['data-src'])
        except:
            pass
    with open("test.html", "wb") as fp:
        fp.write(soup.encode())
    print("get_imgs_url done")
    return images


def news_save(soup, img_src, path):
    for script in soup.findAll('script'):
        script.extract()
    # for style in soup.findAll('style'):
    #     style.extract()
    title = soup.find("h2", attrs={'class': "rich_media_title"}).get_text()
    content = soup.find("div", attrs={"class": "rich_media_content"})
    title = title.strip()
    imgs = soup.find_all('img')
    index = 0
    for img in imgs:
        try:
            if img['data-src'] is not None:
                img['src'] = "../../" + img_src[index]
                index += 1
        except:
            pass
    name = str(upload(content, title))
    with open(path + name + ".html", "wb") as fp:
        fp.write(soup.encode())
    print(title + "***\tDone")


def get_news(news_urls):
    for url in news_urls:
        img_src = []
        index = 1
        imgs = get_imgs_url(url)
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        head = soup.find('div', attrs={'class': 'rich_media_meta_list'})
        date = head.find('em').get_text()
        img_path = "images/" + date + "/"
        html_path = year + "/" + today + "/"
        if os.path.exists(html_path) is False:
            os.makedirs(html_path)
        if os.path.exists(img_path) is False:
            os.makedirs(img_path)
        else:
            print("数据库已存在数据")
            continue
        for img in imgs:
            # 将每个img链接重新解析
            image = download_page(img)
            img_path = "images/" + date + "/" + str(index)
            with open(img_path, 'wb') as fp:
                fp.write(image)
                img_src.append(img_path)
                index += 1
        news_save(soup, img_src, html_path)
    print("Done")
    return


def initial():
    html_url = "http://weixin.sogou.com/weixin?type=1&query=%E5%9B%BD%E9%99%85%E5%86%9C%E4%B8%9A%E8%88%AA%E7%A9%BA%E" \
               "6%96%BD%E8%8D%AF%E6%8A%80%E6%9C%AF%E8%81%94%E5%90%88%E5%AE%9E%E9%AA%8C%E5%AE%A4"
    web_look = get_access()
    html_url = load_page(web_look, html_url)
    true_url = next_page(html_url)
    news_urls = get_news_urls(load_page(web_look, true_url))
    web_look.quit()
    get_news(news_urls)


if __name__ == '__main__':
    initial()
