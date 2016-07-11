from anillo.http import responses

from core.users import user_actions
# from core import exceptions

from tools.adt.converter import to_plain, from_plain

# from web.api.decorators import login_required


# @login_required
def list_users(request):
    users = user_actions.list_users()
    return responses.Ok([to_plain(user) for user in users])

