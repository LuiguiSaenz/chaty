from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
# Create your tests here.

class LoginTest(APITestCase):
    def setUp(self):
        pass

    def test_animals_can_speak(self):
        client = APIClient()
        client.login(username='lauren', password='secret')