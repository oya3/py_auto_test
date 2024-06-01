import os
import sys
import argparse
from test_runner import TestRunner
from test_reader import TestReader
import traceback
import pdb

os.environ['INLINEDIR'] = os.path.dirname(os.path.abspath(__file__))
os.environ['NO_PROXY'] = "127.0.0.1"
app_name = "auto_test"
print(f"{app_name} version.0.2024.05.26.0000\n")
params = {}
params['url'] = "http://127.0.0.1:4723"

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help='connection destination of WinAppDriver')
parser.add_argument('tests_path', help='tests path')
parser.add_argument('scenario_name', help='scenario name to be executed')
args = parser.parse_args()

if len(sys.argv) != 3:
    print(f"usage: {app_name} <tests_path> <scenario_name>")
    print(" tests_path: tests path")
    print(" scenario_name: scenario name to be executed")
    print(" [options] -u : connection destination of WinAppDriver")
    sys.exit()

params['tests_path'] = args.tests_path
params['scenario_name'] = args.scenario_name

try:
    params['test_reader'] = TestReader(params['tests_path'])
    runner = TestRunner(params)
    runner.run()
    print('complete.')
except Exception as err:
    # エラーメッセージを表示
    print(f"An error occurred: {err}")
    # 詳細なエラー情報（スタックトレース）を表示
    traceback.print_exc()
    # pdb.set_trace()
    # print("args {}".format(err.args))
    # print("err {}".format(str(err)))
    # print("exc_info {}".format(sys.exc_info()))

    sys.exit()
