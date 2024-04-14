from .models import ResetPassword
from django.utils.crypto import get_random_string
import time
from datetime import datetime, timedelta

def CreateToken():
    now = str(time.time())
    random_string = str(get_random_string(30))

    token = random_string + '&' + now + '@'
    return token


def CheckLinkExpire(user_id):
    reset_password = ResetPassword.objects.filter(user_id=user_id).filter(is_used=False).last()

    if reset_password and reset_password.created_at.timestamp() + 900 >= time.time():
        return True

    return False