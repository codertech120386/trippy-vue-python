import datetime
from django.test import TestCase
from users.services import create_user
from .models import Trip
from .services import create_trip, edit_trip, delete_trip


class TripModelTestCase(TestCase):
    def setUp(self):
        self.user = create_user("a@g.com", "test123", "user")
        start = datetime.date.today() + datetime.timedelta(days=10)
        end = datetime.date.today() + datetime.timedelta(days=12)
        self.user.save()
        self.trip = Trip(user=self.user, destination="Test", comment="test", start_date=start, end_date=end)
        self.trip.save()

    def test_days_left(self):
        self.assertEqual(self.trip.days_left(), 10)


class TripServiceTestCase(TestCase):
    def setUp(self):
        self.user = create_user("a@g.com", "test123", "user")
        self.user.save()

    def test_create_trips(self):
        trips = Trip.objects.filter(user=self.user)
        self.assertEqual(len(trips), 0)
        start = datetime.date.today() + datetime.timedelta(days=10)
        end = datetime.date.today() + datetime.timedelta(days=12)
        trip = create_trip(self.user.email, start, end, "Test", "test")
        trips = Trip.objects.filter(user=self.user)
        self.assertEqual(len(trips), 1)
        self.assertEqual(trips[0], trip)

    def test_edit_trips(self):
        start = datetime.date.today() + datetime.timedelta(days=10)
        end = datetime.date.today() + datetime.timedelta(days=12)
        trip = Trip(user=self.user, destination="Test", comment="test", start_date=start, end_date=end)
        trip.save()
        new_start = datetime.date.today() + datetime.timedelta(days=15)
        new_end = datetime.date.today() + datetime.timedelta(days=20)
        trip = edit_trip(trip.pk, self.user.email, start_date=new_start, end_date=new_end)
        self.assertEqual(trip.start_date, new_start)
        self.assertEqual(trip.end_date, new_end)

    def test_delete_trips(self):
        start = datetime.date.today() + datetime.timedelta(days=10)
        end = datetime.date.today() + datetime.timedelta(days=12)
        trip = Trip(user=self.user, destination="Test", comment="test", start_date=start, end_date=end)
        trip.save()
        delete_trip(trip.pk)
        self.assertFalse(Trip.objects.filter(pk=trip.pk).exists())
