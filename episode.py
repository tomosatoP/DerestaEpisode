#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, element
from time import time, sleep
from pathlib import Path
import requests
import logging
import csv


_last_time: float = 0.0
t_table = str.maketrans("［］", "[]", "＋")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
logger_sh = logging.StreamHandler()
logger_sh.setFormatter(logger_formatter)
logger.addHandler(logger_sh)


class EpisodeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        logger.error(f"Episode: {args}")


class _url_content:
    def __init__(self, url: str) -> None:
        while not self._wait():
            pass
        response: requests.models.Response = requests.get(url=url)
        self._content: bytes = response.content
        logger.info(f"Episode: Request to {url}")

    def _wait(self) -> bool:
        global _last_time
        while time() - _last_time < 1.0:
            sleep(0.1)
        _last_time = time()
        return True


class url_image(_url_content):
    def __init__(self, url: str) -> None:
        super().__init__(url=url)

    def save(self, filename: str) -> int:
        with open(file=f"image/{filename}", mode="wb") as f:
            return f.write(self._content)


class _url_table(_url_content):
    def __init__(self, url: str, index: int) -> None:
        super().__init__(url=url)
        self.index = index
        self.html: BeautifulSoup = BeautifulSoup(self._content, "html.parser")

    def headlines(self) -> list[str]:
        thead: element.Tag = self.html.findAll("thead")[self.index]
        return list(map(lambda x: x.text, thead.find_all("th")))

    def records(self) -> list[list[str | element.Tag]]:
        result: list[list[str | element.Tag]] = list()

        tbody: element.Tag = self.html.findAll("tbody")[self.index]
        for trow in tbody.find_all("tr"):
            # trow: element.ResultSet
            result.append(trow.findAll("td"))
        return result


class table_idollist(_url_table):
    def __init__(self, url: str) -> None:
        super().__init__(url=url, index=1)

    def duplicate(self, csvfilename: str) -> list:
        result: list = list()
        replica: list = list()

        if not Path(csvfilename).exists():
            raise EpisodeError(f"File not found - {csvfilename}.")

        with open(file=csvfilename, mode="rt") as f:
            replica = list(csv.DictReader(f))

        eval("self.headlines()")
        replica_names: list = list(map(lambda x: x["名前"], replica))
        for record in self.records():
            if not record[2] in replica_names:
                with open(file=csvfilename, mode="at") as f:
                    csv_f = csv.writer(f)
                    csv_f.writerow(record)
                result.append(record[1])

        logger.info(f"Episode: Added {len(result)} idols.")
        return result

    def headlines(self) -> list[str]:
        # type, idol_url, 名前, 年齢, 誕生日, 星座, 血液型, 身長, 体重, B, W, H, 利き手, 出身地, 趣味, CV, 実装日
        result = super().headlines()
        if not result == [
            "",
            "名前",
            "年齢",
            "誕生日",
            "星座",
            "血液型",
            "身長",
            "体重",
            "B",
            "W",
            "H",
            "利き手",
            "出身地",
            "趣味",
            "CV",
            "実装日",
        ]:
            raise EpisodeError("Headlines did not match.")

        result[0] = "type"
        result[1:1] = ["idol_url"]
        return result

    def records(self) -> list[list[str | element.Tag]]:
        result: list[list] = list()
        for row in super().records():
            field: list[str] = list()
            for cell in row:
                # cell: element.Tag
                if isinstance(cell, element.Tag):
                    match cell["class"][0]:
                        case "mu__table--col2":
                            if cell.a:
                                field.append(cell.a["href"])
                            else:
                                field.append("-")
                            field.append(cell.text)
                        case _:
                            field.append(cell.text)
            result.append(field)
        return result


class _table_episode(_url_table):
    def __init__(self, url: str) -> None:
        super().__init__(url=url, index=2)

    def headlines(self) -> list[str]:
        return [
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

    def records(self) -> list[list[str | element.Tag]]:
        # result: list[list[str | element.Tag]]
        result = [list(x) for x in zip(*super().records())]
        for i in range(len(result[0])):
            # result[0][i]: element.Tag
            result[0][i] = result[0][i].text.translate(t_table)
        return result


class table_episodelist(_url_table):
    def __init__(self, url: str) -> None:
        super().__init__(url=url, index=1)

    def duplicate(self, csvfilename: str) -> list:
        result: list = list()
        replica: list = list()

        if not Path(csvfilename).exists():
            raise EpisodeError(f"File not found - {csvfilename}.")

        with open(file=csvfilename, mode="rt") as f:
            replica = list(csv.DictReader(f))

        eval("self.headlines()")
        replica_urls: list = list(map(lambda x: x["episode_url"], replica))
        for record in self.records():
            if not record[1] in replica_urls:
                episode = _table_episode(url=str(record[1]))
                eval("episode.headlines()")
                with open(file=csvfilename, mode="at") as f:
                    csv_f = csv.writer(f)
                    csv_f.writerow(record + episode.records()[0])
                result.append(record[1])
                image = url_image(url=str(record[0]))
                image.save(
                    filename=f"{str(record[3]).translate(t_table)}{str(record[2])}.png"
                )

        logger.info(f"Episode: Added {len(result)} episodes.")
        return result

    def headlines(self) -> list[str]:
        # 画像, episode_url, エピソード名, レア, 実装日, 登場機会
        # 矢口美羽のみ: 画像, episode_url, エピソード名, レア, 実装日, 分類
        result = super().headlines()
        if not any(
            [
                result == ["画像", "エピソード名", "レア", "実装日", "登場機会"],
                result == ["画像", "エピソード名", "レア", "実装日", "分類"],
            ]
        ):
            raise EpisodeError("Headlines did not match.")

        result[1:1] = ["episode_url"]
        return result

    def records(self) -> list[list[str | element.Tag]]:
        result: list[list] = list()
        for row in super().records():
            field: list[str] = list()
            for cell in row:
                # cell: str | element.Tag
                if isinstance(cell, element.Tag):
                    match cell["class"][0]:
                        case "mu__table--col1":
                            # source: data-srcset[1x, 2x, 3x], srcset, type="image/webp"
                            # source: data-srcset[1x, 2x, 3x], srcset, type="image/png"
                            # img: alt, data-src, height, src, width
                            webp_url: str = cell.findAll("source")[0][
                                "data-srcset"
                            ].rsplit(",")[-1]
                            field.append(webp_url.strip().split()[0])
                        case "mu__table--col2":
                            if cell.a:
                                field.append(cell.a["href"])
                            else:
                                field.append("-")
                            field.append(cell.text.translate(t_table))
                        case _:
                            field.append(cell.text)
            if field[3] in ["SR＋", "SSR＋"]:
                result.append(field)
        return result


if __name__ == "__main__":
    print(__file__)
