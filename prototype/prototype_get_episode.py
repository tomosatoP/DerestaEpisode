#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup, element
import csv

url: str = "https://gamerch.com/imascg-slstage-wiki/entry/524709"

resp: requests.models.Response = requests.get(url)
html: BeautifulSoup = BeautifulSoup(resp.content, "html.parser")

headlines: list[str] = [
    "センター効果",
    "センター効果説明",
    "特技",
    "特技説明",
    "特技分類",
    "特技発動間隔",
    "入手方法1",
    "入手方法2",
    "特訓前後",
    "ボイス有無",
    "CV",
    "ソロVer有無",
    "実装日",
    "登場機会",
    "プラチナガシャ",
    "ローカルガシャ",
]

talbe_body: element.Tag = html.findAll("tbody")[2]
table_body_elems: element.ResultSet = talbe_body.find_all("td")
datas: list[list[str]] = list()
data: list[str] = list()
for elem in table_body_elems:
    data.append(elem.text)

datas.append(data)

with open(file="csv3.csv", mode="wt") as f:
    writer = csv.writer(f)
    writer.writerow(headlines)
    for data in datas:
        writer.writerow(data)

if __name__ == "__main__":
    print(__file__)
