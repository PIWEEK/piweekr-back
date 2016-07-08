import os.path

from anillo.handlers.routing import router as anillo_router, optionized_url as url
from anillo.http import responses

from web.api import handlers

urls = [
    url("/", handlers.dummy, methods=["get"]),
]

router = anillo_router(urls)
