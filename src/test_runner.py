
# このコードは、元のRubyコードの機能をPythonで再現するために作成されました。
# ただし、このコードはあくまで参考であり、実際の環境で動作するかどうかは保証できません。
# 必要に応じて適宜修正してください。ご了承ください。
# また、selenium-webdriverとfileutilsはPythonのseleniumとshutilに対応します。
# pryはデバッグ用のライブラリで、Pythonではpdbが相当しますが、このコードではデバッグ用のコードは省略しています。
# 必要に応じてimport pdb; pdb.set_trace()を挿入してください。
# また、spawnメソッドはRubyのプロセス生成メソッドで、Pythonではos.systemが相当します。
# ただし、os.systemはシェルを経由してコマンドを実行するため、引数のエスケープなどに注意が必要です。
# また、os.systemはコマンドの終了を待つため、非同期にプロセスを生成したい場合はsubprocess.Popenなどを使用してください。
# 以上を踏まえて、適宜コードを修正して使用してください。
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.chrome.options import Options
import os
import time
import shutil
import pdb

class TestRunner:
    def __init__(self, params):
        self.params = params
        if 'scenario_name' not in self.params:
            raise ValueError("ERROR: not found :scenario_name")
        if 'url' not in self.params:
            raise ValueError("ERROR: not found :url")
        if 'test_reader' not in self.params:
            raise ValueError("ERROR: not found :test_reader")
        self.test_reader = self.params['test_reader']
        self.scenario_name = self.params['scenario_name']
        if self.scenario_name not in self.test_reader.scenarios:
            raise ValueError("ERROR: not found scenario_name")
        self.scenario = self.test_reader.scenarios[self.scenario_name]
        self.sequences = self.test_reader.sequences
        self.capabilities = {}
        self.capabilities["app"] = "Root"
        self.capabilities["platformName"] = "Windows"
        self.capabilities["deviceName"] = "WindowsPC"
        self.capabilities["appium:automationName"] = "Windows"
        self.driver = webdriver.Remote(
            command_executor=self.params['url'],
            desired_capabilities=self.capabilities)

        self.config = self.scenario['config']
        self.screenshots_path = self.config['screenshots_path']
        self.screenshots_auto = self.config.get('screenshots_auto', True)
        os.makedirs(self.screenshots_path, exist_ok=True)

    def exe_spawn(self, exe_path):
        print(f"exe_spawn: {exe_path}")
        os.startfile(exe_path)
        self.wait = WebDriverWait(self.driver, 20)  # 最大で20秒間待つ

    def wait_for_app(self, params):
        print(f"wait_for_app: {params}")
        if ('name' in params):
            self.app = self.wait.until(EC.presence_of_element_located((By.NAME, params['name'])))
        elif ('class_name' in params):
            self.app = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, params['class_name'])))
        else:
            raise ValueError(f"ERROR: not found wait_for_app prams.{params}")

    def wait_for_form(self, xpath):
        print(f"wait_for_form: {xpath}")
        # if self.driver.find_element_by_xpath(xpath).is_displayed():
        self.appwait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def get_text(self, xpath):
        print(f"get_text: {xpath}")
        element = self.app.find_element_by_xpath(xpath)
        value = element.get_attribute("Value.Value")
        print(value)

    def assert_text(self, params):
        print(f"assert_text: {params}")
        element = self.app.find_element_by_xpath(params['xpath'])
        # value = element.get_attribute("Value.Value")
        actual = element.get_attribute(params['target'])
        if (actual != params['expected']):
            print(f"assert {actual} != {params['expected']}")
        else:
            print("OK")

    def set_text(self, params):
        xpath = params['xpath']
        print(f"set_text: {xpath}:{params['text']}")
        element = self.app.find_element_by_xpath(xpath)
        # element = self.appwait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        element.send_keys(params['text'])
        # if 'after_key_event' in params:
        #     _keys = self.get_keys(params['after_key_event'])
        #     if len(_keys) == 1:
        #         element.send_keys(_keys[0])
        #     else:
        #         element.send_keys(_keys[0], _keys[1])

    def get_keys(self, key_strings):
        results = []
        keys = key_strings.split('+')
        for key in keys:
            if key == 'enter':
                results.append(Keys.ENTER)
            else:
                results.append(key)
        return results

    def click(self, xpath):
        print(f"click: {xpath}")
        try:
            # self.driver.find_element_by_xpath(xpath).click()
            self.app.find_element_by_xpath(xpath).click()
            return  # 通常クリック成功
        except Exception as err:
            # エラーメッセージを表示
            print(f"An error occurred: {err}")
        # clickダメならSPACE送信
        self.app.find_element_by_xpath(xpath).send_keys(Keys.SPACE)

    def run(self):
        for sequence_name in self.scenario['sequences']:
            print(f"sequence_name:[{sequence_name}]")
            sequence = self.sequences[sequence_name]
            for command_index, command in enumerate(sequence['commands']):
                name = command['name']
                params = command['params']
                print(f"command:[{name}/{params}]")
                if name == 'exe_spawn':
                    self.exe_spawn(params['exe_path'])
                    # self.wait = WebDriverWait(self.driver, 10)
                elif name == 'wait_for_app':
                    self.wait_for_app(params)
                    # 自動スクリーンショット
                    spath = os.path.join(self.screenshots_path, sequence_name)
                    os.makedirs(spath, exist_ok=True)
                    png_file = f"{command_index:03d}.png"
                    if self.screenshots_auto:
                        self.driver.save_screenshot(os.path.join(spath, png_file))

                elif name == 'wait_for_form':
                    self.wait_for_form(params['xpath'])
                    # 自動スクリーンショット
                    spath = os.path.join(self.screenshots_path, sequence_name)
                    os.makedirs(spath, exist_ok=True)
                    png_file = f"{command_index:03d}.png"
                    if 'AutomationId' in params['xpath']:
                        png_file = f"{command_index:03d}_{params['xpath'].split('AutomationId=')[1].split(' ')[0]}.png"
                    if self.screenshots_auto:
                        self.driver.save_screenshot(os.path.join(spath, png_file))

                elif name == 'set_text':
                    self.set_text(params)
                elif name == 'click':
                    self.click(params['xpath'])
                elif name == 'sleep':
                    time.sleep(params['time'] / 1000)
                elif name == 'screenshot':
                    spath = os.path.join(self.screenshots_path, sequence_name)
                    os.makedirs(spath, exist_ok=True)
                    png_file = f"{command_index:03d}.png"
                    if params and 'filepath' in params:
                        png_file = params['filepath']
                    self.driver.save_screenshot(os.path.join(spath, png_file))
                elif name == 'directory_copy':
                    print(f"shutil.copytree({params['src']}, {params['dst']})")
                    shutil.copytree(params['src'], params['dst'])
                elif name == 'file_copy':
                    print(f"shutil.copy2({params['src']}, {params['dst']})")
                    shutil.copy2(params['src'], params['dst'])
                elif name == 'assert_text':
                    self.assert_text(params)
