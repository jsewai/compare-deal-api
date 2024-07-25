from knox.auth import TokenAuthentication
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import APIException, ValidationError, ParseError
from rest_framework.settings import api_settings
from user.serializers import UserSerializer
from rest_framework.response import Response
from knox.models import AuthToken, AuthTokenManager
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from core.models import User
from rest_framework.views import APIView


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(
                user,
                context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({
            'user': {
                "name": user.name,
                "email": user.email,
            },
            "token": AuthToken.objects.create(user)[1]
        })
