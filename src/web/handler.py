from anillo.http import responses

class Handler:
    def __call__(self, request, *args, **kwargs):
        method = request.method.lower()
        handler = getattr(self, method)
        if handler:
            return handler(request, *args, **kwargs)
        else:
            return responses.MethodNotAllowed()

