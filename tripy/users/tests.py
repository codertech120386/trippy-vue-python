from django.test import TestCase
from .models import User
from .services import create_user, delete_user


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = create_user("a@g.com", "test123", "user")

    def test_token(self):
        token = self.user.get_jwt_token()
        user = User.from_token(token)
        self.assertEqual(user, self.user)


class UserServiceTestCase(TestCase):
    def test_create_user(self):
        users = User.objects.all()
        self.assertEqual(len(users), 0)
        user = create_user("a@g.com", "test123", "user")
        users = User.objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(user, users[0])

    def test_delete_user(self):
        users = User.objects.all()
        self.assertEqual(len(users), 0)
        user = create_user("a@g.com", "test123", "user")
        users = User.objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(user, users[0])
        delete_user(user.pk)
        users = User.objects.all()
        self.assertEqual(len(users), 0)
