from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=200)

class UserResponseSerializer(serializers.Serializer):
    players = serializers.ListField()
    message = serializers.CharField()

class UserResponse(object):

    def __init__(self):
        users = User.objects.all()
        print(users)
        serializers = UserSerializer(users, many=True)  
        print(serializers.data)
        self.players = serializers.data
        self.message = "Success"