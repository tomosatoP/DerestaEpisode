#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import episode

url1: str = "https://gamerch.com/imascg-slstage-wiki/entry/516012"
csv1: str = "data_idols.csv"
csv2: str = "data_episodes.csv"


if __name__ == "__main__":
    print(__file__)

    idols = episode.table_idollist(url=url1)
    idol_urls: list = list(map(lambda x: x[1], idols.records()))
    idols.duplicate(csvfilename=csv1)

    for idol_url in idol_urls:
        if not idol_url == "-":
            episodes = episode.table_episodelist(url=idol_url)
            episodes.duplicate(csvfilename=csv2)
