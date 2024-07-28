from django.core.exceptions import PermissionDenied
from functools import wraps

def manager_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userprofile.role == 'Manager':
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view

def teamlead_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userprofile.role == 'Team Lead':
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view