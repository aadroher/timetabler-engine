
from yaml import load, Loader as YamlLoader, Dumper as YamlDumper
from pathlib import Path

current_dir = Path(__file__).parent
data_dir_path = current_dir/'../../data'


class Loader:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        raw_data = (data_dir_path/f'{collection_name}.yml').read_text()
        self.records = load(raw_data, Loader=YamlLoader)

    def by_code(self, code):
        return (record for record in self.records if record['code'] == code)
