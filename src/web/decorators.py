from anillo.http import responses

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        if getattr(request, "user"):
            return func(self, request, *args, **kwargs)
        else:
            return responses.Unauthorized()
    return wrapper

