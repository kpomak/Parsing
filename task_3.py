import datetime
import json

import requests
from lxml import html


def lenta_ru_parser():

    def paths_handler(link, element, path):
        """
        function adds to dictionary article defined in function lenta_ru_parser
        by key "element" value of Xpaths search result or don't...
        """
        try:
            article[element] = link.xpath(path)[0]
        except Exception:
            pass

    def correct_date():
        """
        function adds date for daily news, when only time is specified
        """
        date = article.get('date')
        if date != None and len(date) < 6:
            article['date'] += f', {current_date}'

    def correct_url(link):
        """
        function changes relative url to absolute
        """
        relative_url = link.xpath('./@href')[0]
        article['link'] = url + relative_url if relative_url.startswith('/') else relative_url 


    current_date = datetime.date.today().strftime('%d %B %Y')
    url = 'https://lenta.ru'
    parsed_data = {url: []}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    }
    paths_list = [    # patterns to find all news blocks on page
        '//div[@class="topnews__column"]//a[contains(@class, "topnews")]',
        '//div[contains(@class, "swiper-slide")]/a',
        '//div[contains(@class, "longgrid")]/a'
    ]
    patterns_dict = { # elements to be parsed and xpats patterns from them
        'title': './/h3[contains(@class, "title")]/text()',
        'body': './/span/text()',
        'date': './/time/text()',
    }

    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)

    links_list = [dom_element for path in paths_list for dom_element in dom.xpath(path)]

    for link in links_list:
        article = {}

        for name, pattern in patterns_dict.items():
            paths_handler(link, name, pattern)

        correct_date()
        correct_url(link)
        parsed_data[url].append(article)
    
    return parsed_data


with open('top_news.json', 'w') as f:
    json.dump(lenta_ru_parser(), f, indent=4, ensure_ascii=False)
