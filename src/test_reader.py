import yaml
import glob
import os

class TestReader:
    def __init__(self, path):
        self.path = path
        self.read_yaml(self.path)

    def symbolize(self, obj):
        if isinstance(obj, dict):
            return {k: self.symbolize(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.symbolize(v) for v in obj]
        else:
            return obj

    def read_yaml(self, path):
        self.scenarios = {}
        self.sequences = {}
        for file in glob.glob(f"{path}/**/*.yml", recursive=True):
            print(f"reading... {file}")
            with open(file, 'r', encoding='utf-8') as f:
                body = yaml.safe_load(f)
            body = self.symbolize(body)
            if 'content_type' not in body:
                raise ValueError("ERROR: not found :content_type")
            if 'contents' not in body:
                raise ValueError("ERROR: not found :contents")
            contents = body['contents']
            if 'name' not in contents:
                raise ValueError("ERROR: not found :name")
            if body['content_type'] == 'screen_test_scenario':
                if contents['name'] in self.scenarios:
                    raise ValueError(f"ERROR: multiple scenario name: {contents['name']}")
                if 'config' not in contents:
                    raise ValueError("ERROR: not found :config")
                if 'sequences' not in contents:
                    raise ValueError("ERROR: not found :sequences")
                self.scenarios[contents['name']] = contents
            elif body['content_type'] == 'screen_test_sequence':
                if contents['name'] in self.sequences:
                    raise ValueError(f"ERROR: multiple sequence name: {contents['name']}")
                if 'commands' not in contents:
                    raise ValueError("ERROR: not found :commands")
                self.sequences[contents['name']] = contents
            else:
                raise ValueError(f"ERROR: unknown content_type: {body['content_type']}")
