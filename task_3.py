import requests
from pprint import pprint

from lxml import html

url = 'https://lenta.ru'




headers = {

'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}

response = requests.get(url,  headers=headers)
dom = html.fromstring(response.text)

time = dom.xpath("current-date()")
print(time)

paths_list = [
    '//div[@class="topnews__column"]//a[contains(@class, "topnews")]',
    '//div[contains(@class, "swiper-slide")]/a',
    '//div[contains(@class, "longgrid")]/a'
]

links_list = [dom_element for path in paths_list for dom_element in dom.xpath(path)]



parsed_data = {url: []}

for link in links_list:
    article = {}

    try:
        article['title'] = link.xpath('.//h3[contains(@class, "title")]/text()')[0]
    except Exception:
        pass
    
    try:
        article['body'] = link.xpath('.//span/text()')[0]
    except Exception:
        pass

    try:
        article['date'] = link.xpath('.//time/text()')[0]
    except Exception:
        pass



    relative_url = link.xpath('./@href')[0]
    article['link'] = url + relative_url if relative_url.startswith('/') else relative_url


    parsed_data[url].append(article)


# pprint(parsed_data)
