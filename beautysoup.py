import json
import re
import time

import requests
from bs4 import BeautifulSoup as bs


def hh_salary_parser(salary: str) -> list:
    """
    function parse headhunter salary string to min, max values and currency
    """
    salary = salary.replace("\u202f", "").replace(" ", "")
    currency = re.findall(r"\D+", salary)[-1]
    money = re.findall(r"\d+", salary)
    min_salary = money[0]
    max_salary = money[-1] if money[-1] != min_salary else "infinity"
    return [min_salary, max_salary, currency]


def hh_parse(target: str, data: list) -> list:
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
            salary = vacancy.find(
                attrs={"data-qa": "vacancy-serp__vacancy-compensation"}
            )
            salary = hh_salary_parser(salary.getText()) if salary else None
            vacancy = vacancy.find("a")
            name = vacancy.getText()
            link = vacancy.get("href")

            parsed_vacancy = {"name": name, "link": link, "source": "hh.ru"}
            if salary:
                parsed_vacancy["salary"] = salary

            parsed_data.append(parsed_vacancy)

        page += 1
        time.sleep(5)
    return data


if __name__ == "__main__":
    parsed_data = []
    hh_parse("Django", parsed_data)
    with open("offers.json", "w") as f:
        json.dump(parsed_data, f, indent=4, ensure_ascii=False)
