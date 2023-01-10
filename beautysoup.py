import json
import re
import time

import requests
from bs4 import BeautifulSoup as bs


def salary_parser(salary: str) -> list:
    """
    function parse salary string to min, max values and currency
    """
    salary = "".join(salary.split())
    money = re.findall(r"\d+", salary)
    currency = re.findall(r"\D+", salary)[-1]
    min_salary = money[0]
    max_salary = int(money[-1]) if money[-1] != min_salary else "infinity"
    return [int(min_salary), max_salary, currency]


def hh_parse(target: str, data: list) -> list:
    """
    parse hh.ru vacancies searched by target
    and save it to data list
    """
    url = "https://spb.hh.ru/search/vacancy"
    params = {
        "from": "suggest_post",
        "area": "2",
        "text": target,
        "ored_clusters": "true",
        "enable_snippets": "true",
        "hhtmFrom": "vacancy_search_list",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"
    }
    page = 0
    while True:
        params["page"] = page
        response = requests.get(url, headers=headers, params=params)

        soup = bs(response.text, features="lxml")
        vacancies = soup.find_all(class_="vacancy-serp-item-body__main-info")

        if not vacancies:
            break

        for vacancy in vacancies:
            salary_content = vacancy.find(
                attrs={"data-qa": "vacancy-serp__vacancy-compensation"}
            )
            salary = salary_parser(salary_content.getText()) if salary_content else None
            vacancy = vacancy.find("a")
            name = vacancy.getText()
            link = vacancy.get("href")
            _id = re.search(r"\d+", link)[0] + "hh"

            parsed_vacancy = {"name": name, "link": link, "source": "hh.ru", "_id": _id}
            if salary:
                parsed_vacancy["salary"] = salary

            data.append(parsed_vacancy)

        page += 1
        time.sleep(5)
    return data


def sj_parse(target: str, data: list) -> list:
    """
    parse superjob.ru vacancies searched by target
    and save it to data list
    """
    ids = set()
    url = "https://www.superjob.ru/vacancy/search/"
    base_url = "https://spb.superjob.ru"
    params = {
        "geo[t][0]": "14",
        "geo[t][1]": "4",
        "keywords": target,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"
    }
    page = 0
    while True:
        params["page"] = page
        response = requests.get(url, headers=headers, params=params)
        soup = bs(response.text, features="lxml")
        vacancies = soup.find_all(class_="f-test-search-result-item")

        if not vacancies:
            break

        for vacancy in vacancies:
            salary_content = vacancy.find(class_="f-test-text-company-item-salary")
            vacancy = vacancy.find("a")

            # form filter
            if not vacancy:
                continue

            link = vacancy.get("href")

            # advertising filter
            if link.startswith("http"):
                continue

            _id = re.search(r"\d+", link)[0] + "sj"
            if _id in ids:
                continue
            ids.add(_id)

            name = vacancy.getText()
            parsed_vacancy = {
                "name": name,
                "link": base_url + link,
                "source": "spb.superjob.ru",
                "_id": _id,
            }

            if salary_content:
                salary_item = salary_content.span.getText()
                salary = (
                    salary_parser(salary_item)
                    if re.findall(r"\d+", salary_item)
                    else None
                )
                if salary:
                    parsed_vacancy["salary"] = salary
            data.append(parsed_vacancy)
        page += 1
        time.sleep(5)
    return data


if __name__ == "__main__":
    parsed_data = []
    hh_parse("Django", parsed_data)
    sj_parse("Django", parsed_data)

    with open("offers.json", "w") as f:
        json.dump(parsed_data, f, indent=4, ensure_ascii=False)
