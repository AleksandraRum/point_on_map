from django.contrib.gis.geos import Point as geoPoint
from django.contrib.gis.measure import D
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from points.models import Message, Point
from points.serializers import (MessageSerializer, PointSearchSerializer,
                                PointSerializer)


class PointCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Point.objects.all()
    serializer_class = PointSerializer


class MessageCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class PointSearchGetView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PointSerializer

    def get_queryset(self):
        params = PointSearchSerializer(data=self.request.query_params)
        params.is_valid(raise_exception=True)
        lon = params.validated_data["longitude"]
        lat = params.validated_data["latitude"]
        rad = params.validated_data["radius"]
        location = geoPoint(lon, lat, srid=4326)
        queryset = Point.objects.filter(location__distance_lte=(location, D(km=rad)))

        return queryset


class MessageSearchGetView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        params = PointSearchSerializer(data=self.request.query_params)
        params.is_valid(raise_exception=True)
        lon = params.validated_data["longitude"]
        lat = params.validated_data["latitude"]
        rad = params.validated_data["radius"]
        location = geoPoint(lon, lat, srid=4326)
        queryset = Message.objects.filter(
            point__location__distance_lte=(location, D(km=rad))
        )

        return queryset
