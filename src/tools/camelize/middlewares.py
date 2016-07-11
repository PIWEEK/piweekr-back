# -*- coding: utf-8  -*-
from cgi import parse_header

import functools

from .utils import camelize
from .utils import underscoreize


def wrap_camelize_response_body(func=None):
    """
    A middleware that camelize the response body in case
    of that the "Content-Type" header is "application/json".
    """
    if func is None:
        return functools.partial(wrap_camelize_response_body, encoder=encoder)

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)

        if "Content-Type" in response.headers and response.headers['Content-Type'] is not None:
            ctype, pdict = parse_header(response.headers.get('Content-Type', ''))
            if ctype == "application/json" and (isinstance(response.body, dict) or
                                                isinstance(response.body, list)):
                response.body = camelize(response.body)
        return response
    return wrapper


def wrap_underscoreize_request_body(func=None):
    """
    A middleware that parses the body of requests and underscoreize
    it to the request under the `body` attribute (replacing
    the previous value). Can preserve the original value in
    a new attribute `raw_body` if you give preserve_raw_body=True.
    """

    if func is None:
        return functools.partial(
            wrap_underscoreize_request_body,
        )

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        ctype, pdict = parse_header(request.headers.get('Content-Type', ''))
        if ctype == "application/json":
            request.body = underscoreize(request.body)
        return func(request, *args, **kwargs)
    return wrapper
