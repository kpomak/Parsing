"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
"""


import json
import requests


url = 'https://api.github.com/users/kpomak/repos'
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "content-type": "text/plain",
    "X-GitHub-Api-Version": "2022-11-28"
    }
response =  requests.get(url, headers=headers)

with open('repos.json', 'w') as f:
    json.dump(response.json(), f, indent=4)
