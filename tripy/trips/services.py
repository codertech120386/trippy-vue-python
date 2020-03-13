from users.selectors import get_user_by_email
from utils.exceptions import EmailNotRegistered, InvalidTripId
from .models import Trip


def create_trip(user_email, start_date, end_date, destination, comment):
    user = get_user_by_email(user_email)
    if not user:
        raise EmailNotRegistered()
    trip = Trip(
        user_id=user.pk,
        start_date=start_date,
        end_date=end_date,
        destination=destination,
        comment=comment
    )
    trip.save()
    return trip


def edit_trip(pk, user_email, **kwargs):
    user = get_user_by_email(user_email)
    if not user:
        raise EmailNotRegistered()
    if not Trip.objects.filter(pk=pk).exists():
        raise InvalidTripId()
    trip = Trip.objects.get(pk=pk)
    trip.user_id = user.pk
    for key, value in kwargs.items():
        setattr(trip, key, value)
    trip.save()
    return trip


def delete_trip(pk):
    Trip.objects.filter(pk=pk).delete()
