import requests
from bs4 import BeautifulSoup
from json import dumps
from pprint import pprint

ses = requests.session()


def article_catch(url_list, j):
    articles = []
    for i, item in enumerate(url_list):
        Soup = BeautifulSoup(ses.get(item).text, 'html.parser')
        title = Soup.find('h2').text
        time = Soup.find('time').text
        pictimage = Soup.find('div', {'class': 'fullstory lfi'})
        try:
            image = pictimage.find('img').get('src')
        except Exception:
            image = None
        content_part = Soup.find(id='post-content')
        content = ""
        for par in content_part.find_all('p'):
            if content != "":
                content = content + '\n' + par.text
            else:
                content = par.text
        dit = {
            'title': title.strip(),
            'time': time.strip(),
            'image': image,
            'content': content,
        }
        articles.append(dit)
        with open('DailyMashArticles{0}.json'.format(j), 'w+') as f:
            f.write(dumps(articles))


for i in range(1, 99):
    url2scrape = 'https://thedailymash.co.uk/page/{0}?s'.format(i)
    Soup = BeautifulSoup(ses.get(url2scrape).text, 'html.parser')
    url_list = []
    for item in Soup.find_all('div', {'class': 'holder'}):
        url_list.append(item.find('a').get('href'))
    pprint(url_list)
    article_catch(url_list, i)
    print('Done:', i)
