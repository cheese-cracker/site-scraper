# Note: This is year-wise unlike the other webcrawlers!
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json


ses = requests.session()


def article_catch(url_list, j):
    articles = []
    for i, url in enumerate(url_list):
        Soup = BeautifulSoup(ses.get(url).text, "html.parser")
        # title = Soup.find('h1')
        article = Soup.find('article')
        title = article.find('h1', {'class': 'entry-title'})
        time_part = article.find('span', {'class': 'entry-meta-date updated'})
        fig = article.find('figure')
        content_div = article.find('div', {'class': 'entry-content clearfix'})
        content = ""
        for par in content_div.find_all('p'):
            if content != "":
                content = content + '\n' + par.text
            else:
                content = par.text
        try:
            image = fig.find('img').get('src')
        except AttributeError or TypeError:
            image = None
        dit = {
            'title': title.text,
            'time': time_part.find('a').text,
            'image': image,
            'content': content
        }
        articles.append(dit)
        with open('DailyBonnet{0}.json'.format(j), 'w+') as f:
            f.write(json.dumps(articles))


url_base = 'https://www.dailybonnet.com/2018/page'
for i in range(90):
    url2scrape = url_base + '/' + str(i+1)
    Soup = BeautifulSoup(ses.get(url2scrape).text, "html.parser")
    titl = Soup.find('title').text
    if "Daily" not in titl:
        print('page', i+1)
        break
    url_list = []
    for article in Soup.find_all('article'):
        head = article.find('h3', {'class': 'entry-title mh-posts-list-title'})
        url_list.append(head.find('a').get('href'))

    pprint(url_list)
    article_catch(url_list, i)
    print(i, "Done")
