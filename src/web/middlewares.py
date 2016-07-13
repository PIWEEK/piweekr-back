from core.users import user_actions


def wrap_verify_user(func):

    def wrapper(request, *args, **kwargs):
        user_id = request.get('identity', {}).get('user_id', None)
        request.user = user_actions.get_by_id(user_id) if user_id else None
        return func(request, *args, **kwargs)

    return wrapper

