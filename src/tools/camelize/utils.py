# -*- coding: utf-8  -*-

from collections import OrderedDict
import re


def camelize(data):
    def _underscore_to_camel(match):
        return match.group()[0] + match.group()[2].upper()

    if isinstance(data, dict):
        new_dict = OrderedDict()
        for key, value in data.items():
            new_key = re.sub(r"[a-z]_[a-z]", _underscore_to_camel, key)
            new_dict[new_key] = camelize(value)
        return new_dict
    if isinstance(data, (list, tuple)):
        for i in range(len(data)):
            data[i] = camelize(data[i])
        return data
    return data



first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def underscoreize(data):
    def _camel_to_underscore(name):
        s1 = first_cap_re.sub(r'\1_\2', name)
        return all_cap_re.sub(r'\1_\2', s1).lower()

    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = _camel_to_underscore(key)
            new_dict[new_key] = underscoreize(value)
        return new_dict
    if isinstance(data, (list, tuple)):
        for i in range(len(data)):
            data[i] = underscoreize(data[i])
        return data
    return data
