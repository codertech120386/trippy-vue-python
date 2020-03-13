from django.core.paginator import Paginator
import datetime
from .models import Trip
from .serializers import TripFullSerializer, TripSerializer


def get_all_trips(q="", page=1):
    q = q.lower()
    trips = [trip for trip in Trip.objects.all() if q in trip.search_blob()]
    pager = Paginator(trips, 6)
    if page in pager.page_range:
        page_trips = pager.page(page).object_list
    else:
        page_trips = []
    return TripFullSerializer(page_trips, many=True).data, pager.num_pages


def get_trips_for_user(user_id, q="", page=1, days=None):
    q = q.lower()
    trips = Trip.objects.filter(user_id=user_id)
    if days:
        today = datetime.date.today()
        cutoff = today + datetime.timedelta(days=days)
        trips = trips.filter(start_date__gte=today, start_date__lte=cutoff)
    trips = [trip for trip in trips if q in trip.search_blob()]
    pager = Paginator(trips, 6)
    if page in pager.page_range:
        page_trips = pager.page(page).object_list
    else:
        page_trips = []
    return TripSerializer(page_trips, many=True).data, pager.num_pages
