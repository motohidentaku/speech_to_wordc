# Speech to Wordc

Amazon Transcribeが出力した結果を基にWordcloudを描く


## Requirements

* Python 3.7
* [Poetry](https://python-poetry.org/) 
* [Amazon Transcribe](https://aws.amazon.com/jp/transcribe/)の出力データ

## Install
Poetry
```
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
$ source $HOME/.poetry/env
```
下記のバージョン確認で`・・・py2.7/subprocess32.py:149: RuntimeWarning: The _posixsubprocess・・・`というエラーが出たら、`~/.poetry/bin/poetry`の１行目を`#!/usr/bin/env python3`に変更
```
$ poetry --version
```

Speech to Wordc
```
$ poetry install
```

辞書の変更（しなくてもいい）
```
git clone https://github.com/neologd/mecab-ipadic-neologd.git
xz -dkv mecab-ipadic-neologd/seed/*.csv.xz
cat mecab-ipadic-neologd/seed/*.csv > neologd.csv
```

```
from janome.dic import UserDictionary
from janome import sysdic
user_dict = UserDictionary('neologd.csv', 'utf8', 'ipadic', sysdic.connections)
user_dict.save('neologd')
```

## Run
S3にアクセスできるロールが設定されているEC2で実行するか、当該bucketへアクセスできるアクセスキーが環境変数で設定されていること。

```
$ poetry shell
$ speech_to_wordc 
```
or
```
$ poetry run speech_to_wordc
```

以下の引数が必須です

* `--bucket <S3 BUCKET>`: Amazon Transcribeの結果が格納されているS3のbucket名
* `--file <S3 FILEPATH>`: Amazon Transcribeの結果が格納されているS3のファイルパス名

以下の引数が利用可能です

* `--output <FILEPATH>`: 画像ファイルを出力するパス。defaultは`speech_to_wordc/out/wc_`
* `--notword <FILEPATH>`: 集計対象から除外する単語リスト。defaultは`notword.txt`
* `--font <FILEPATH>`: 集計対象から除外する単語リスト。defaultは`speech_to_wordc/Meiryo.ttf`
