from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import uuid
# Create your models here.
class Game(models.Model):
    identifier = models.UUIDField(unique=True,
        default=uuid.uuid4
    )

    status = models.CharField(
        max_length=200
    )

    player1 = models.ForeignKey(
        User,
        related_name="player1"
    )

    player2 = models.ForeignKey(
        User
    )

    winner = models.CharField(
        max_length=500,
        null=True
    )

    board = ArrayField(models.IntegerField(null=True),size=9)
    

    created_at = models.DateTimeField(
       auto_now_add=True,
       editable=False
    )