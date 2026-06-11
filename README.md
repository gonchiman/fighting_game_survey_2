# Fighting Game Steam Analysis

Steam Charts の月間平均プレイヤー数をもとに、Steam で配信されている格闘ゲームのプレイヤー数推移や累積推定プレイ時間を可視化する分析プロジェクトです。

Streamlit アプリでグラフとテーブルを確認できるほか、データ取得、図表出力、レビュー数からの推定販売本数計算をスクリプトとして実行できます。

## 主な機能

- Steam Charts から月間統計 CSV を取得
- 月間平均プレイヤー数の推移を可視化
- 平均プレイヤー数から月間・累積の推定プレイ時間を計算
- 初月ピーク人数と安定期平均プレイヤー数を比較
- 各タイトルのプレイヤー指標をテーブルとチャートで分析
- Steam レビュー数から販売本数を簡易推定

## 対象タイトル

対象タイトルは [src/fighting_game_analysis/config/games.py](src/fighting_game_analysis/config/games.py) の `GAMES` で管理しています。

現在の主な対象タイトル:

- Street Fighter V
- TEKKEN 7
- DRAGON BALL FighterZ
- SOULCALIBUR VI
- Mortal Kombat 11
- GUILTY GEAR -STRIVE-
- Street Fighter 6
- TEKKEN 8
- Granblue Fantasy Versus: Rising
- JoJo's Bizarre Adventure: All-Star Battle R
- FATAL FURY: City of the Wolves

## セットアップ

Python 3.11 以上を使用します。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m pip install streamlit pytest
```

## Streamlit アプリの起動

```powershell
streamlit run app.py
```

アプリから以下の分析ページを開けます。

- `Cumulative Play Hours`: 累積推定プレイ時間
- `Avg Players Trend`: 月間平均プレイヤー数の推移
- `Player Metrics Analysis`: 初月比、偏差値、前月比などの指標
- `Initial Peak vs Stable Average Players`: 初月ピーク人数と安定期平均プレイヤー数の比較

トップページの `Data Update` から、選択したタイトルの Steam Charts CSV を更新できます。

## コマンドラインでの使い方

すべての対象タイトルの Steam Charts CSV を取得します。

```powershell
python scripts/fetch_all.py
```

取得済み CSV からグラフ画像を出力します。

```powershell
python scripts/save_figures.py
```

Steam レビュー数を取得し、推定 Steam 販売本数を表示します。

```powershell
python scripts/estimate_sales.py
```

## データと出力

- 生データ CSV: `data/raw/`
- 生成グラフ: `outputs/figures/`
- レポート関連ファイル: `reports/`

Steam Charts の CSV はタイトルごとに `data/raw/` に保存されます。ファイル名はゲームタイトルを小文字化し、スペースや記号を置換した形式です。

## テスト

```powershell
pytest
```

テスト対象は `tests/` にあります。

## プロジェクト構成

```text
app.py                         Streamlit アプリのトップページ
pages/                         Streamlit の各分析ページ
scripts/                       データ取得・図表保存・推定処理の実行スクリプト
src/fighting_game_analysis/    分析ロジック、データ取得、設定、可視化
data/raw/                      Steam Charts から取得した CSV
outputs/                       生成した図表やレポート
tests/                         自動テスト
```

## メモ

- `Avg. Players` は Steam Charts の月間平均プレイヤー数です。
- 推定プレイ時間は `Avg. Players * 月の日数 * 24` で計算しています。
- `Last 30 Days` の行は月単位の分析から除外しています。
- 取得元サイトの構造変更により、データ取得処理が動かなくなる可能性があります。
