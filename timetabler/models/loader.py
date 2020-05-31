
from collections import namedtuple
from yaml import load, Loader as YamlLoader, Dumper as YamlDumper
from pathlib import Path

from amazing_printer import ap

current_dir = Path(__file__).parent
data_dir_path = current_dir/'../../data'


def get_named_tuple(type_name='', record=None):
    field_names = list(record)
    NewClass = namedtuple(type_name, field_names)
    return NewClass(**record)


def load_records(type_name='', collection_name=''):
    raw_data = (data_dir_path/f'{collection_name}.yml').read_text()
    records = load(raw_data, Loader=YamlLoader)
    return [get_named_tuple(type_name=type_name, record=record) for record in records]
