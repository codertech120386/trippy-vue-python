from .models import User
from utils import exceptions


def validate_new_user_email(email):
    if User.objects.filter(email=email).exists():
        raise exceptions.EmailAlreadyRegistered()
    return email


def validate_existing_user_email(email):
    if not User.objects.filter(email=email).exists():
        raise exceptions.EmailNotRegistered()
    return email
