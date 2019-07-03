from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserResponseSerializer, UserResponse, \
                    GameSerializer, GameResponseSerializer, GameResponse, \
                    GameListResponseSerializer, GameListResponse, \
                    GameListSerializer, MoveResponseSerializer, \
                    MoveSerializer, MoveResponse
from rest_framework import permissions
from pruebaluigui.serializers import ErrorMessageResponseSerializer, ErrorMessageResponse
from pruebaluigui import api_errors
from rest_framework.utils.serializer_helpers import ReturnDict
from api.models import Game

######### LISTA DE USUARIOS ###############
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


######### CREACIÓN DE JUEGO ###############
class GameApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        
        try:
            invited_pk = request.data.get('invited')
            if invited_pk is None:
                return Response(ErrorMessageResponseSerializer(
                    ErrorMessageResponse(api_errors.INVITED_NOT_SENT)
                ).data)

            data = request.data.dict()
            data["creator"] = request.user.id
            game_serializer = GameSerializer(data=data)

            if game_serializer.is_valid():
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


######### LISTA DE JUEGOS ###############
class GameList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        try:
            return Response(GameListResponseSerializer(
                    GameListResponse()
                ).data)
        except:
            return Response(ErrorMessageResponseSerializer(
                ErrorMessageResponse(api_errors.ERROR)
            ).data)


######### DETALLE DE JUEGO ###############
class GameDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, identifier, format=None):
        
        try:
            game = Game.objects.get(identifier=identifier)
        except:
            return Response(ErrorMessageResponseSerializer(
                ErrorMessageResponse(api_errors.IDENTIFIER_INVALID_SENT)
            ).data)
        
        return Response(GameListSerializer(game, many=False).data)


######### CREACIÓN DE MOVIMIENTO ###############
class MoveApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, identifier, format=None):
        try:
            game = Game.objects.get(identifier=identifier)
        except:
            return Response(ErrorMessageResponseSerializer(
                ErrorMessageResponse(api_errors.IDENTIFIER_INVALID_SENT)
            ).data)
        
        if game.status == 'done':
            return Response(ErrorMessageResponseSerializer(
                ErrorMessageResponse(api_errors.GAME_DONE)
            ).data)
        
        data = request.data.dict()
        data["player"] = request.user.id
        data["identifier"] = identifier
        move_serializer = MoveSerializer(data=data)
        if move_serializer.is_valid():
            move = move_serializer.save()
            return Response(MoveResponseSerializer(
                MoveResponse(move)
            ).data)
        else:
            errors = move_serializer.errors
            all_errors = ReturnDict(
                list(errors.items()) + [("error_code",[1006])],
                serializer = errors.serializer
            )
            return Response(all_errors,status = status.HTTP_400_BAD_REQUEST)