import requests

from collections import Counter

import config
from bs4 import BeautifulSoup

HOME = 'https://pikabu.ru/'


def parse_stories(session: requests.sessions.Session, num_of_stories: int):
    tags_counter = Counter()
    id_stories = set()
    i = 1
    paramload = {'page': str(i)}
    complete = False

    while not complete:

        request = session.get(HOME, params=paramload)
        print('request for new page', request.status_code)
        soup = BeautifulSoup(request.text, 'lxml')
        stories = soup.find_all('article', class_='story')

        for i, story in enumerate(stories):
            if story['data-story-id'] not in id_stories:
                id_stories.add(story['data-story-id'])
                print('story id', story['data-story-id'])
                try:
                    tags_str = story.find('div', class_='story__tags tags').text[1:-1]
                    print(tags_str)
                    for tag in tags_str.split(' '):
                        tags_counter[tag] += 1
                except AttributeError:
                    print('story without tags')

                if len(id_stories) == num_of_stories:
                    complete = True
                    break
        print(len(id_stories))

        i += 1
        paramload['page'] = str(i)
    return tags_counter


def make_auth(session):
    url = "https://www.google.com/recaptcha/api2/userverify"

    querystring = {"k": "6Lf5DUsUAAAAAGeOi2l8EpSqiAteDx5PGFMYPkQW"}

    payload = ""
    headers = {
        'origin': "https://www.google.com",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "*/*",
        'cache-control': "no-cache"
    }

    response = session.post(url, data=payload, headers=headers, params=querystring)
    print('google recaptcha status', response.status_code)

    url = "https://pikabu.ru/ajax/auth.php"

    payload = config.data_auth
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'origin': "https://pikabu.ru",
        'x-csrf-token': "ugjimgomredb61ub2b0atr8rso1obcq5",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }

    response = session.post(url, data=payload, headers=headers)

    print('auth code', response.status_code)


def pikabu_parse(home, headers):
    session = requests.Session()
    session.headers = headers

    request = session.get(home)
    print(request.status_code)

    make_auth(session)
    print(parse_stories(session, 50))


if __name__ == '__main__':
    pikabu_parse(HOME, config.GOOGLE_HEADERS)
