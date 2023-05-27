#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup, element
import csv

url: str = "https://gamerch.com/imascg-slstage-wiki/entry/516012"

res: requests.models.Response = requests.get(url)
html: BeautifulSoup = BeautifulSoup(res.content, "html.parser")

table_head: element.Tag = html.findAll("thead")[1]
table_head_elems: element.ResultSet = table_head.find_all("th")
# <th class="mu__talbe--col16">実装日</th>
# ,名前,年齢,誕生日,星座,血液型,身長,体重,B,W,H,利き手,出身地,趣味,CV,実装日
# 1列目の見出しを 'type' にし、2列目に 'address' を挿入
headlines: list = list()
for elem in table_head_elems:
    headlines.append(elem.text)
headlines[0] = "type"
headlines.insert(1, "idol_url")

table_body: element.Tag = html.findAll("tbody")[1]
table_body_rows: element.ResultSet = table_body.find_all("tr")
# <td class="mu__table--col1" style="background-color:#fbc">**</td>
# <td class="mu__table--col2"><a href="https://***">***</a></td>
# <td class="mu__table--col16">YYYY/MM/DD</td>

datas: list[list[str]] = list()
for row in table_body_rows:
    # row: element.Tag
    data: list[str] = list()
    for cell in row.findAll("td"):
        # cell: element.Tag
        if cell["class"] == ["mu__table--col2"]:
            data.append(cell.a["href"]) if cell.a else data.append("-")
        data.append(cell.text)
    datas.append(data)


with open(file="csv1.csv", mode="wt") as f:
    writer = csv.writer(f)
    writer.writerow(headlines)
    for data in datas:
        writer.writerow(data)

if __name__ == "__main__":
    print(__file__)
