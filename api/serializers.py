from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Game
import uuid
import arrow
from django.db.models import Q

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
    creator = serializers.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super(GameSerializer, self).__init__(*args, **kwargs)
        self.fields["invited"].error_messages["required"] = "This field is required"
        self.fields["invited"].error_messages["null"] = "This field can't be null"
        self.fields["invited"].error_messages["blank"] = "This field can't be empty"

    def validate_invited(self, value):
        if isinstance(value, int):
            if value == self.initial_data["creator"]:
                raise serializers.ValidationError('You can not play with yourself')
            
            invited_exists = User.objects.filter(pk=value).exists()
            if not invited_exists:
                raise serializers.ValidationError('The invited user does not exist')

            game = Game.objects.filter(Q(player1_id=value,
                                   status="progress") |
                                   Q(player2_id=value,
                                   status="progress")).exists()
            if game:
                raise serializers.ValidationError('The invited user is participating in a game in progress')
            
            return value
        else:
            raise serializers.ValidationError('Id of invited is not integer')

    def validate_creator(self, value):
        game = Game.objects.filter(Q(player1_id=value,
                                   status="progress") |
                                   Q(player2_id=value,
                                   status="progress")).exists()
        if game:
            raise serializers.ValidationError('You are already participating in a game in progress')

        return value
        
    def create(self, validated_data):
        creator = User.objects.get(pk=validated_data.get("creator"))
        invited = User.objects.get(pk=validated_data.get("invited"))
        identifier = uuid.uuid4().hex
        board = [None] * 9
        game = Game.objects.create(
                            identifier=identifier,
                            player1=creator,
                            player2=invited,
                            status="progress",
                            board=board
        )
        game.save()
        return game

class GameResponseSerializer(serializers.Serializer):
    game = serializers.DictField()

class GameResponse(object):

    def __init__(self, game):
        game_info = {}
        game_info["status"] = game.status
        game_info["created"] = arrow.get(game.created_at).shift(hours=-5).format('YYYY-MM-DD HH:mm')
        game_info["identifier"] = game.identifier
        self.game = game_info


########### GAME LIST #########################
class GameListSerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=200)
    status = serializers.CharField(max_length=200)
    creation = serializers.SerializerMethodField()
    players = serializers.SerializerMethodField()
    board = serializers.SerializerMethodField()
    winner = serializers.SerializerMethodField()
    class Meta:
        model = Game

    def get_creation(self, game):
        created_at = arrow.get(game.created_at).shift(hours=-5).format('YYYY-MM-DD HH:mm')
        return created_at

    def get_players(self, game):
        players =[]
        player = {}
        player["id"] = game.player1.id
        players.append(player)
        player = {}
        player["id"] = game.player2.id
        players.append(player)
        return players   

    def get_board(self, game):
        return game.board 
    
    def get_winner(self, game):
        if game.winner:
            return game.winner.id
        
        return None


class GameListResponseSerializer(serializers.Serializer):
    games = serializers.ListField()
    message = serializers.CharField()

class GameListResponse(object):

    def __init__(self):
        games = Game.objects.all()
        serializers = GameListSerializer(games, many=True)
        self.games = serializers.data
        self.message = "Success"


################ MOVE CREATION #################
class MoveSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    player = serializers.IntegerField(required=False)
    identifier = serializers.CharField(required=False, max_length=200)

    def __init__(self, *args, **kwargs):
        super(MoveSerializer, self).__init__(*args, **kwargs)
        self.fields["position"].error_messages["required"] = "This field is required"
        self.fields["position"].error_messages["null"] = "This field can't be null"
        self.fields["position"].error_messages["blank"] = "This field can't be empty"

    def validate_position(self, value):
        if isinstance(value, int):
            if value > 8:
                raise serializers.ValidationError('The position should be in the range of 0 to 8')

            game = Game.objects.get(identifier=self.initial_data["identifier"])
            if game.board[value]:
                raise serializers.ValidationError('The selected position is already used')

            return value
        else:
            raise serializers.ValidationError('Position is not integer')

    def validate_player(self, value):
        game = Game.objects.filter(Q(player1_id=value, 
                                    identifier=self.initial_data["identifier"]) |
                                   Q(player2_id=value,
                                   identifier=self.initial_data["identifier"]))
        if game.exists():
            if game.first().last_move == value:
                raise serializers.ValidationError('It\'s the turn of the other player')
            
            return value
        else:
            raise serializers.ValidationError('The user is not in this game')

    def create(self, validated_data):
        game = Game.objects.get(identifier=validated_data.get("identifier"))
        game.last_move = validated_data.get("player")

        board = game.board
        board[validated_data.get("position")] = validated_data.get("player")
        game.board = board
        # validamos si ha ganado
        # filas
        index = 0
        while index < len(board):
            if board[index] is None:
                index = index + 3
                continue
            if board[index] == board[index+1] and board[index+1] == board[index+2]:
                game.winner_id = validated_data.get("player")
                game.status = 'done'
                game.save()
                return game
            index = index + 3
        # columnas
        index = 0
        while index < (len(board)/3):
            if board[index] is None:
                index = index + 1
                continue
            if board[index] == board[index+3] and board[index+3] == board[index+6]:
                game.winner_id = validated_data.get("player")
                game.status = 'done'
                game.save()
                return game
            index = index + 1
        # Diagonales
        if board[0] and board[0] == board[4] and board[4] == board[8]:
            game.winner_id = validated_data.get("player")
            game.status = 'done'
            game.save()
            return game
        if board[2] and board[2] == board[4] and board[4] == board[6]:
            game.winner_id = validated_data.get("player")
            game.status = 'done'
            game.save()
            return game

        # Cuando hay un empate
        available_positions = board.count(None)
        if available_positions == 0:
            game.status = 'done'
        game.save()
        return game

class MoveResponseSerializer(serializers.Serializer):
    game = serializers.DictField()

class MoveResponse(object):

    def __init__(self, game):
        game_info = {}
        game_info["status"] = game.status
        game_info["board"] = game.board
        game_info["winner"] = game.winner.id if game.winner else None
        self.game = game_info


class MoveDetailSerializer(serializers.Serializer):
    board = serializers.SerializerMethodField()
    class Meta:
        model = Game
    
    def get_board(self, game):
        return game.board 