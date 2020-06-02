import pprint

pretty_printer = pprint.PrettyPrinter(indent=4)


def pp(value):
    return pretty_printer.pprint(value)
