from pathlib import Path
from functools import reduce
from yaml import load, Loader as YamlLoader, Dumper as YamlDumper
import json

current_dir = Path(__file__).parent
data_dir_path = current_dir/'../data'

COLLECTION_NAMES = [
    'phases',
    'curricula'
]


def load_records(collection_name=''):
    raw_data = (data_dir_path/f'{collection_name}.yml').read_text()
    return load(raw_data, Loader=YamlLoader)


def add_collection(collections, collection_name):
    new_collection_fragment = {
        collection_name: load_records(collection_name)
    }
    return {**collections, **new_collection_fragment}


def load_data():
    collections = reduce(add_collection, COLLECTION_NAMES, {})

    return json.dumps(collections, indent=2)
