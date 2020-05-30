from yaml import load, Loader as YamlLoader, Dumper as YamlDumper
from pathlib import Path

from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4).pprint

current_dir = Path(__file__).parent
data_dir_path = current_dir/'../data'
studies_data_path = data_dir_path/'studies.yml'


def load_data(path):
    raw_data = path.read_text()
    return load(raw_data, Loader=YamlLoader)


def load_studies():
    data = load_data(studies_data_path)
    pp(data)


def main():
    load_studies()
