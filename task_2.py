"""
2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему,
пройдя авторизацию. Ответ сервера записать в файл.
Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide).
Сделайте запрос, чтобы получить список всех сообществ на которые вы подписаны.
"""


import json
import requests

import secret


url =f'https://api.vk.com/method/groups.get'
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0",
    }
params = {
    'user_id': secret.user_id,
    'extended': '1',
    'access_token': secret.token,
    'v': '5.131'
    }

response = requests.get(url, params=params, headers=headers)

with open('groups.json', 'w') as f:
    json.dump(response.json(), f, indent=4)

