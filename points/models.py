from django.contrib.auth import get_user_model
from django.contrib.gis.db import models

User = get_user_model()


class Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="points")
    location = models.PointField(geography=True, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location}"


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(blank=False)
    point = models.ForeignKey(
        Point, on_delete=models.CASCADE, related_name="point_messages"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.text}"
