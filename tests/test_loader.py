
import pprint
from timetabler.models.loader import load_records

pp = pprint.PrettyPrinter(indent=4).pprint


def test_loader():
    records = load_records(type_name='Subject', collection_name='subjects')
    record = records[0]

    pp(records)
    pp(record)
    pp(record.name)
    pp(record.code)
    pp(record.type)
