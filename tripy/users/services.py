from .models import User
from utils.exceptions import IncorrectPassword, EmailAlreadyRegistered, EmailNotRegistered, InvalidUserId
from utils.password import get_hashed_password, check_password


def register_user(email, password, role):
    if User.objects.filter(email=email).exists():
        raise EmailAlreadyRegistered()
    user = create_user(email, password, role)
    return {
        "token": user.get_jwt_token()
    }


def login_user(email, password):
    if not User.objects.filter(email=email).exists():
        raise EmailNotRegistered()
    user = User.objects.get(email=email)
    if not check_password(password, user.password):
        raise IncorrectPassword()
    return {
        "token": user.get_jwt_token()
    }


def create_user(email, password, role):
    if User.objects.filter(email=email).exists():
        raise EmailAlreadyRegistered()
    hashed_password = get_hashed_password(password)
    user = User(
        email=email,
        password=hashed_password,
        role=role
    )
    user.save()
    return user


def edit_user(pk, password=None, **kwargs):
    if not User.objects.filter(pk=pk).exists():
        raise InvalidUserId()
    user = User.objects.get(pk=pk)
    if kwargs.get('email', '') != user.email:
        if User.objects.filter(email=kwargs.get('email', '')).exists():
            raise EmailAlreadyRegistered()

    if password not in [None, ""]:
        user.password = get_hashed_password(password)
    for key, value in kwargs.items():
        setattr(user, key, value)
    user.save()
    return user


def delete_user(pk):
    User.objects.filter(pk=pk).delete()
