from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, resolve_url

def confirm_staff(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.user_role == 'S':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Unauthorised access')
            return redirect("cvapp:logout")
    return wrapper