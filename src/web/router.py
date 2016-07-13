import os.path

from anillo.handlers.routing import router as anillo_router, optionized_url as url
from anillo.http import responses

from web.api.users import user_handlers
from web.api.ideas import idea_handlers
from web.api.projects import project_handlers

PREFIX = "/api/v1"

urls = [
    # User
    url(PREFIX + "/login", user_handlers.Login(), methods=["post"]),
    url(PREFIX + "/logout", user_handlers.Logout(), methods=["post"]),
    url(PREFIX + "/users", user_handlers.UsersList(), methods=["get"]),
    url(PREFIX + "/users/<string:username>", user_handlers.UserDetail(), methods=["get", "patch", "delete"]),

    # Ideas
    url(PREFIX + "/ideas",
        idea_handlers.IdeasList(), methods=["get", "post"]),
    url(PREFIX + "/ideas/<string:idea_uuid>",
        idea_handlers.IdeaDetail(), methods=["get", "put", "delete"]),
    url(PREFIX + "/ideas/<string:idea_uuid>/invited",
        idea_handlers.IdeaInvitedList(), methods=["get", "post", "delete"]),
    url(PREFIX + "/ideas/<string:idea_uuid>/comments",
        idea_handlers.IdeaComentsList(), methods=["get", "post", "delete"]),

    # Projects
    url(PREFIX + "/projects",
        project_handlers.ProjectsList(), methods=["get"]),
    url(PREFIX + "/projects/<string:project_uuid>/comments",
        project_handlers.ProjectComentsList(), methods=["get", "post", "delete"]),
]

router = anillo_router(urls)
