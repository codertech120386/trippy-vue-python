import jwt
from django.db import models
from django.conf import settings
from utils.abstract_models import Base


ROLE_ADMIN = "admin"
ROLE_USER_MANAGER = "user_manager"
ROLE_USER = "user"


class User(Base):
    ROLES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_USER_MANAGER, "User Manager"),
        (ROLE_USER, "User"),
    )
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(choices=ROLES, max_length=50)

    def get_jwt_token(self):
        payload = {
            "user_id": self.pk,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
        return token

    def search_blob(self):
        return "::".join([self.email, self.role]).lower()

    @classmethod
    def from_token(cls, token):
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return cls.objects.get(pk=payload['user_id'])

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
