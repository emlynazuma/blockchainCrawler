from collections import deque
import csv
import requests
from bs4 import BeautifulSoup
import time


baseURL = "https://www.blockchain.com"
blocksURL = "https://www.blockchain.com/btc/blocks"


def get_blocks_pagely(URL):
    response = requests.get(URL).text
    soup = BeautifulSoup(response, features="html.parser")
    result = []

    for i, item in enumerate(soup.findAll('span', text="Height")[1:]):
        result.append([])
        result[i].append(item.parent.nextSibling.text)
    for i, item in enumerate(soup.findAll('span', text="Hash")[1:]):
        result[i].append(item.parent.nextSibling.text)
    for i, item in enumerate(soup.findAll('span', text="Mined")[1:]):
        result[i].append(item.parent.nextSibling.text)
    for i, item in enumerate(soup.findAll('span', text="Miner")[1:]):
        result[i].append(item.parent.nextSibling.text)
    for i, item in enumerate(soup.findAll('span', text="Size")[1:]):
        result[i].append(item.parent.nextSibling.text)
    for i, item in enumerate(soup.findAll('span', text="Height")[1:]):
        result[i].append(baseURL + item.parent.nextSibling.a['href'])
    return result


def get_blocks(page: int):
    result = []
    for p in range(1, page + 1):
        URL = f"{blocksURL}?page={p}"
        result.extend(get_blocks_pagely(URL))
    return result


def get_fee_pagely(URL: str):
    response = requests.get(URL).text
    soup = BeautifulSoup(response, features="html.parser")
    result = []
    for item in soup.findAll('span', text="Fee"):
        result.append(float(item.parent.nextSibling.span.text.split(" ")[0]))
    return result


def get_fee(baseURL: str, page: int):
    result = []
    for p in range(1, page + 1):
        URL = f"{baseURL}?page={p}"
        result.extend(get_fee_pagely(URL))
    return result


if __name__ == "__main__":
    res = get_blocks(1)
    d = deque(res)

    title = ["height", "hash", "mined", "miner", "size", "linkOfSubPage", "timestamp", "avgFee"]
    with open("result.csv", "a+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerow(title)

    while len(d) != 0:
        block = d.pop()
        block_url = block[-1]
        fee = get_fee(block_url, 5)
        block.append(int(time.time()))
        avg_fee = sum(fee) / len(fee)
        block.append(avg_fee)
        with open("result.csv", "a+") as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerow(block)
