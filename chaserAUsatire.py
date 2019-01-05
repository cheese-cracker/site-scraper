import requests
from bs4 import BeautifulSoup
from json import dumps
from pprint import pprint

ses = requests.session()


def article_catch(url_list, j):
    articles = []
    for i, item in enumerate(url_list):
        Soup = BeautifulSoup(ses.get(item).text, 'html.parser')
        title = Soup.find('div', {'class': 'title_title'}).text
        time = Soup.find('time', {'class': 'entry-date'}).text
        image = Soup.find('img', {'class': 'feature-image'}).get('src')
        article = Soup.find('article')
        for script in article(['script']):
            script.extract()
        content = ""
        for par in article.find_all('p'):
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
        with open('ChaserArticle{0}.json'.format(j), 'w+') as f:
            f.write(dumps(articles))


url_base = 'https://chaser.com.au/news/page/'
for i in range(1, 21):
    url2scrape = url_base + str(i)
    Soup = BeautifulSoup(ses.get(url2scrape).text, 'html.parser')
    url_list = [item.get('href') for item in Soup.find_all('a', {'class': 'archive_story'})]
    pprint(url_list)
    article_catch(url_list, i)
    print('Done:', i)
