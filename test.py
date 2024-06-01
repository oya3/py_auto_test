from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

# アプリの起動
desired_caps = {}
desired_caps["app"] = "Root"
desired_caps["platformName"] = "Windows"
desired_caps["deviceName"] = "WindowsPC"
desired_caps["appium:automationName"] = "Windows"
driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4723',
    desired_capabilities=desired_caps)

# Notepadの起動
exe_path = "C:\\Windows\\system32\\notepad.exe"
os.startfile(exe_path)

# Notepadのウィンドウが表示されるまで待つ
wait = WebDriverWait(driver, 10)  # 最大で10秒間待つ
notepad = wait.until(EC.presence_of_element_located((By.NAME, "無題 - メモ帳")))

# Notepad内の特定の要素をXPathで取得
#element = notepad.find_element_by_xpath(".//Document[@ClassName=\"Edit\"]")

if True: # 1回目文字列書き出し
    xpath = "//Document[@ClassName=\"Edit\"]" # "/Pane[@ClassName=\"#32769\"][@Name=\"デスクトップ 1\"]/Window[@ClassName=\"Notepad\"][@Name=\"無題 - メモ帳\"]/Document[@ClassName=\"Edit\"][@Name=\"テキスト エディター\"]"
    text = "これは自動実行のサンプル。\n"
    element = notepad.find_element_by_xpath(xpath)
    element.send_keys(text)
    
if True: # 2回目文字列書き出し
    xpath = "//Document[@ClassName=\"Edit\"]" # "/Pane[@ClassName=\"#32769\"][@Name=\"デスクトップ 1\"]/Window[@ClassName=\"Notepad\"][@Name=\"無題 - メモ帳\"]/Document[@ClassName=\"Edit\"][@Name=\"テキスト エディター\"]"
    text = "ファイルメニューやボタン操作も自由自在。\n"
    element = notepad.find_element_by_xpath(xpath)
    element.send_keys(text)

if True: # 1回目文字列書き出し
    xpath = "//Document[@ClassName=\"Edit\"]" # "/Pane[@ClassName=\"#32769\"][@Name=\"デスクトップ 1\"]/Window[@ClassName=\"Notepad\"][@Name=\"無題 - メモ帳\"]/Document[@ClassName=\"Edit\"][@Name=\"テキスト エディター\"]"
    text = "これは自動実行のサンプル。\n"
    element = notepad.find_element_by_xpath(xpath)
    element.send_keys(text)
    
if True: # 2回目文字列書き出し
    xpath = "//Document[@ClassName=\"Edit\"]" # "/Pane[@ClassName=\"#32769\"][@Name=\"デスクトップ 1\"]/Window[@ClassName=\"Notepad\"][@Name=\"無題 - メモ帳\"]/Document[@ClassName=\"Edit\"][@Name=\"テキスト エディター\"]"
    text = "ファイルメニューやボタン操作も自由自在。\n"
    element = notepad.find_element_by_xpath(xpath)
    element.send_keys(text)

if True: # ファイル
    xpath = "//MenuBar[@AutomationId=\"MenuBar\"][@Name=\"アプリケーション\"]/MenuItem[@Name=\"ファイル(F)\"]"
    element = notepad.find_element_by_xpath(xpath)
    element.click()

if True: # 終了
    xpath = "//Menu[@Name=\"ファイル(F)\"][@ClassName=\"#32768\"]/MenuItem[@Name=\"メモ帳の終了(X)\"]"
    element = notepad.find_element_by_xpath(xpath)
    element.click()

if True: # 上書きしない
    xpath = "//Window[@Name=\"メモ帳\"][@ClassName=\"#32770\"]/Button[starts-with(@AutomationId,\"CommandButton_\")][@Name=\"保存しない(N)\"]"
    element = notepad.find_element_by_xpath(xpath)
    element.click()
