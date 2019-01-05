import requests
from bs4 import BeautifulSoup
from json import dumps
from pprint import pprint

ses = requests.session()


def article_catch(url_list, j):
    articles = []
    for i, item in enumerate(url_list):
        Soup = BeautifulSoup(ses.get(item).text, 'html.parser')
        title = Soup.find('h1', {'class': 'title'}).text
        time = Soup.find('div', {'class': 'post-meta'}).text.split()[0]
        main = Soup.find('div', {'class': 'col_main'})
        image = main.find('img').get('src')
        content = ""
        for par in main.find_all('p'):
            if content != "":
                content = content + '\n' + par.text
            else:
                content = par.text
        dit = {
            'title': title.lstrip(),
            'time': time,
            'image': image,
            'content': content,
        }
        articles.append(dit)
        with open('CivilianArticle{0}.json'.format(j), 'w+') as f:
            f.write(dumps(articles))


url_base = 'http://www.thecivilian.co.nz/page/'
for i in range(1, 21):
    url2scrape = url_base + str(i)
    Soup = BeautifulSoup(ses.get(url2scrape).text, 'html.parser')
    url_list = []
    for item in Soup.find_all('div', {'class': 'post-content'}):
        url_list.append(item.find('a').get('href'))
    pprint(url_list)
    article_catch(url_list, i)
    print('Done:', i)
