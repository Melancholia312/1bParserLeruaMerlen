import json
import random
import time

import requests
from bs4 import BeautifulSoup
import csv

cookies = {
    '_slid_server': '',
    'ggr-widget-test': '0',
    '_ym_uid': '1688029203740152408',
    '_ym_d': '1688029203',
    'cookie_accepted': 'true',
    'tmr_lvid': 'ee8f4936be6e8bb0dd24f034c55e3fae',
    'tmr_lvidTS': '1688029203475',
    'iap.uid': 'e7fd78c58c2a409884c4507001de9e1a',
    'uxs_uid': '560f43a0-165b-11ee-82ce-e1d9caf0949e',
    'aplaut_distinct_id': 'Zcv8yCiVaiyt',
    '_gid': 'GA1.2.639592769.1688029205',
    '_gaexp': 'GAX1.2.cvwgp_Y9T9epcDxlhE2dNA.19595.1!3-f7YYJVSuWAe60Jb0RbSg.19616.x503!pg6Iz5B9QGu0NOrfm08tNw.19607.1',
    '_preselectTariff': 'true',
    'sawOPH': 'true',
    '_reactCheckout': 'true',
    '_b2bCheckout3': 'true',
    '_ym_isad': '1',
    'GACookieStorage': 'GA1.2.1630616458.1688029203',
    '_ym_visorc': 'b',
    'X-API-Experiments-sub': 'B',
    '_regionID': '3439',
    'qrator_jsid': '1688104821.568.fItITMc4BEB9v75w-0i4tjbs5vbtmsq99qpudcuhj60c4bssc',
    '_ga': 'GA1.2.1630616458.1688029203',
    '_gat_UA-20946020-1': '1',
    '_ga_Z72HLV7H6T': 'GS1.1.1688104941.3.1.1688107275.0.0.0',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    # 'Cookie': '_slid_server=; ggr-widget-test=0; _ym_uid=1688029203740152408; _ym_d=1688029203; cookie_accepted=true; tmr_lvid=ee8f4936be6e8bb0dd24f034c55e3fae; tmr_lvidTS=1688029203475; iap.uid=e7fd78c58c2a409884c4507001de9e1a; uxs_uid=560f43a0-165b-11ee-82ce-e1d9caf0949e; aplaut_distinct_id=Zcv8yCiVaiyt; _gid=GA1.2.639592769.1688029205; _gaexp=GAX1.2.cvwgp_Y9T9epcDxlhE2dNA.19595.1!3-f7YYJVSuWAe60Jb0RbSg.19616.x503!pg6Iz5B9QGu0NOrfm08tNw.19607.1; _preselectTariff=true; sawOPH=true; _reactCheckout=true; _b2bCheckout3=true; _ym_isad=1; GACookieStorage=GA1.2.1630616458.1688029203; _ym_visorc=b; X-API-Experiments-sub=B; _regionID=3439; qrator_jsid=1688104821.568.fItITMc4BEB9v75w-0i4tjbs5vbtmsq99qpudcuhj60c4bssc; _ga=GA1.2.1630616458.1688029203; _gat_UA-20946020-1=1; _ga_Z72HLV7H6T=GS1.1.1688104941.3.1.1688107275.0.0.0',
    'Origin': 'https://saratov.leroymerlin.ru',
    'Referer': 'https://saratov.leroymerlin.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-api-key': 'Yeg8l3zQDwpVNBDTP3q6jM4lQVLW5TTv',
    'x-request-id': 'b12249ae1c75fb41716b1610ad6ab370',
}

json_data = {
    'familyIds': [],
    'limit': 30,
    'regionId': '3439',
    'facets': [],
    'suggest': True,
    'offset': 0,
    'customerId': 'GA1.2.1630616458.1688029203',
    'parentFamilyId': None,
    'searchMethod': 'DEFAULT',
}


BASE_URL = 'https://api.leroymerlin.ru/hybrid/v1/getProducts'

CATEGORIES = {
    'Краски Для Внутренних Работ': ['7d0e80e0-4672-11ea-b9e6-8d2ee1855ff8'],
    'Электроинструменты': ["37097a00-475d-11ea-a27c-5dbb3eb10c3c"],
    'Водонагреватели': ['90f9bd40-48e8-11ea-9e76-ef66c83887c3_Opus_Family']
}


def get_json(url):
    time.sleep(random.randint(5, 8))
    r = requests.post(url, cookies=cookies, headers=headers, json=json_data)
    if r.status_code == 200:
        return r.json()
    else:
        return "ERROR"


def get_all_goods():
    all_goods = {}
    json = get_json(BASE_URL)
    while json != "ERROR" and len(json.get('content')) != 0:
        for good in json.get('content'):
            all_goods[good['displayedName']] = good['price']['main_price']
        json_data['offset'] += 30
        json = get_json(BASE_URL)

    return all_goods


def write_to_csv():
    records = get_all_goods()

    with open('products.csv', 'w', encoding='UTF8') as f:
        w = csv.DictWriter(f, records.keys())
        w.writeheader()
        w.writerow(records)


def ui():
    print('Категории: ' + ', '.join(CATEGORIES.keys()))
    user_category = input("Введите название категории: ").title()
    if user_category not in CATEGORIES.keys():
        print("Такой категории нет")
        return

    print("Идет подготовка вашего файла. Пожалуйста, подождите...")
    json_data["familyIds"] = CATEGORIES[user_category]
    write_to_csv()
    print("Готово")


ui()
