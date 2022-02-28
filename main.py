import requests
import time
import json
from urllib.parse import urlparse
from publicsuffixlist import PublicSuffixList
from IPy import IP


def get_timestamp():
    url = "https://data.miningpoolstats.stream/data/time?t={}"
    payload = {}
    headers = {
        'authority': 'data.miningpoolstats.stream',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'sec-gpc': '1',
        'origin': 'https://miningpoolstats.stream',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://miningpoolstats.stream/',
        'accept-language': 'en,en-US;q=0.9'
    }

    response = requests.request("GET", url.format(int(time.time())), headers=headers, data=payload)

    return int(response.text)


def get_coins():
    url = "https://data.miningpoolstats.stream/data/coins_data.js?t={}"

    payload = {}
    headers = {
        'authority': 'data.miningpoolstats.stream',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'sec-gpc': '1',
        'origin': 'https://miningpoolstats.stream',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://miningpoolstats.stream/',
        'accept-language': 'en,en-US;q=0.9'
    }

    response = requests.request("GET", url.format(get_timestamp()), headers=headers, data=payload)

    coins_data = json.loads(response.text)
    coins = []
    # print(json.dumps(coins_data, indent=4, sort_keys=True))
    for coin_data in coins_data['data']:
        coins.append(coin_data['page'])
    return coins


def get_pools(page='ethereum'):
    print('processing: {}...'.format(page))

    url = "https://data.miningpoolstats.stream/data/{}.js?t={}"

    payload = {}
    headers = {
        'authority': 'data.miningpoolstats.stream',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'sec-gpc': '1',
        'origin': 'https://miningpoolstats.stream',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://miningpoolstats.stream/',
        'accept-language': 'en,en-US;q=0.9'
    }

    response = requests.request("GET", url.format(page, get_timestamp()), headers=headers, data=payload)

    pools_data = json.loads(response.text)
    pools = []
    # psl = PublicSuffixList()
    if 'data' in pools_data:
        for pool_data in pools_data['data']:
            # parse_result = urlparse(pool_data['url'])
            # domain = psl.privatesuffix(parse_result.netloc)
            # pools.append(domain)
            pools.append(pool_data['url'])
    return pools


def save_pools(pool_list):
    with open('pools.txt', 'a') as f:
        f.write('\n'.join(pool_list) + '\n')


def is_ip(address):
    try:
        IP(address)
        return True
    except Exception as e:
        return False


def clean_pools_data():
    raw = []
    psl = PublicSuffixList()
    with open('pools.txt', 'r') as f:
        for line in f:
            text = line.strip('\n')
            parse_result = urlparse(text)
            domain = parse_result.hostname.__str__()
            if is_ip(domain):
                # raw.append(domain)
                pass
            else:
                domain = psl.privatesuffix(parse_result.hostname.__str__())
                if domain is not None:
                    raw.append(domain)
    cleaned = list(set(raw))
    cleaned.sort()
    with open('pools_cleaned_domain.txt', 'a') as f:
        f.write('\n'.join(cleaned) + '\n')
    print(cleaned)


if __name__ == '__main__':
    # c = get_coins()
    # coin_count = len(c)
    # for idx, page in enumerate(c):
    #     print('{}/{}'.format(idx + 1, coin_count))
    #     p = get_pools(page)
    #     save_pools(p)
    clean_pools_data()
