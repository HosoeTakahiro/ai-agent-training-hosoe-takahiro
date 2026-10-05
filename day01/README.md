# Day 01

## 受講者が実装する場所

- `day01/app.py`（基本はこのファイルを編集）

## 目的

- 開発環境のセットアップができる状態にする
- GitHubのPR提出フローに慣れる
- Pythonで小さなCLIを作り、例外/ログ/READMEの書き方を身につける

## ゴール（完了条件）

- READMEどおりに第三者が実行できる
- 入力不備で終了コード `2` になり、標準エラーに分かりやすいメッセージが出る

## 機能要件

### 機能要件

コマンド

- `python -m day01.app` で起動できること（モジュール名は固定）

必須オプション

- `--name`：表示したい名前（文字列、必須）

任意オプション

- `--repeat`：繰り返し回数（整数、デフォルト `1`、1〜10）
- `--format`：出力形式（`text` / `json`、デフォルト `text`）

出力

- `--format text` の場合：標準出力に、指定回数分のテキストを出す
- `--format json` の場合：標準出力にJSONを出す
  - 例：`{"name":"Taro","repeat":2,"outputs":["Hello, Taro","Hello, Taro"]}`

終了コード

- 正常終了：`0`
- 入力不備（未指定、範囲外など）：`2`

ログ

- 実行開始時に、`name` / `repeat` / `format` をINFOで出す
- 例外発生時はERRORで出す

### 受け入れ基準

- `--name` 未指定で終了コード `2`、標準エラーに分かりやすいメッセージが出る
- `--repeat 2` で2行（または2要素）出る
- `--format json` でJSONとしてパース可能な文字列が出る

## 実装タスク

- `day01/app.py` を編集し、機能要件を満たす
- 例外時は標準エラーへメッセージを出し、終了コードを要件どおりにする

## 実行方法

### セットアップ

```bash
# 仮想環境の作成と有効化
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 実行コマンド例

```bash
# 基本的な実行
python -m day01.app --name "Taro"

# 繰り返し回数を指定
python -m day01.app --name "Taro" --repeat 3

# JSON形式で出力
python -m day01.app --name "Taro" --repeat 2 --format json
```

### 期待する出力例

```
# --name "Taro" の場合
Hello, Taro

# --name "Taro" --repeat 2 --format json の場合
{"name": "Taro", "repeat": 2, "outputs": ["Hello, Taro", "Hello, Taro"]}
```

---

**以下は受講者が記入してください**

- 追加で確認した入力例：python -m day01.app --name
                      python -m day01.app --name "Hosoe"
                      python -m day01.app --name "Hosoe" --repeat 30
                      python day01/app.py --name “HosoeHosoeHosoeHosoeHosoeHosoeHosoeHosoeHosoeHosoeHosoeHosoeHosoeHosoeHosoeHosoeHosoeHosoe”  
- 発生したエラーと対処：当初は「def _validate_args」内にエラーを出力する用のコードを作成したが、思った通りにエラーとならなかった。そこでCopilotと連携し、コマンドの意味をなどを調べ、「class Day01ArgumentParser」を作成し、「def build_parser()」に継承するようにした。

## 提出物

- `day01/app.py`
- `day01/README.md`

## セルフレビュー

- 正常系：`--name Taro` で期待どおりに表示される
- 異常系：`--name` 未指定でエラーになり、メッセージが分かりやすい
- 境界：`--name` に長い文字列や記号を入れても壊れない
- 再実行：同じ入力で複数回実行しても安定して同じ結果になる

## リサーチメモ（任意）

調べたURLや、理解した要点をメモしてください。

- Python仮想環境（venv等）
　他のプロジェクトに影響が発生しないよう仮想環境を作成し有効化する必要があること
- 依存管理（requirements/pyprojectの考え方）
　追加のライブラリを使用するためには「pip install –r requirements.txt」で依存関係をインストールする必要があること。
- CLIの引数処理（例：argparse等）
　argparseはPythonのスクリプトに渡すコマンドライン引数を解析してくれｒ標準ライブラリ。
　<https://www.r-jc.jp/news-blog/1426/python-argparse-%E4%BD%BF%E3%81%84%E6%96%B9%E5%BC%95%E6%95%B0%E4%B8%80%E8%A6%A7%E8%A1%A8%E3%81%A8cli%E9%9B%9B%E5%BD%A2314%E5%AF%BE%E5%BF%9C/>
- ログ（INFO/ERRORの使い分け）
　INFO：プログラムが正常に稼働している時の記録、通常の挙動の把握に使用する。
　ERROR：問題が発生し、処理が失敗または中断したときの記録、対応が必要な場合に使われることが多い。
　<https://jisou-programmer.beproud.jp/%E3%83%AD%E3%82%AE%E3%83%B3%E3%82%B0/71-info%E3%80%81error%E3%81%A0%E3%81%91%E3%81%A7%E3%81%AA%E3%81%8F%E3%83%AD%E3%82%B0%E3%83%AC%E3%83%99%E3%83%AB%E3%82%92%E4%BD%BF%E3%81%84%E5%88%86%E3%81%91%E3%82%8B.html>
- GitHub：ブランチ作成→PR→修正push
　以下を参照し実行
　<https://zenn.dev/praha/articles/db1c4bcc4ef48c>