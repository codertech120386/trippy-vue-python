from django.core.paginator import Paginator
from .models import User
from .serializers import UserSerializer


def get_users(q="", page=1):
    q = q.lower()
    users = [user for user in User.objects.all() if q in user.search_blob()]
    pager = Paginator(users, 6)
    if page in pager.page_range:
        page_users = pager.page(page).object_list
    else:
        page_users = []
    return UserSerializer(page_users, many=True).data, pager.num_pages


def get_user_by_email(email):
    return User.objects.filter(email=email).first()
