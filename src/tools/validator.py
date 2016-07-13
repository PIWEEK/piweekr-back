from skame.validator import validate
from skame.schemas import base


class Validator:
    '''
    Base class to implement a validator of a set of input data (as a python dictionary)
    against a schema defined with "skame".

    If the input data matches the schema, then is_valid = True and you can read then
    validated (and perhaps cleaned) data in cleaned_data. If not, then is_valid = False,
    cleaned_data will be None and errors will be a dictionary with the failed fields and
    the error messages.
    '''
    schema = None

    def __init__(self, data: dict):
        (self.cleaned_data, self.errors) = validate(self.schema, data)

    def is_valid(self) -> bool:
        return not bool(self.errors)

