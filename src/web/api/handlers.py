from anillo.http import responses

# from core import actions
# from core import exceptions

# from web.api.decorators import login_required


# @login_required
def dummy(request):
    return responses.Ok({
        1: "one",
        2: "two",
    })

