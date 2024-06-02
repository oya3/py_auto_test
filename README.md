# git clone 後の開発環境構築

## python仮想化環境設定

```bash
$ poetry install
$ source .venv/Scripts/activate
```
## テスト実行

1. WindowsApplicationDriverを起動する

```
$ "C:\Program Files\Windows Application Driver\WinAppDriver.exe"
Windows Application Driver listening for requests at: http://127.0.0.1:4723/
Press ENTER to exit.
```

2. サンプルのメモ帳テストを実施

```
$ python test.py
```

# 新規プロジェクト作成

## poetry プロジェクト設定

```
$ poetry init

This command will guide you through creating your pyproject.toml config.

Package name [py_auto_test]:
Version [0.1.0]:
Description []:
Author [Kazunori OYA <terje@oya3.net>, n to skip]:
License []:  mit
Compatible Python versions [^3.11]:

Would you like to define your main dependencies interactively? (yes/no) [yes] no
Would you like to define your development dependencies interactively? (yes/no) [yes] no
Generated file

[tool.poetry]
name = "py_auto_test"
version = "0.1.0"
description = ""
authors = ["Kazunori OYA <terje@oya3.net>"]
license = "mit"
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"


Do you confirm generation? (yes/no) [yes]
```

## 仮想環境を.venvで作成する設定

```
$ poetry config virtualenvs.in-project true
```

## poetry のパッケージモードを無効にする

> $ emacs pyproject.toml
```
[tool.poetry]
...
package-mode = false   #<--- ここ追加。パッケージモードを無効にする
```

## パッケージ追加

```
$ poetry add appium-python-client==1.3.0
$ poetry add urllib3==1.26.18
$ poetry add pyyaml

# 開発パッケージ追加（静的解析）
$ poetry add --dev jedi flake8 importmagic autopep8 yapf black

```

## 実行

``` bash
# メモ帳デモ
$ python src/main.py "tests/notepad" "memo"
# 電卓デモ
$ python src/main.py "tests/calc" "arithmetic_operation"
```

# WinAppDriver.exeのインストールパス

おそらく以下のパターンのどれか。

- "C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
- "C:\Program Files\Windows Application Driver\WinAppDriver.exe"

# 参考URL

- 公式ドキュメント
  https://github.com/microsoft/WinAppDriver/tree/master/Docs
    - release
      https://github.com/microsoft/WinAppDriver/releases
- pypi
    - Appium-Python-Client 1.3.0
      https://pypi.org/project/Appium-Python-Client/1.3.0/

# 課題

- 絶対xpathを指定するとelementが2回目から取得できない問題
    たぶん、相対xpathにすることで対応できている様子（アプリケーションからのxpath指定にするだけ）
    - How to use WinAppDriver to locate elements on Modal window of Modal window
       https://stackoverflow.com/questions/67631773/how-to-use-winappdriver-to-locate-elements-on-modal-window-of-modal-window
