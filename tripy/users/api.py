from rest_framework import serializers, generics
from utils.responses import success_response
from utils.exceptions import InputValidationError
from utils.auth import JWTAuthentication, UserPermission
from .services import register_user, login_user, create_user, edit_user, delete_user
from .selectors import get_users
from .validations import validate_new_user_email, validate_existing_user_email
import logging
logger = logging.getLogger('django')


class RegisterUserView(generics.GenericAPIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()
        role = serializers.CharField()

        def validate(self, data):
            data = super().validate(data)
            data['email'] = validate_new_user_email(data['email'])
            return data

    serializer_class = InputSerializer

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        if not serializer.is_valid():
            raise InputValidationError("some of your inputs are missing or not valid")

        email, password, role = [serializer.data[key] for key in ['email', 'password', 'role']]
        token = register_user(email, password, role)
        return success_response(message="User registered in successfully", data=token)


class LoginUserView(generics.GenericAPIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    def validate(self, data):
        logger.debug("inside validate method")
        data = super().validate(data)
        data['email'] = validate_existing_user_email(data['email'])
        return data

    serializer_class = InputSerializer

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        if not serializer.is_valid():
            raise InputValidationError("One of your inputs is not valid")

        email, password = [serializer.data[key] for key in ['email', 'password']]
        token = login_user(email, password)
        return success_response(message="User logged in successfully", data=token)


class UserViewSet(generics.GenericAPIView):
    permission_classes = [UserPermission]
    authentication_classes = [JWTAuthentication]

    class AddSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()
        role = serializers.CharField()

    class EditSerializer(serializers.Serializer):
        email = serializers.EmailField()
        pk = serializers.IntegerField()
        role = serializers.CharField()

    def get(self, request):
        q = request.GET.get('q', "")
        page = int(request.GET.get('page', 1))
        users, total_pages = get_users(q=q, page=page)
        return success_response(data={
            "users": users,
            "total_pages": total_pages
        })

    def post(self, request):
        serializer = self.AddSerializer(data=request.data)
        if not serializer.is_valid():
            raise InputValidationError("some of your inputs are missing or not valid")
        create_user(**request.data)
        return success_response(message="User Created Successfully")

    def put(self, request):
        serializer = self.EditSerializer(data=request.data)
        if not serializer.is_valid():
            raise InputValidationError("some of your inputs are missing or not valid")
        edit_user(**request.data)
        return success_response(message="User Edited Successfully")

    def delete(self, request):
        delete_user(**request.data)
        return success_response(message="User Deleted Successfully")


class VerifyUserView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return success_response(message="", data={
            "role": request.user.role,
            "id": request.user.id
        })
