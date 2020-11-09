# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
from pprint import pprint
import json
main_link = "https://api.github.com"
user = "degtyreva"
response = requests.get(f"{main_link}/users/{user}/repos")
j_data = response.json()
print(response.url)
for el in j_data:
    print(f"Репозиторий {el['name']}")
with open('data.json', 'w') as file:
    json.dump(j_data, file)

# 2. Изучить    список    открытых    API(https: // www.programmableweb.com / category / all / apis).Найти
# среди    них    любое, требующее    авторизацию (любого    типа).Выполнить    запросы    к
# нему, пройдя    авторизацию. Ответ    сервера    записать    в    файл.    Если    нет
# желания    заморачиваться    с    поиском, возьмите    API    вконтакте (https: // vk.com / dev / first_guide).Сделайте
# запрос, чтб    получить    список    всех    сообществ    на    которые    вы    подписаны.


url = 'https://api.vk.com/method/groups.get'
token = '111111'
request_params = {
    'v':'5.52',
    'method':'groups.get',
    'oauth':'1',
    'access_token':token
}
response2 = requests.get(url, params=request_params)
data = response2.json()
with open('data_vc.json', 'w') as f:
     json.dump(data, f)

print(f"Количество сообществ: {data['response']['count']}")
print(data['response']['items'])

