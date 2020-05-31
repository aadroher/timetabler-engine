from yaml import load, Loader as YamlLoader, Dumper as YamlDumper
from pathlib import Path
from amazing_printer import ap

current_dir = Path(__file__).parent
data_dir_path = current_dir/'../data'
studies_data_path = data_dir_path/'subjects.yml'


def load_data(path):
    raw_data = path.read_text()
    return load(raw_data, Loader=YamlLoader)


def load_studies():
    data = load_data(studies_data_path)
    ap(data)


def main():
    load_studies()
