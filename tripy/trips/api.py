from rest_framework import generics
from utils.responses import success_response
from utils.exceptions import InputValidationError
from utils.auth import JWTAuthentication, TripPermission
from .serializers import TripSerializer
from .selectors import get_all_trips, get_trips_for_user
from .services import delete_trip, edit_trip, create_trip


class TripViewSet(generics.GenericAPIView):
    permission_classes = [TripPermission]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        q = request.GET.get('q', '')
        page = int(request.GET.get('page', 1))
        days = int(request.GET['days']) if 'days' in request.GET else None

        if request.user.role == 'admin':
            trips, total_pages = get_all_trips(q, page)
        else:
            trips, total_pages = get_trips_for_user(request.user.pk, q, page, days)
        return success_response(data={
            "trips": trips,
            "total_pages": total_pages
        })

    def post(self, request):
        serializer = TripSerializer(data=request.data)
        if not serializer.is_valid():
            raise InputValidationError("some of your inputs are missing or not valid")
        if 'user_email' not in request.data:
            create_trip(user_email=request.user.email, **request.data)
        else:
            create_trip(**request.data)
        return success_response(message="Trip Created Successfully")

    def put(self, request):
        serializer = TripSerializer(data=request.data)
        if not serializer.is_valid():
            raise InputValidationError("some of your inputs are missing or not valid")
        if 'user_email' not in request.data:
            edit_trip(user_email=request.user.email, **request.data)
        else:
            edit_trip(**request.data)
        return success_response(message="Trip edited Successfully")

    def delete(self, request):
        delete_trip(**request.data)
        return success_response(message="Trip deleted Successfully")
