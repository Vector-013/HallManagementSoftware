from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from functools import wraps


# def student_required(
#     function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="login"
# ):
#     """
#     Decorator for views that checks that the logged in user is a student,
#     redirects to the log-in page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and u.role == "student",
#         login_url=login_url,
#         redirect_field_name=redirect_field_name,
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator


def hall_clerk_access_only():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not (request.appuser.role == "hall_clerk"):
                return HttpResponse(
                    "You are not a student and \
                        you are not allowed to access this page !"
                )
            return view(request, *args, **kwargs)

        return _wrapped_view

    return decorator
