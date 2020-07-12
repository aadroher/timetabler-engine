import pprint
from .fixtures import load_data

pp = pprint.PrettyPrinter(indent=4).pprint


def test_fixtures():
    print(
        load_data()
    )
