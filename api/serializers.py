from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Game
import uuid
########### PLAYERS ##################
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=200)

class UserResponseSerializer(serializers.Serializer):
    players = serializers.ListField()
    message = serializers.CharField()

class UserResponse(object):

    def __init__(self):
        users = User.objects.all()
        serializers = UserSerializer(users, many=True)
        self.players = serializers.data
        self.message = "Success"

########### GAME #####################

class GameSerializer(serializers.Serializer):
    invited = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        super(GameSerializer, self).__init__(*args, **kwargs)
        self.fields["invited"].error_messages["required"] = "This field is required"
        self.fields["invited"].error_messages["null"] = "This field can't be null"
        self.fields["invited"].error_messages["blank"] = "This field can't be empty"

    def validate_invited(self, value):
        print(value, "invited")
        if isinstance(value, int):
            return value
        else:
            raise serializers.ValidationError('Id of invited is not integer')

    def create(self, request, validated_data):
        print(validated_data)
        invited_id = validated_data['invited']
        print(validated_data)
        identifier = uuid.uuid4().hex
        pass
        """ game = Game.objects.create(
                            identifier=identifier,
                            player1=req
        ) """

class GameResponseSerializer(serializers.Serializer):
    game = serializers.DictField()

class GameResponse(object):

    def __init__(self):
        users = User.objects.all()
        serializers = UserSerializer(users, many=True)
        self.players = serializers.data
        self.message = "Success"