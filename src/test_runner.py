
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
from image_comp import ImageComp
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
        self.elements = {}

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
        time.sleep(2)  # 表示アニメーション完了待ち

    def wait_for_form(self, params):
        print(f"wait_for_form: {params}")
        xpath = params['xpath']
        # if self.driver.find_element_by_xpath(xpath).is_displayed():
        #self.appwait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        if ('name' in params):
            self.app = self.wait.until(EC.presence_of_element_located((By.NAME, params['name'])))
        elif ('class_name' in params):
            self.app = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, params['class_name'])))
        else:
            raise ValueError(f"ERROR: not found wait_for_app prams.{params}")

    def set_element(self, params):
        print(f"set_element: {params}")
        name = params['element_name']
        xpath = params['xpath']
        element = self.app.find_element_by_xpath(xpath)
        self.elements[name] = element

    def get_text(self, xpath):
        print(f"get_text: {xpath}")
        element = self.app.find_element_by_xpath(xpath)
        value = element.get_attribute("Value.Value")
        print(value)

    def assert_text(self, params):
        print(f"assert_text: {params}")
        target_element = self.app
        if 'element_name' in params:
            target_element = self.elements[params['element_name']]
        element = target_element.find_element_by_xpath(params['xpath'])
        actual = element.get_attribute(params['target'])
        if (actual != params['expected']):
            print(f"assert {actual} != {params['expected']}")
        else:
            print("OK")

    def set_text(self, params):
        xpath = params['xpath']
        print(f"set_text: {xpath}:{params['text']}")
        target_element = self.app
        element = target_element.find_element_by_xpath(xpath)
        element.send_keys(params['text'])

    def get_keys(self, key_strings):
        results = []
        keys = key_strings.split('+')
        for key in keys:
            if key == 'enter':
                results.append(Keys.ENTER)
            else:
                results.append(key)
        return results

    def click(self, params):
        print(f"click: {params}")
        xpath = params['xpath']
        target_element = self.app
        if 'element_name' in params:
            target_element = self.elements[params['element_name']]
        try:
            # self.driver.find_element_by_xpath(xpath).click()
            target_element.find_element_by_xpath(xpath).click()
            return  # 通常クリック成功
        except Exception as err:
            # エラーメッセージを表示
            print(f"An error occurred: {err}")
        # clickダメならSPACE送信
        target_element.find_element_by_xpath(xpath).send_keys(Keys.SPACE)

    def select(self, params):
        print(f"select: {params}")
        xpath = params['xpath']
        target_element = self.app
        if 'element_name' in params:
            target_element = self.elements[params['element_name']]
        element = target_element.find_element_by_xpath(xpath)
        element.click()
        element.find_element_by_name(params['value']).click()

    def screenshot(self, sequence_name, command_index, params=None):
        spath = os.path.join(self.screenshots_path, sequence_name)
        os.makedirs(spath, exist_ok=True)
        png_file = f"{command_index:03d}.png"
        if params and 'filepath' in params:
            png_file = params['filepath']
        png_filepath = os.path.join(spath, png_file)
        png_filepath = png_filepath.replace("\\", "/")
        # 旧ファイルが存在している場合、oldファイルにしてバックアップする
        bak_filepath = self.create_backup_file(png_filepath, '.bak')
        self.app.screenshot(os.path.join(spath, png_file))  # アプリのみスクリーンショット
        if bak_filepath is not None:
            comp = ImageComp(png_filepath, bak_filepath)
            comp.run()

    def get_backup_file_name(self, filepath, append_ext):
        dirpath, filename = os.path.split(filepath)
        basename, ext = os.path.splitext(filename)
        new_filename = f"{basename}{append_ext}{ext}"
        new_filepath = os.path.join(dirpath, new_filename)
        new_filepath = new_filepath.replace("\\", "/")
        return new_filepath

    def create_backup_file(self, filepath, append_ext):
        if not os.path.isfile(filepath):
            return None  # ファイルが存在しない場合はバックアップしない
        new_filepath = self.get_backup_file_name(filepath, append_ext)
        shutil.copyfile(filepath, new_filepath)
        return new_filepath

    def run(self):
        for sequence_name in self.scenario['sequences']:
            print(f"sequence_name:[{sequence_name}]")
            sequence = self.sequences[sequence_name]
            for command_index, command in enumerate(sequence['commands']):
                name = command['name']
                params = command['params']
                print(f"command:[{name}/{params}]")
                # debug command. 現状は停止するしかできない
                if ('debug' in command):
                    pdb.set_trace()
                # アプリ起動
                if name == 'exe_spawn':
                    self.exe_spawn(params['exe_path'])
                    # self.wait = WebDriverWait(self.driver, 10)
                # アプリ起動待ち
                elif name == 'wait_for_app':
                    self.wait_for_app(params)
                    # 自動スクリーンショット
                    self.screenshot(sequence_name, command_index)
                # アプリ起動待ち for Form 版（waite_for_app + AccessibleName(Name)を使うので、もう使わないはず）
                elif name == 'wait_for_form':
                    self.wait_for_form(params)
                    # 自動スクリーンショット
                    self.screenshot(sequence_name, command_index)
                    # spath = os.path.join(self.screenshots_path, sequence_name)
                    # os.makedirs(spath, exist_ok=True)
                    # png_file = f"{command_index:03d}.png"
                    # if 'AutomationId' in params['xpath']:
                    #     png_file = f"{command_index:03d}_{params['xpath'].split('AutomationId=')[1].split(' ')[0]}.png"
                    # if self.screenshots_auto:
                    #     self.driver.save_screenshot(os.path.join(spath, png_file))
                # テキストエリアに文字列を設定
                elif name == 'set_text':
                    self.set_text(params)
                # クリックイベント発行（ラジオボタンの選択も含む）
                elif name == 'click':
                    self.click(params)
                # 待ち(ms)
                elif name == 'sleep':
                    time.sleep(params['time'] / 1000)
                # 画面キャプチャ
                elif name == 'screenshot':
                    self.screenshot(sequence_name, command_index, params)
                # ディレクトリコピー
                elif name == 'directory_copy':
                    print(f"shutil.copytree({params['src']}, {params['dst']})")
                    shutil.copytree(params['src'], params['dst'])
                # ファイルコピー
                elif name == 'file_copy':
                    print(f"shutil.copy2({params['src']}, {params['dst']})")
                    shutil.copy2(params['src'], params['dst'])
                # 文字列確認
                elif name == 'assert_text':
                    self.assert_text(params)
                # プルダウン選択
                elif name == 'select':
                    self.select(params)
                # プルダウン選択
                elif name == 'set_element':
                    self.set_element(params)
