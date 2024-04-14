from django.contrib.auth import get_user_model
from django.shortcuts import redirect

class CheckAuthenticationForCheckout:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/checkout') and not request.user.is_authenticated:
            return redirect('/')

        response = self.get_response(request)
        return response