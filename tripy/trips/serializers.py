from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Trip


class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ['pk', 'start_date', 'end_date', 'destination', 'comment', 'days_left']
        read_only = ('pk', 'days_left')


class TripFullSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trip
        fields = ['pk', 'start_date', 'end_date', 'destination', 'comment', 'user', 'days_left']
