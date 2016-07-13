import os.path

from anillo.handlers.routing import router as anillo_router, optionized_url as url
from anillo.http import responses

from web.api.users import user_handlers
from web.api.ideas import idea_handlers
from web.api.projects import project_handlers

PREFIX = "/api/v1"

urls = [
    url(PREFIX + "/login", user_handlers.Login(), methods=["post"]),
    url(PREFIX + "/logout", user_handlers.Logout(), methods=["post"]),
    url(PREFIX + "/users", user_handlers.UsersList(), methods=["get"]),
    url(PREFIX + "/ideas", idea_handlers.IdeasList(), methods=["get", "post"]),
    url(PREFIX + "/projects", project_handlers.ProjectsList(), methods=["get"]),
]

router = anillo_router(urls)
