from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserResponseSerializer, UserResponse
from rest_framework import permissions
from pruebaluigui.serializers import ErrorMessageResponseSerializer, ErrorMessageResponse
from pruebaluigui import api_errors


class UserList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        try:
            return Response(UserResponseSerializer(
                    UserResponse()
                ).data)
        except:
            return Response(ErrorMessageResponseSerializer(
                ErrorMessageResponse(api_errors.ERROR)
            ).data)
        