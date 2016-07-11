import sys


class Field:
    def __init__(self, type=None, null=False, default=None):
        self.type = type
        self.null = null
        self.default = default

    def __setattr__(self, name, value):
        if sys._getframe(1).f_locals.get("self") != self:
            raise NotImplementedError("You cannot modify a field from outside it")
        self.__dict__[name] = value


class ADTMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # Group all fields (and fields of base classes) in a "_fields" class attribute
        new_attrs = {
            "_fields": {},
        }
        all_attrs = {}
        for base in bases:
            if issubclass(base, ADT):
                all_attrs.update(base._fields)
        all_attrs.update(attrs)
        for attr_name, attr_value in all_attrs.items():
            if isinstance(attr_value, Field):
                new_attrs["_fields"][attr_name] = attr_value
            else:
                new_attrs[attr_name] = attr_value

        return type.__new__(cls, name, bases, new_attrs)


class ADT(metaclass=ADTMetaclass):
    """
    A class that behaves like an Abstract Data Type. It does not allow arbitrary modification of
    attributes from outside, but else can only change state via well-defined actions (commands).
    """

    def __init__(self, *args, **kwargs):
        for field_name, field in self._fields.items():
            value = kwargs.get(field_name, field.default)
            if not field.null:
                assert value != None, "'{}' must not be None".format(field_name)
            if field.type:
                assert value == None or type(value) == field.type, "'{}' must be {}".format(field_name, field.type)
            self.__dict__[field_name] = value

    def __setattr__(self, field_name, value):
        if sys._getframe(1).f_locals.get("self") != self:
            raise NotImplementedError("You cannot modify a {} from outside it".format(self.__class__.__name__))
        field = self._fields.get(field_name)
        if not field:
            raise IndexError("Attribute '{}' not found".format(field_name))
        if not field.null:
            assert value != None, "'{}' must not be None".format(field_name)
        if field.type:
            assert value == None or isinstance(value, field.type), "'{}' must be {}".format(field_name, field.type)
        self.__dict__[field_name] = value


class StrField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(type=str, *args, **kwargs)


class IntField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(type=int, *args, **kwargs)


class FloatField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(type=float, *args, **kwargs)


class ADTID(ADT):
    id = IntField(null=True)

    @property
    def is_attached(self):
        return (self.id is not None)

    def attach(self, id):
        self.id = id

