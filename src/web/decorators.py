from anillo.http import responses

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if getattr(request, "user"):
            return func(request, *args, **kwargs)
        else:
            return responses.Unauthorized()
    return wrapper
