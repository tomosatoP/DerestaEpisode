# デレステのエピソード一覧
[Gamerch](https://gamerch.com/) の [アイマス デレステ攻略まとめwiki](https://gamerch.com/imascg-slstage-wiki/) からエピソード一覧を取得

1. [アイドル一覧](https://gamerch.com/imascg-slstage-wiki/entry/516012) から `プロフィール一覧` を取得
1. `プロフィール一覧` から `<アイドル>のプロフィールとセリフ一覧` の URL([例](https://gamerch.com/imascg-slstage-wiki/entry/517369)) を取得
1. `<アイドル>のプロフィールとセリフ一覧` から `エピソード一覧` を取得
1. `エピソード一覧` から `SR＋`, `SSR＋` の `エピソード` の URL([例](https://gamerch.com/imascg-slstage-wiki/entry/523527)) を取得
1. URL から欲しいデータをスクレイピング

## 制限事項

1. `プロフィール一覧` にゲスト(最上静香, ジュリア)が含まれていない。
1. `エピソード一覧` の `見出し` は、異なっているアイドルがある。... 例: `登場機会` -> `分類`
1. `エピソード` の table は、各行が `見出し`, `フィールド` の構成になっている。
1. `エピソード` の `フィールド` は、統一しきれていない。

## 補足
環境: wsl2 - Ubuntu
~~~sh
~ $ sudo apt -y install python3 python3-pip
~ $ sudo -H python3 -m pip install --upgrade pip

~ $ git clone https://github.com/tomosatoP/DerestaEpisode.git
~/DerestaEpisode $ python3 -m venv venv --upgrade-deps
~/DerestaEpisode $ . venv/bin/activate
(venv) ~/DerestaEpisode $ pip install requests beatifulsoup4
(venv) ~/DerestaEpisode $ python3 datalist.py
~~~