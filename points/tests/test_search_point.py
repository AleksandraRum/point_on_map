from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from points.models import Point

CREATE_URL = "/api/points/"
SEARCH_URL_NEXT = "/api/points/search/?latitude=41.3888&longitude=2.15899&radius=3"
SEARCH_URL_FAR = "/api/points/search/?latitude=41.3888&longitude=2.15899&radius=3000"
SEARCH_URL_WRONG = "/api/points/search/?latitude=41.3888&longitude=2.15899&radius=-3"

User = get_user_model()


class TestSearchPoints(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", password="passuser")
        cls.token = Token.objects.create(user=cls.user)

    def auth_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def create_point_next(self):
        self.auth_token()
        response = self.client.post(
            CREATE_URL, {"latitude": 41.3888, "longitude": 2.14899}, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        return Point.objects.get(id=response.data["id"])

    def create_point_far(self):
        self.auth_token()
        response = self.client.post(
            CREATE_URL, {"latitude": 41.3888, "longitude": 8.15899}, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        return Point.objects.get(id=response.data["id"])

    def test_search_points_no_auth(self):
        self.client.credentials()
        response = self.client.get(SEARCH_URL_NEXT)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_search_points_with_auth_no_points(self):
        self.auth_token()
        response = self.client.get(SEARCH_URL_NEXT)
        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(len(response.data), 0)

    def test_search_points_with_auth_near(self):
        point_next = self.create_point_next()
        self.create_point_far()
        response = self.client.get(SEARCH_URL_NEXT)
        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], point_next.id)

    def test_search_points_with_auth_far(self):
        point_next = self.create_point_next()
        point_far = self.create_point_far()
        response = self.client.get(SEARCH_URL_FAR)
        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(len(response.data), 2)
        ids = [i["id"] for i in response.data]
        self.assertIn(point_next.id, ids)
        self.assertIn(point_far.id, ids)

    def test_search_point_unvalidated(self):
        self.auth_token()
        response = self.client.get(SEARCH_URL_WRONG)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
