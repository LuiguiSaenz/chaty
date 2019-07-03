from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserResponseSerializer, UserResponse, \
                    GameSerializer, GameResponseSerializer, GameResponse
from rest_framework import permissions
from pruebaluigui.serializers import ErrorMessageResponseSerializer, ErrorMessageResponse
from pruebaluigui import api_errors
from rest_framework.utils.serializer_helpers import ReturnDict

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


class GameApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        
        try:
            invited_pk = request.data.get('invited')
            if invited_pk is None:
                return Response(ErrorMessageResponseSerializer(
                    ErrorMessageResponse(api_errors.INVITED_NOT_SENT)
                ).data)
                
            game_serializer = GameSerializer(data=request.data)
            if game_serializer.is_valid():
                print(1212)
                game = game_serializer.save()
                return Response(GameResponseSerializer(
                    GameResponse(game)
                ).data)
            else:
                errors = game_serializer.errors
                all_errors = ReturnDict(
                    list(errors.items()) + [("error_code",[1006])],
                    serializer = errors.serializer
                )
                return Response(all_errors,status = status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response(ErrorMessageResponseSerializer(
                ErrorMessageResponse(api_errors.ERROR)
            ).data)
        