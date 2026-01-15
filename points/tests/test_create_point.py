from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point as geoPoint
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from points.models import Point

CREATE_URL = "/api/points/"

User = get_user_model()


class TestCreatePoint(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", password="passuser")
        cls.token = Token.objects.create(user=cls.user)

    def auth_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_create_point_no_auth(self):
        points_before = Point.objects.count()
        response = self.client.post(
            CREATE_URL, {"latitude": 41.3888, "longitude": 2.15899}, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        self.assertEqual(points_before, Point.objects.count())

    def test_create_point_with_auth(self):
        self.auth_token()
        response = self.client.post(
            CREATE_URL, {"latitude": 41.3888, "longitude": 2.15899}, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Point.objects.count() == 1
        expected_location = geoPoint(2.15899, 41.3888, srid=4326)
        actual = Point.objects.first().location
        self.assertTrue(actual.equals_exact(expected_location, tolerance=0.000001))

    def test_create_point_set_user(self):
        self.auth_token()
        response = self.client.post(
            CREATE_URL,
            {"latitude": 41.3888, "longitude": 2.15899, "user": 150},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        point = Point.objects.get(id=response.data["id"])
        self.assertEqual(point.user, self.user)
        self.assertNotEqual(point.user.id, 150)

    def test_create_point_unvalidated(self):
        self.auth_token()
        response = self.client.post(
            CREATE_URL, {"latitude": 413888, "longitude": 2.15899}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
