import os.path

from anillo.handlers.routing import router as anillo_router, optionized_url as url
from anillo.http import responses

from web.api.users import user_handlers
from web.api.ideas import idea_handlers

PREFIX = "/api/v1"

urls = [
    url(PREFIX + "/users", user_handlers.list_users, methods=["get"]),
    url(PREFIX + "/ideas", idea_handlers.list_ideas, methods=["get"]),
]

router = anillo_router(urls)
