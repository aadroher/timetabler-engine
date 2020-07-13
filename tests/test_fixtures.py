import pprint
from .fixtures.loader import load_data

pp = pprint.PrettyPrinter(indent=4).pprint


def test_fixtures():
    print(
        load_data()
    )
