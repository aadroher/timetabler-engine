import yaml


class Subjects(yaml.YAMLObject):
    yaml_tag = '!Subjects'

    def __init__(self, name, code):
        self.name = name
        self.code = code
