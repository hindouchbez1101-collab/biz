from functools import wraps
from django.http import HttpResponseForbidden

GROUP_RECEPTION  = "RECEPTION"
GROUP_GERANT     = "GERANT"
GROUP_ADMIN      = "ADMIN"
GROUP_PHARMACIE  = "PHARMACIE"

def in_groups(user, allowed):
    if not user.is_authenticated:
        return False
    user_groups = set(user.groups.values_list("name", flat=True))
    if user.is_superuser:
        return True
    return bool(user_groups.intersection(set(allowed)))

def require_groups(*allowed):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not in_groups(request.user, allowed):
                return HttpResponseForbidden("Accès refusé.")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
