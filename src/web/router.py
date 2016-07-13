import os.path

from anillo.handlers.routing import router as anillo_router, optionized_url as url
from anillo.http import responses

from web.api.users import user_handlers
from web.api.ideas import idea_handlers
from web.api.projects import project_handlers

PREFIX = "/api/v1"

urls = [
    url(PREFIX + "/login", user_handlers.login, methods=["post"]),
    url(PREFIX + "/logout", user_handlers.logout, methods=["post"]),
    url(PREFIX + "/users", user_handlers.list_users, methods=["get"]),
    url(PREFIX + "/ideas", idea_handlers.list_ideas, methods=["get"]),
    url(PREFIX + "/projects", project_handlers.list_projects, methods=["get"]),
]

router = anillo_router(urls)
