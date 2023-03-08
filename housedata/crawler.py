#!/usr/bin/env python3

import time
import json

import requests
from bs4 import BeautifulSoup

from logger import logger
from constants import (
    API_URL, ROOT_URL, CONDITIONS, WEB_URL_FORMAT_STR, HEADERS,
    PARSE_INTERVAL_IN_SECONDS, MAP_URL_FORMAT_STR
)

cache = set()


class CrawlControl:
    def __init__(self):
        self.is_crawler_looping = True


crawler1 = CrawlControl()


def get_houses(session):
    logger.info('requests 591 API... ')
    logger.info(CONDITIONS['regionid'])
    if CONDITIONS['regionid'] == 3:
        CONDITIONS['section'] = "43,50,38,37,44,34,47"
    else:
        CONDITIONS.pop('section', None)

    response = session.get(API_URL, params=CONDITIONS)
    logger.info('API_URL' + API_URL)
    try:
        json = response.json()
        data = json['data']
    except KeyError:
        logger.debug("response.json()['data']: {}".format(response.json()['data']))
        logger.error("Cannnot get data from response.json['data']")
    except Exception:
        logger.debug("response: {}".format(response.text))
        raise
    else:
        houses = data.get('data', [])
        logger.info("receive {} datas".format(len(houses)))
        # if data number less than 30 means this regionid's data is use up, fetch next one
        # link to check region id mapping
        # https://github.com/g0v/tw-rental-house-data/blob/master/crawler/crawler/spiders/all_591_cities.py
        if len(houses) < 30:
            if CONDITIONS['kind'] < 2: # try 獨立套房: 1, 分租套房: 2
                CONDITIONS['kind'] += 1
            else:
                CONDITIONS['firstRow'] = 0
                CONDITIONS['regionid'] += 2
                CONDITIONS['kind'] = 1
        if CONDITIONS['regionid'] >= 5: # we only want 台北市 1, 新北市 3
            crawler1.is_crawler_looping = False
            logger.info("crawling stop + {}".format(crawler1.is_crawler_looping))

        for house in houses:
            yield house


def log_house_info(house):
    logger.info(
        "名稱：{}-{}-{}".format(
            house['region_name'],
            house['section_name'],
            house['fulladdress'],
        )
    )
    # logger.info("網址：{}".format(WEB_URL_FORMAT_STR.format(house['post_id'])))
    # logger.info("租金：{} {}".format(house['price'], house['unit']))
    # logger.info("坪數：{} 坪".format(house['area']))
    # logger.info("格局：{}".format(house['layout']))
    # logger.info("更新時間：{}".format(time.ctime(house['refreshtime'])))
    # logger.info("\n")


def search_houses(session):
    houses = get_houses(session)
    for house in houses:
        if house['post_id'] in cache:  # post id is unique for every house posted on 591
            continue

        log_house_info(house)
        save_house(session, house)
        cache.update([house['post_id']])


def save_house(session, house):
    if house['floor'] <= 1:  # filter house contains unwanted floor (ex. 1F, B1)
        return
    raw = {
        "houseId": house['id'],
        "userId": house['user_id'],
        "type": house['type'],
        "kind": house['kind'],
        "postId": house['post_id'],
        "regionId": house['regionid'],
        "regionName": house['regionname'],
        "sectionName": house['sectionname'],
        "sectionId": house['sectionid'],
        "streetId": house['streetid'],
        "streetName": house['street_name'],
        "alleyName": house['alley_name'],
        "caseName": house['cases_name'],
        "caseId": house['cases_id'],
        "layout": house['layout'],
        "room": house['room'],
        "area": house['area'],
        "floor": house['floor'],
        "allFloor": house['allfloor'],
        "updateTime": house['updatetime'],
        "condition": house['condition'],
        "cover": house['cover'],
        # "refreshTime":house['refreshtime'],
        "closed": house['closed'],
        "kindName": house['kind_name'],
        "iconClass": house['icon_class'],
        "fullAddress": house['fulladdress']
    }
    target = MAP_URL_FORMAT_STR.format(raw['houseId'])
    res = session.get(target)
    get_price = house['price']
    is_string = isinstance(get_price, str)
    if is_string:
        raw['price'] = int(get_price.replace(',', ""))
    else:
        raw['price'] = get_price

    html = res.content
    soup = BeautifulSoup(html, "html.parser")

    raw["coordinateX"] = soup.find(id="lng").get('value') if soup.find(id="lng") else ""
    raw["coordinateY"] = soup.find(id="lat").get('value') if soup.find(id="lat") else ""

    json_body = json.dumps(raw)
    # TODO insert into DB
    # TODO decide need house and notify Telegram if success
    time.sleep(0.3)


def set_csrf_token(session):
    r = session.get(ROOT_URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    token_item = soup.select_one('meta[name="csrf-token"]')
    session.headers = HEADERS
    session.headers['X-CSRF-TOKEN'] = token_item.get('content')


def main():
    session = requests.Session()

    while crawler1.is_crawler_looping:
        set_csrf_token(session)
        search_houses(session)
        time.sleep(PARSE_INTERVAL_IN_SECONDS)
        CONDITIONS['firstRow'] += 30
        print(CONDITIONS['firstRow'])


if __name__ == "__main__":
    main()
