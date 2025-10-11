    # accounts/decorators.py
from django.shortcuts import redirect
from django.contrib import messages

def seller_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'seller':
            return view_func(request, *args, **kwargs)
        messages.error(request, "You are not authorized to view this page.")
        return redirect('home')
    return wrapper