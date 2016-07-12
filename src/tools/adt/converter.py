from .types import ADT


def to_plain(the_object, *args, **kwargs):
    converter = ObjectConverter.get(type(the_object))
    return converter.to_plain(the_object, *args, **kwargs)


def from_plain(the_type, plain_data, *args, **kwargs):
    converter = ObjectConverter.get(the_type)
    return converter.from_plain(the_type, plain_data, *args, **kwargs)


class ObjectConverter:
    _registry = []

    @classmethod
    def register(cls, the_type, converter):
        cls._registry.insert(0, (the_type, converter))

    @classmethod
    def get(cls, the_type):
        if the_type is not None:
            for converter_type, converter in cls._registry:
                if issubclass(the_type, converter_type):
                    return converter()
        return IdentityConverter()


class IdentityConverter(ObjectConverter):
    def to_plain(self, the_object):
        return the_object

    def from_plain(self, the_type, plain_data):
        return plain_data


class ADTConverter(ObjectConverter):
    def to_plain(self, the_object, ignore_fields=[]):
        d = {}
        for field_name, field in the_object._fields.items():
            if not field_name in ignore_fields:
                value = getattr(the_object, field_name)
                converter = ObjectConverter.get(type(value))
                d[field_name] = converter.to_plain(value)
        return d

    def from_plain(self, the_type, plain_data):
        d = {}
        for field_name, field in the_type._fields.items():
            value = plain_data.get(field_name, None)
            converter = ObjectConverter.get(field.type)
            d[field_name] = converter.from_plain(field.type, value)
        return the_type(**d)

ObjectConverter.register(ADT, ADTConverter)


from datetime import date, datetime

class DateConverter(ObjectConverter):
    def to_plain(self, the_object):
        return the_object.isoformat()

    def from_plain(self, the_type, plain_data):
        datetime = datetime.strptime(plain_data, "%Y-%m-%d")
        return date(datetime.year, datetime.month, datetime.day)

ObjectConverter.register(date, DateConverter)


class DateTimeConverter(ObjectConverter):
    def to_plain(self, the_object):
        return the_object.isoformat()

    def from_plain(self, the_type, plain_data):
        # this is problematic, see http://stackoverflow.com/questions/127803/how-to-parse-an-iso-8601-formatted-date-in-python
        return datetime.strptime(plain_data, "%Y-%m-%dT%H:%M:%S.%fZ")

ObjectConverter.register(datetime, DateTimeConverter)


import arrow

class ArrowConverter(ObjectConverter):
    def to_plain(self, the_object):
        return the_object.isoformat()

    def from_plain(self, the_type, plain_data):
        return arrow.get(plain_data)

ObjectConverter.register(arrow.arrow.Arrow, ArrowConverter)

