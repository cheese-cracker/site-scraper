import requests
import re
import json
from pprint import pprint
from bs4 import BeautifulSoup

session = requests.session()


def article_catch(url_list, i):
    articles = []
    for linkD in url_list:
        article_url = "https://www.newyorker.com"+linkD
        article_page = session.get(article_url)
        Soup = BeautifulSoup(article_page.text, "html.parser")
        time = Soup.find('p', {"class": "ArticleTimestamp__timestamp___1klks "}).text
        main_part = Soup.find(id='articleBody')
        content = ""
        for par in main_part.find_all('p'):
            if content != "":
                content = content + '\n' + par.text
            else:
                content = par.text
        pictimage = Soup.find('picture', {'class': 'component-responsive-image'})
        image = pictimage.find('img').get('src')
        title = Soup.find('h1').text
        dit = {
                'title': title,
                'time': time,
                'content': content,
                'image': image,
        }
        articles.append(dit)
    with open('BorowitzArticles{0}.json'.format(i), 'w+') as f:
        f.write(json.dumps(articles))


def runCityScape():
    url_href_type = re.compile("/humor/borowitz-report/.+")
    for i in range(1, 10):
        url_list = []
        url2scrape = "https://www.newyorker.com/humor/borowitz-report/page/" + str(i)
        Soup = BeautifulSoup(session.get(url2scrape).text, "html.parser")
        # url_class_type = re.compile("Link__link___3dWa\s+")
        for item in Soup.find_all('a', {"href": url_href_type}):
            linkD = item.get('href')
            if linkD not in url_list and '/page/' not in linkD:
                url_list.append(linkD)
        print(i, 'done')
        # with open(file_name, 'w') as final_file:
            # final_file.write(json.dumps(result_set))
        # print("FILE: "+file_name)
        pprint(url_list)
        article_catch(url_list, i)


runCityScape()
