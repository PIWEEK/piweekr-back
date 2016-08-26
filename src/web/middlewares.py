from anillo.http import responses
import json

from core.users import user_actions
from web.api import exceptions as api_exceptions

import settings


def wrap_verify_user(func):

    def wrapper(request, *args, **kwargs):
        user_id = request.get('identity', {}).get('user_id', None)
        request.user = user_actions.get_by_id(user_id) if user_id else None
        return func(request, *args, **kwargs)

    return wrapper


def wrap_error_handler(func):

    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)

        except api_exceptions.NotFound as ex:
            return responses.NotFound(**_render_error(ex))

        except api_exceptions.Forbidden as ex:
            return responses.Forbidden(**_render_error(ex))

        except api_exceptions.BadRequest as ex:
            return responses.BadRequest(**_render_error(ex))

        except Exception as ex:
            if settings.DEBUG == False:
                return responses.InternalServerError(**_render_error(ex, "Internal error: {}".format(str(ex))))
            else:
                from werkzeug.debug.tbtools import get_current_traceback
                traceback = get_current_traceback()
                return responses.InternalServerError(
                    traceback.plaintext,
                    headers={"Content-type": "text/plain"}
                )

    return wrapper


def _render_error(ex, message = None):
    info = {
        "code": getattr(ex, "code", "generic_error"),
        "detail": message if message else str(ex),
    }
    return {"body": json.dumps(info), "headers": {"Content-Type": "application/json"}}

