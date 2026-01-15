from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point as geoPoint
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from points.models import Message, Point

CREATE_URL = "/api/points/"
SEARCH_URL_NEXT = (
    "/api/points/messages/search/?latitude=41.3888&longitude=2.15899&radius=3"
)
SEARCH_URL_FAR = (
    "/api/points/messages/search/?latitude=41.3888&longitude=2.15899&radius=3000"
)
SEARCH_URL_WRONG = (
    "/api/points/messages/search/?latitude=41.3888&longitude=2.15899&radius=-3"
)

User = get_user_model()


class TestSearchMessages(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", password="passuser")
        cls.token = Token.objects.create(user=cls.user)

    def auth_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def create_message_next(self):
        point = Point.objects.create(
            user=self.user, location=geoPoint(2.14899, 41.3888, srid=4326)
        )
        message = Message.objects.create(
            author=self.user, point=point, text="next_by_you"
        )
        return message

    def create_message_far(self):
        point = Point.objects.create(
            user=self.user, location=geoPoint(8.15899, 41.3888, srid=4326)
        )
        message = Message.objects.create(
            author=self.user, point=point, text="far_by_you"
        )
        return message

    def test_search_messages_no_auth(self):
        self.client.credentials()
        response = self.client.get(SEARCH_URL_NEXT)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_search_messages_with_auth_no_points(self):
        self.auth_token()
        response = self.client.get(SEARCH_URL_NEXT)
        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(len(response.data), 0)

    def test_search_messages_with_auth_near(self):
        self.auth_token()
        message_next = self.create_message_next()
        self.create_message_far()
        response = self.client.get(SEARCH_URL_NEXT)
        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["text"], message_next.text)

    def test_search_messages_with_auth_far(self):
        self.auth_token()
        message_next = self.create_message_next()
        message_far = self.create_message_far()
        response = self.client.get(SEARCH_URL_FAR)
        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(len(response.data), 2)
        texts = [i["text"] for i in response.data]
        self.assertIn(message_next.text, texts)
        self.assertIn(message_far.text, texts)
