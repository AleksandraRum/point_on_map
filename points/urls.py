from django.urls import path

from points.views import (MessageCreateView, MessageSearchGetView,
                          PointCreateView, PointSearchGetView)

urlpatterns = [
    path("points/", PointCreateView.as_view()),
    path("points/messages/", MessageCreateView.as_view()),
    path("points/search/", PointSearchGetView.as_view()),
    path("points/messages/search/", MessageSearchGetView.as_view()),
]
