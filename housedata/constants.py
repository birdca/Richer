ROOT_URL = "https://rent.591.com.tw"
API_URL = "https://rent.591.com.tw/home/search/rsList"
MAP_URL_FORMAT_STR = ROOT_URL + "/map-houseRound.html?type=1&post_id={}&s=j_edit_maps&version=1"

HEADERS = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en-US,en;q=0.9",
    'connection': "keep-alive",
    'dnt': "1",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'
}

CONDITIONS = {
    'is_new_list': '1',
    'type': '1',
    'kind': 1,  # 獨立套房: 1, 分租套房: 2
    # 'shape': '2',  # 公寓	1, 電梯大樓	2
    'searchtype': '1',
    'regionid': 1,  # 台北市 1, 新北市 3
    'area': '7,40',
    'rentprice': '4000,13000',
    'hasimg': '1',
    'not_cover': '1'
    , 'firstRow': 0
}

WEB_URL_FORMAT_STR = "https://rent.591.com.tw/rent-detail-{}.html"

CRAWL_LIST_INTERVAL_IN_SECONDS = 5
NEXT_CRAWL_INTERVAL_IN_SECONDS = 600  # we wait 10 minutes to start next crawl
