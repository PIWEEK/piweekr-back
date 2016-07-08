import sys
import os


def setup_application():
    import settings

    from anillo.app import application
    from anillo.utils.common import chain
    from anillo.middlewares.json import wrap_json_body, wrap_json_response
    from anillo.middlewares.cors import wrap_cors, DEFAULT_HEADERS
    from anillo.middlewares.default_headers import wrap_default_headers
    from anillo.middlewares.params import wrap_query_params
    # from .middlewares import wrap_auth, error_handler
    from .router import router

    handler = chain(
        wrap_cors(allow_headers=list(DEFAULT_HEADERS) + ["x-session-id", "accept-language", "authorization"]),
        # error_handler,
        # wrap_auth(secret=settings.PIWEEKR_SECRET),
        wrap_json_body(),
        wrap_json_response,
        wrap_default_headers({}, {"Content-Type": "application/json"}),
        wrap_query_params,
        router
    )

    return application(handler)


def runserver(livereload = False):
    app = setup_application()

    if livereload:
        from livereload import Server
        server = Server(app)
        server.watch(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'dist'))
        server.serve(port=5000, host='0.0.0.0')
    else:
        from anillo import serving
        serving.run_simple(app, port=5000, host='0.0.0.0')

