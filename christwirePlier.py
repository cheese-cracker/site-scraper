import requests
from bs4 import BeautifulSoup
from json import dumps
from pprint import pprint

ses = requests.session()


def article_catch(url_list, j):
    articles = []
    for i, item in enumerate(url_list):
        Soup = BeautifulSoup(ses.get(item).text, 'html.parser')
        article = Soup.find('article')
        title = article.find('h1', {'class': 'entry-title'}).text
        time = article.find('span', {'class': 'entry-meta-date updated'}).text
        try:
            image = article.find('img').get('src')
        except Exception:
            image = None
        written = article.find('div', {'class': 'entry-content mh-clearfix'})
        content = ""
        for par in article.find_all('p'):
            if content != "":
                content = content + '\n' + par.text
            else:
                content = par.text
        dit = {
            'title': title.strip(),
            'time': time,
            'image': image,
            'content': content,
        }
        articles.append(dit)
        with open('ChristwireArticle{0}.json'.format(j), 'w+') as f:
            f.write(dumps(articles))


url_base = 'http://www.christwire.org/page/'
for i in range(1, 3):
    url2scrape = url_base + str(i)
    Soup = BeautifulSoup(ses.get(url2scrape).text, 'html.parser')
    url_list = []
    for item in Soup.find_all('h3'):
        url_list.append(item.find('a').get('href'))
    pprint(url_list)
    article_catch(url_list, i)
    print('Done:', i)
