from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests
import re


def salary_parser(salary: str) -> tuple:
    salary = salary.replace('\u202f', '').replace(' ', '')
    currency = re.findall(r'\D+', salary)[-1]
    money = re.findall(r'\d+', salary)
    min_salary = money[0]
    max_salary = money[-1] if money[-1] != min_salary else 'infinity'
    return min_salary, max_salary, currency


def hh_parse(target: str, data: dict) -> dict:
    url = "https://spb.hh.ru/search/vacancy"
    source = "hh.ru"
    params = {
        "from": "suggest_post",
        "area": "2",
        "text": target,
        "hhtmFrom": "vacancy_search_list",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"
    }
    page = 0

    params["page"] = page

    response = requests.get(url, headers=headers, params=params)
    soup = bs(response.text, features="lxml")
    vacancys = soup.find_all(class_="vacancy-serp-item-body")

    for vacancy in vacancys:
        salary = vacancy.find(attrs={'data-qa':"vacancy-serp__vacancy-compensation"})
        *salary, = salary_parser(salary.getText()) if salary else ''
        vacancy = vacancy.find("a")
        name = vacancy.getText()
        link = vacancy.get("href")

    return data

parsed_data = {}

hh_parse("python", parsed_data)
