#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup, element
import csv

url: str = "https://gamerch.com/imascg-slstage-wiki/entry/517369"

resp: requests.models.Response = requests.get(url)
html: BeautifulSoup = BeautifulSoup(resp.content, "html.parser")

table_head: element.Tag = html.findAll("thead")[1]
table_heaa_elems: element.ResultSet = table_head.find_all("th")
# 画像,エピソード名,レア,実装日,登場機会
# 2列目に 'address' を挿入
headlines: list = list()
for elem in table_heaa_elems:
    headlines.append(elem.text)
headlines.insert(1, "address")

table_body: element.Tag = html.findAll("tbody")[1]
table_body_rows: element.ResultSet = table_body.find_all("tr")

datas: list[list[str]] = list()
for row in table_body_rows:
    # row: element.Tag
    data: list[str] = list()
    for cell in row.findAll("td"):
        # cell: element.Tag
        match cell["class"][0]:
            case "mu__table--col1":
                # source: data-srcset[1x, 2x, 3x], srcset, type="image/webp"
                # source: data-srcset[1x, 2x, 3x], srcset, type="image/png"
                # img: alt, data-src, height, src, width
                webp_url: str = cell.findAll("source")[0]["data-srcset"].rsplit(",")[-1]
                data.append(webp_url.strip().split()[0])
            case "mu__table--col2":
                data.append(cell.a["href"]) if cell.a else data.append("-")
                data.append(cell.text.translate(str.maketrans("［］", "[]")))
            case _:
                data.append(cell.text)
    if data[3] in ["SR", "SSR"]:
        # N,R にはエピソードが無いので省略
        resp = requests.get(data[0])
        with open(file=f"{data[3]}{data[2]}.png", mode="wb") as f:
            f.write(resp.content)
        datas.append(data)

with open(file="csv2.csv", mode="wt") as f:
    writer = csv.writer(f)
    writer.writerow(headlines)
    for data in datas:
        writer.writerow(data)

if __name__ == "__main__":
    print(__file__)
