import requests
from config import HEADERS, HEADRS_MAIN, params, NEXT_PAGE
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json

HOME = 'https://pikabu.ru/'


def pikabu_parse(home, headers):
    session = requests.Session()
    session.headers = headers

    request = session.get(home)
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    print(cookies)

    soup = BeautifulSoup(request.text, 'lxml')
    stories = soup.find_all('header', class_='story__header')
    print(len(stories))
    print(stories[-2])

    paramload = {'twitmode': '1', 'of': 'v2', 'page': '1', '_': cookies['ulfs']}
    request = session.get(home, data=paramload, cookies=cookies)

    print(request.status_code)
    cook2 = requests.utils.dict_from_cookiejar(session.cookies)
    print(cook2)
    soup = BeautifulSoup(request.text, 'lxml')

    stories2 = soup.find_all('header', class_='story__header')
    print(len(stories2))
    print(stories[-2])


if __name__ == '__main__':
    pikabu_parse(HOME, HEADRS_MAIN)
