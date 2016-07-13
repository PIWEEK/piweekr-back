from functools import partial

from .types import ADT, Field, ADTMetaclass


class RoleSingle(ADT):
    role_class = Field()
    role_name = Field(type=str)


class RoleMulti(ADT):
    role_class = Field()
    role_name = Field(type=str)
    role_fk = Field(type=str)
    required = Field(type=bool, default=True)


class Relationship1NMetaclass(type):

    def __init__(self, name, bases, attrs):
        super().__init__(name, bases, attrs)

        if hasattr(self, "role_1"):
            if not hasattr(self.role_1.role_class, "_relationships"):
                self.role_1.role_class._relationships = {}
            self.role_1.role_class._relationships[self.role_n.role_name] = self

            if not hasattr(self.role_n.role_class, "_relationships"):
                self.role_n.role_class._relationships = {}
            self.role_n.role_class._relationships[self.role_1.role_name] = self


class Relationship1N(metaclass=Relationship1NMetaclass):
    pass


class Context:

    def __init__(self):
        self._storage = {}

    def add(self, instance):
        the_class = instance.__class__
        if not self._storage.get(the_class):
            self._storage[the_class] = {}
        self._storage[the_class][instance.id] = instance

        if hasattr(the_class, "_relationships"):
            for relationship in the_class._relationships.values():
                if issubclass(relationship, Relationship1N):
                    if the_class == relationship.role_1.role_class:
                        foreign_instances = getattr(self, relationship.role_n.role_name)(instance)
                        instance.__dict__[relationship.role_n.role_name] = foreign_instances
                        for foreign_instance in foreign_instances:
                            foreign_instance.__dict__[relationship.role_1.role_name] = instance
                    if the_class == relationship.role_n.role_class:
                        foreign_instance = getattr(self, relationship.role_1.role_name)(instance)
                        instance.__dict__[relationship.role_1.role_name] = foreign_instance
                        if foreign_instance:
                            if not hasattr(foreign_instance, relationship.role_n.role_name):
                                foreign_instance.__dict__[relationship.role_n.role_name] = []
                            foreign_instance.__dict__[relationship.role_n.role_name].append(instance)

    def __getattr__(self, attr_name):
        return partial(_get_related, self, attr_name)


def _get_related(context, role_name, instance):
    the_class = instance.__class__
    assert hasattr(the_class, "_relationships"), "Role {} not found".format(role_name)

    relationship = the_class._relationships.get(role_name)
    assert relationship, "Role {} not found".format(role_name)

    if issubclass(relationship, Relationship1N):
        if role_name == relationship.role_1.role_name:
            return _get_related_1(context, relationship.role_1, relationship.role_n, instance)
        if role_name == relationship.role_n.role_name:
            return _get_related_n(context, relationship.role_n, relationship.role_1, instance)

    assert False, "Unknown role type"


def _get_related_1(context, role_1, role_n, instance):
    foreign_class = role_1.role_class
    foreign_key = getattr(instance, role_n.role_fk)
    if foreign_class in context._storage:
        foreign_instance = context._storage[foreign_class].get(foreign_key)
    else:
        foreign_instance = None
    return foreign_instance


def _get_related_n(context, role_n, role_1, instance):
    foreign_class = role_n.role_class
    if foreign_class in context._storage:
        foreign_instances = context._storage[foreign_class].values()
        return [
            i for i in foreign_instances
            if getattr(i, role_n.role_fk) == instance.id
        ]
    else:
        return []

