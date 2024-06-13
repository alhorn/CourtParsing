import json
from collections import deque
from concurrent.futures import ThreadPoolExecutor

from db_setup import setup_db
from fill_db import fill_db
from parsers.parser import get_urls_from_search, to_json_data, parse_table


def load_proxies():
    with open('Proxy.txt') as f:
        return deque([row.strip() for row in f])


def get_case_urls(proxies, link):
    proxy = proxies.popleft()
    try:
        get_urls_from_search(link, proxy)
    finally:
        proxies.append(proxy)


def get_cases_from_urls(proxies, link):
    proxy = proxies.popleft()
    try:
        parse_table(link, proxy)
    finally:
        proxies.append(proxy)


def get_links():
    with open('urls.txt') as f:
        return [row.strip().replace('/rs/babushkinskij', 'https://mos-gorsud.ru/rs/babushkinskij') for row in f]


def main():
    proxies = load_proxies()

    links = []
    for i in range(1, 68):
        links.append(
            f'https://mos-gorsud.ru/rs/kuzminskij/search?courtAlias=babushkinskij&processType=1&formType=shortForm&page={i}'
        )
    # 1 воркер, так как сайт начинает отдавать 503 при большем количестве
    # тут парсятся ссылки на дела в файл
    with ThreadPoolExecutor(max_workers=1) as pool:
        pool.map(lambda link: get_case_urls(proxies, link), links)

    links = get_links()
    # тут парсятся сами дела в json
    # тут тоже не брал много потоков чтобы сайт не упал
    with ThreadPoolExecutor(max_workers=2) as pool:
        pool.map(lambda link: get_cases_from_urls(proxies, link), links)
    with open('data.json', 'r+', encoding='utf-8') as f:
        json.dump(to_json_data, f, ensure_ascii=False, indent=4)

    # создает бд
    setup_db()

    # наполняет бд файлами
    fill_db()


if __name__ == "__main__":
    main()
