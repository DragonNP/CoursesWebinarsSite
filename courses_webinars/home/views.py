from django.shortcuts import redirect


def index(request):
    if request.user.is_authenticated:
        return redirect(f'/accounts/profile')
    else:
        return redirect(f'accounts/login')
