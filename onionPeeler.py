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
        title = article.find('h1')
        time = article.find('time')
        pict = article.find('picture')
        content = ""
        for par in article.find_all('p'):
            if content != "":
                content = content + '\n' + par.text
            else:
                content = par.text
        try:
            image = pict.find('img').get('src')
        except AttributeError or TypeError:
            image = None
        dit = {
            'title': title.text,
            'time': time.get('datetime'),
            'image': image,
            'content': content
        }
        articles.append(dit)
        with open('OnionArticle{0}.json'.format(j), 'w+') as f:
            f.write(json.dumps(articles))


url2scrape = 'https://www.theonion.com'
for i in range(2):
    Soup = BeautifulSoup(ses.get(url2scrape).text, "html.parser")
    url_list = []
    for article in Soup.find_all('article'):
        head = article.find('h1')
        url_list.append(head.find('a', {'class': "js_entry-link"}).get('href'))

    pprint(url_list)
    article_catch(url_list, i)
    btn = Soup.find('div', {'class': 'load-more__button'})
    url2scrape = "https://www.theonion.com" + btn.find('a').get('href')
