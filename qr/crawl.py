import sys
import requests
from bs4 import BeautifulSoup


class Crawl:

    def __init__(self, url):
        self._url = url

    def crawl(self, soupbase):
        html = requests.get(self._url).text
        soup = BeautifulSoup(html, 'lxml')
        elements = soupbase(soup)
        return elements


def main(url: str):
    crawler = Crawl(url)

    def soupbase(soup):
        title = soup.find('title').string
        return (title,)

    try:
        elements = crawler.crawl(soupbase)
        data = '\n'.join(elements)
        sys.stdout.write(data)
    except Exception as e:
        print(e)
        sys.stderr.write('An error occurred.')


if __name__ == '__main__':
    url = sys.argv[1]
    main(url)
