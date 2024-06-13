from time import sleep

from bs4 import BeautifulSoup
import requests

from parsers.field_names import titles






to_json_data = []


def get_urls_from_search(page_url, proxy):
    st_accept = "text/html"
    st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    headers = {
        "Accept": st_accept,
        "User-Agent": st_useragent
    }
    response = requests.get(page_url, headers=headers, proxies={
        'http': proxy,
    })
    print(response.status_code, proxy)
    sleep(2)
    text = ''
    bs = BeautifulSoup(response.text, "lxml")
    temp = bs.find_all('a', 'detailsLink', '_blank')
    for a in temp:
        if '/rs/babushkinskij/services/cases/kas/details/' in a['href']:
            text += a['href'] + '\n'

    with open('urls.txt', 'a') as f:
        f.write(text)


def parse_table(page_url, proxy):

    payload = {}
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=1'
    }

    response = requests.request("GET", page_url, headers=headers1, data=payload)
    print(response.status_code, proxy)

    bs = BeautifulSoup(response.text, "lxml")
    temp = bs.find('div', 'detail-cart')
    rows = temp.find_all('div', 'row_card')
    main_info = {}
    for row in rows:
        main_info[titles[" ".join(row.find('div', 'left').text.strip().split())]] = " ".join(row.find('div', 'right').text.strip().split())

    first_page = bs.find(id="tabs-1")
    second_page = bs.find(id="tabs-2")

    for page in [first_page, second_page]:
        table_names = page.find_all('h3')
        parsed_table_names = []
        for name in table_names:
            parsed_table_names.append(" ".join(name.text.strip().split()))

        tables = page.find_all('table', 'custom_table')
        for table, t_name in zip(tables, parsed_table_names):
            parsed_table = []

            rows = table.find_all('tr')
            columns_names = table.find_all('th')
            parsed_names = []
            for name in columns_names:
                parsed_names.append(" ".join(name.text.strip().split()))

            parsed_rows = []
            for row in rows:
                columns = row.find_all('td')
                parsed_columns = []
                for column in columns:
                    parsed_columns.append(" ".join(column.text.strip().split()))
                if parsed_columns:
                    parsed_rows.append(parsed_columns)

            for parsed_row in parsed_rows:
                data = {
                    titles[parsed_names[0]]: parsed_row[0],
                    titles[parsed_names[1]]: parsed_row[1],
                    titles[parsed_names[2]]: parsed_row[2]
                }
                parsed_table.append(data)
            main_info.update({titles[t_name]: parsed_table})

    to_json_data.append(main_info)
