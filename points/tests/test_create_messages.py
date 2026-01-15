from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point as geoPoint
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from points.models import Message, Point

CREATE_MESSAGE_URL = "/api/points/messages/"
CREATE_POINT_URL = "/api/points/"

User = get_user_model()


class TestCreateMessage(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", password="passuser")
        cls.token = Token.objects.create(user=cls.user)

    def auth_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def create_point(self):
        point = Point.objects.create(
            user=self.user, location=geoPoint(2.15899, 41.3888, srid=4326)
        )
        return point

    def test_create_message_no_auth(self):
        self.client.credentials()
        messages_before = Message.objects.count()
        point = self.create_point()
        response = self.client.post(
            CREATE_MESSAGE_URL, {"text": "Hello!", "point": point.id}, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        self.assertEqual(messages_before, Message.objects.count())

    def test_create_message_with_auth(self):
        self.auth_token()
        messages_before = Message.objects.count()
        point = self.create_point()
        response = self.client.post(
            CREATE_MESSAGE_URL, {"text": "Hello!", "point": point.id}, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Message.objects.count() == messages_before + 1
        message = Message.objects.get(id=response.data["id"])
        self.assertEqual(message.text, "Hello!")

    def test_create_message_set_user(self):
        self.auth_token()
        point = self.create_point()
        response = self.client.post(
            CREATE_MESSAGE_URL,
            {"text": "Hello!", "point": point.id, "author": 150},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        message = Message.objects.get(id=response.data["id"])
        self.assertEqual(message.author, self.user)
        self.assertNotEqual(message.author.id, 150)

    def test_create_message_unvalidated(self):
        self.auth_token()
        messages_before = Message.objects.count()
        point = self.create_point()
        response = self.client.post(
            CREATE_MESSAGE_URL, {"text": "", "point": point.id}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self.assertEqual(messages_before, Message.objects.count())
