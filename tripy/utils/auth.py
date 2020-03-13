from rest_framework import authentication
from rest_framework import permissions
from users.models import User
from utils.exceptions import InvalidToken


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:  # no token passed in request headers
            raise InvalidToken()
        try:
            user = User.from_token(token)  # get the user
        except Exception:
            raise InvalidToken()
        return (user, None)  # authentication successfull


class TripPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user:
            return False
        else:
            return request.user.role in ['user', 'admin']


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user:
            return False
        else:
            return request.user.role in ['user_manager', 'admin']
